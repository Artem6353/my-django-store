from django.shortcuts import render, redirect, get_object_or_404
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
                return redirect('/#catalog')

        elif 'btn_product' in request.POST:
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('/#catalog')

        elif 'btn_order' in request.POST:
            form = OrderForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('/#catalog')

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

    context = {
        'cat_form': cat_form, 'prod_form': prod_form, 'ord_form': ord_form,
        'all_categories': all_categories, 'all_products': all_products, 'all_orders': all_orders,
        'q1': q1, 'q2': q2,
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
    return redirect('/#delete')