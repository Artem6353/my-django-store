from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="Товар")
    price = models.FloatField(verbose_name="Цена")
    image = models.ImageField(upload_to='products/', verbose_name="Фото")
    manual_url = models.URLField(verbose_name="Ссылка на инструкцию")

    def __str__(self):
        return self.title

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_number = models.IntegerField(verbose_name="Номер заказа")
    customer_email = models.EmailField(verbose_name="Email клиента")
    order_date = models.DateField(verbose_name="Дата заказа")
    order_time = models.TimeField(verbose_name="Время заказа")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    invoice_file = models.FileField(upload_to='invoices/', verbose_name="Чек")
    quantity = models.IntegerField(verbose_name="Количество")