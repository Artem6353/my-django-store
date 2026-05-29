from django import forms
from .models import Order, Category, Product

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date'}),
            'order_time': forms.TimeInput(attrs={'type': 'time'}),
        }