from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название категории')
    image = models.ImageField(upload_to='categories/', verbose_name='Изображение', blank=True, null=True)
    slug = models.SlugField(unique=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories',
                               related_query_name='subcategories', verbose_name='Категория')

    def get_absolute_url(self):
        return reverse('category_page', kwargs={'slug': self.slug})

    def get_image_category(self):
        if self.image:
            return self.image.url
        else:
            return '-'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Brand(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название Бренда')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='brand', verbose_name='Категория',
                                 blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренд'


class Product(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название Товара')
    price = models.FloatField(verbose_name='Цена')
    quantity = models.IntegerField(verbose_name='Количество')
    slug = models.SlugField(unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    edited_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, null=True, blank=True)
    color_code = models.TextField(default='#000000', verbose_name='Код цвета', null=True, blank=True)
    color_name = models.TextField(default='Желтый', verbose_name='Цвет', null=True, blank=True)
    description_all = models.TextField(verbose_name='Описание для страницы о товаре', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_image_product(self):
        if self.images:
            try:
                return self.images.first().image.url
            except:
                return '-'
        else:
            return '-'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Gallery(models.Model):
    image = models.ImageField(upload_to='products', verbose_name='Картинка товара')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'


class ProductDescription(models.Model):
    parameter = models.CharField(max_length=255, verbose_name='Название параметра')
    parameter_info = models.CharField(max_length=400, verbose_name='Описание параметра')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='parameters', verbose_name='Продукт')

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметры'


class FavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользоваель')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')

    def __str__(self):
        return f'Продукт {self.product.title}, {self.user.username}'

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные товары'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(max_length=255, default='', verbose_name='Имя')
    last_name = models.CharField(max_length=255, default='', verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Почта покупателя', blank=True, null=True)

    def __str__(self):
        return f'Покупатель {self.first_name}'

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone_number = models.CharField(blank=True, null=True, max_length=30, verbose_name='Номер телефона')
    city = models.CharField(blank=True, null=True, max_length=30, verbose_name='Город')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, verbose_name='Покупатель', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    is_completed = models.BooleanField(default=False)
    shipping = models.BooleanField(default=True, verbose_name='Строка')

    def __str__(self):
        return f'Заказ №: {self.pk}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    @property
    def get_cart_total_price(self):
        order_products = self.orderproduct_set.all()
        total_price = sum([product.get_total_price for product in order_products])
        return total_price

    @property
    def get_cart_total_quantity(self):
        order_products = self.orderproduct_set.all()
        total_price = sum([product.quantity for product in order_products])
        return total_price


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name='Кол-во')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return f'{self.product.title} {self.order}'

    class Meta:
        verbose_name = 'Заказанный товар'
        verbose_name_plural = 'Заказанный товары'

    @property
    def get_total_price(self):
        total_price = self.product.price * self.quantity
        return total_price


class ShippingAdress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name='Заказ')
    address = models.CharField(max_length=255, verbose_name='Адрес ул.дом.кв')
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
    region = models.CharField(max_length=100, verbose_name='Регион')
    comment = models.CharField(max_length=255, null=True, blank=True, verbose_name='Коммент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата доставки')
    phone = models.CharField(max_length=100, verbose_name='Номер телефона')

    def __str__(self):
        return f'{self.address} покупателя'

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставки'


class City(models.Model):
    city_name = models.CharField(max_length=100, verbose_name='Название города')

    def __str__(self):
        return self.city_name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
