from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max, F
from .models import Category, Product, Order
from .forms import CategoryForm, ProductForm, OrderForm


def dashboard_view(request):
    # --- 1. ИНИЦИАЛИЗАЦИЯ ФОРМ ---
    cat_form = CategoryForm()
    prod_form = ProductForm()
    ord_form = OrderForm()

    # --- 2. ОБРАБОТКА ДОБАВЛЕНИЯ (POST) ---
    if request.method == 'POST':
        if 'btn_category' in request.POST:
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('dashboard')

        elif 'btn_product' in request.POST:
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('dashboard')

        elif 'btn_order' in request.POST:
            form = OrderForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('dashboard')

    # --- 3. ВСЕ ТАБЛИЦЫ (Сырые данные для вывода списков) ---
    # Мы берем все категории и сразу "приклеиваем" к ним связанные товары
    all_categories = Category.objects.prefetch_related('product_set').all()
    all_products = Product.objects.all().select_related('category')
    all_orders = Order.objects.all().select_related('product')

    # --- 4. ОТЧЁТЫ И ФИЛЬТРЫ (GET) ---
    search_q1 = request.GET.get('search_q1', '')
    q1 = Product.objects.filter(title__icontains=search_q1) if search_q1 else Product.objects.all()

    date_q2 = request.GET.get('date_q2')
    q2 = Order.objects.filter(order_date=date_q2) if date_q2 else Order.objects.all()

    q3 = Product.objects.aggregate(max_price=Max('price'))

    email_q4 = request.GET.get('email_q4', '')
    q4 = Order.objects.filter(customer_email__icontains=email_q4) if email_q4 else Order.objects.all()

    try:
        month_val = int(request.GET.get('month', 3))
        min_qty_val = int(request.GET.get('min_qty', 1))
    except (ValueError, TypeError):
        month_val, min_qty_val = 3, 1

    q5 = Order.objects.filter(order_date__month=month_val, quantity__gt=min_qty_val)
    q6 = Order.objects.annotate(total=F('quantity') * F('product__price'))
    q7 = Product.objects.all().order_by('-price')
    q8 = Product.objects.filter(price__gt=5000)

    context = {
        'cat_form': cat_form, 'prod_form': prod_form, 'ord_form': ord_form,
        'all_categories': all_categories, 'all_products': all_products, 'all_orders': all_orders,
        'q1': q1, 'q2': q2, 'q3': q3, 'q4': q4, 'q5': q5, 'q6': q6, 'q7': q7, 'q8': q8,
        'title': 'Панель управления магазином'
    }
    return render(request, 'store/dashboard.html', context)


# ФУНКЦИЯ УДАЛЕНИЯ
def delete_item(request, model_name, item_id):
    if model_name == 'category':
        obj = get_object_or_404(Category, id=item_id)
    elif model_name == 'product':
        obj = get_object_or_404(Product, id=item_id)
    elif model_name == 'order':
        obj = get_object_or_404(Order, id=item_id)

    obj.delete()
    return redirect('dashboard')