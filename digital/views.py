from random import randint
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from django.views import View

from .models import *
from django.views.generic import ListView, DetailView, UpdateView
from .forms import LoginForm, RegisterForm, EditAccountForm, EditProfileForm, CustomerForm, ShippingForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
import stripe
from shop import settings

# Create your views here.
from .utils import CartForAuthenticatedUser, get_cart_data


class ProductList(ListView):
    model = Product
    context_object_name = 'categories'
    template_name = 'digital/index.html'
    extra_context = {
        'title': 'Главная страница'
    }

    def get_queryset(self):
        categories = Category.objects.filter(parent=None)
        return categories


def user_login(request):
    if request.user.is_authenticated:
        page = request.META.get('HTTP_REFERER', 'index')
        return redirect(page)
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, 'Вы вошли в аккаунт✔')
                return redirect('index')
            else:
                messages.error(request, 'Неверный логин или пароль')
                return redirect('login')
        else:
            messages.error(request, 'Неверный логин или пароль')
            return redirect('login')
    else:
        form = LoginForm()

    context = {
        'form': form,
        'title': 'Вход в аккаунт'
    }

    return render(request, 'digital/login.html', context)


def user_logout(request):
    logout(request)
    messages.warning(request, 'Вы вышли с аккаунта😪')
    return redirect('index')


class CategoryView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'digital/category_page.html'
    extra_context = {
        'title': 'Категории'
    }

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['slug'])
        products = Product.objects.filter(category=category)
        return products


def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                profile = Profile.objects.create(user=user)
                profile.save()
                messages.success(request, 'Вы успешно зарегистрировались, Войдите в аккаунт')
                return redirect('login')
            else:
                for field in form.errors:
                    messages.error(request, form.errors[field].as_text())

                return redirect('register')
        else:
            form = RegisterForm()

        context = {
            'title': 'Регистрация',
            'form': form
        }

        return render(request, 'digital/register.html', context)


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        product = Product.objects.get(slug=self.kwargs['slug'])
        context['title'] = f'Товар {product.title}'
        products = Product.objects.all()

        data = []

        for i in range(len(products)):
            random_index = randint(0, len(products) - 1)
            p = products[random_index]
            if p not in data and product != p:
                data.append(p)

            context['products'] = data

        return context


def save_favorite_product(request, slug):
    if request.user.is_authenticated:
        user = request.user
        product = Product.objects.get(slug=slug)
        favorite_products = FavoriteProduct.objects.filter(user=user)
        if user:
            if product not in [i.product for i in favorite_products]:
                messages.success(request, f'Товар {product.title} в избранном')
                FavoriteProduct.objects.create(user=user, product=product)
            else:
                fav_product = FavoriteProduct.objects.get(user=user, product=product)
                messages.warning(request, f'Товар {product.title} удалён из избранного')
                fav_product.delete()

        page = request.META.get('HTTP_REFERER', 'index')
        return redirect(page)

    else:
        messages.warning(request, 'Авторизуйтесь, для добавления товара в Избранное')
        return redirect('login')


class FavoriteProductsView(LoginRequiredMixin, ListView):
    model = FavoriteProduct
    context_object_name = 'products'
    template_name = 'digital/favorite.html'
    login_url = 'login'

    def get_queryset(self):
        user = self.request.user
        favorite_products = FavoriteProduct.objects.filter(user=user)
        products = [i.product for i in favorite_products]
        return products


def profile_view(request, pk):
    profile = Profile.objects.get(user_id=pk)
    cart_info = get_cart_data(request)

    context = {
        'title': f'Профиль: {profile.user.username}',
        'profile': profile,
        'order': cart_info['order'],
        'products': cart_info['products']
    }

    return render(request, 'digital/profile.html', context)


def edit_account_view(request, pk):
    if request.user.pk == pk:
        context = {
            'edit_account_form': EditAccountForm(instance=request.user if request.user.is_authenticated else None)
        }
        return render(request, 'digital/edit_user.html', context)
    else:
        return redirect('index')


def edit_profile_view(request, pk):
    cart_info = get_cart_data(request)
    if request.user.pk == pk:
        context = {
            'edit_profile_form': EditProfileForm(
                instance=request.user.profile if request.user.is_authenticated else None)
        }
        return render(request, 'digital/edit_user.html', context)
    else:
        return redirect('index')


def chg_account_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = EditAccountForm(request.POST, instance=request.user)
            if form.is_valid():
                data = form.cleaned_data
                user = User.objects.get(id=request.user.id)
                if user.check_password(data['old_password']):
                    if data['new_password'] == data['confirm_password']:
                        user.set_password(data['new_password'])
                        user.save()
                        update_session_auth_hash(request, user)
                        return redirect('profile', user.pk)
                    else:
                        for field in form.errors:
                            messages.error(request, form.errors[field].as_text())
                            return redirect('edit_account', user.pk)
                else:
                    for field in form.errors:
                        messages.error(request, form.errors[field].as_text())
                        return redirect('edit_account', user.pk)

                form.save()

            else:
                for field in form.errors:
                    messages.error(request, form.errors[field].as_text())
                    return redirect('edit_account', request.user.pk)

            return redirect('profile', request.user.pk)

    else:
        return redirect('login')


def to_cart_view(request, action, pk):
    if request.user.is_authenticated:
        user_cart = CartForAuthenticatedUser(request, pk, action)
        page = request.META.get('HTTP_REFERER', 'index')
        if action == 'add':
            messages.success(request, 'Товар добавлен в корзину')
        elif action == 'del':
            messages.success(request, 'Кол-во товара уменьшено')
        return redirect(page)
    else:
        messages.warning(request, 'Авторизуйтесь')
        return redirect('login')


def my_cart_view(request):
    if request.user.is_authenticated:
        cart_info = get_cart_data(request)

        context = {
            'title': 'Моя корзина',
            'order': cart_info['order'],
            'products': cart_info['products']
        }

        return render(request, 'digital/my_cart.html', context)
    else:
        return redirect('login')


class SearchResults(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'digital/category_page.html'

    def get_queryset(self):
        word = self.request.GET.get('q')
        products = Product.objects.filter(title__iregex=word)

        print(word)
        return products


def chg_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
        user = request.user
        return redirect('profile', user.pk)


def contacts(request):
    context = {
        'title': 'Адрес нашей компании'
    }
    return render(request, 'digital/address.html', context)


def checkout(request):
    if request.user.is_authenticated:
        cart_info = get_cart_data(request)
        context = {
            'title': 'Оформить заказ',
            'order': cart_info['order'],
            'items': cart_info['products'],
            'customer_form': CustomerForm(),
            'shipping_form': ShippingForm()
        }
        return render(request, 'digital/checkout.html', context)
    else:
        return redirect('login')


def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        user_cart = CartForAuthenticatedUser(request)
        cart_info = user_cart.get_cart_info()

        customer_form = CustomerForm(data=request.POST)
        if customer_form.is_valid():
            customer = Customer.objects.get(user=request.user)
            customer.first_name = customer_form.cleaned_data['first_name']
            customer.last_name = customer_form.cleaned_data['last_name']
            customer.email = customer_form.cleaned_data['email']
            customer.save()

        shipping_form = ShippingForm(data=request.POST)
        if shipping_form.is_valid():
            address = shipping_form.save(commit=False)
            address.customer = Customer.objects.get(user=request.user)
            address.order = user_cart.get_cart_info()['order']
            address.save()

        else:
            for field in shipping_form.errors:
                messages.warning(request, shipping_form.errors[field].as_text())

        total_price = cart_info['cart_total_price']
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'DigitalStore товары'
                    },
                    'unit_amount': int(total_price)
                },
                'quantity': 1
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('success')),
            cancel_url=request.build_absolute_uri(reverse('checkout'))
        )
        return redirect(session.url, 303)


def success_payment(request):
    if request.user.is_authenticated:
        user_cart = CartForAuthenticatedUser(request)
        # Реализовать логику сохранения заказа после оплаты

        user_cart.clear()
        messages.success(request, 'Оплата прошла успешно. Мы вас кинули спаибо покупайте ещё.')
        return render(request, 'digital/success.html')

    else:
        return redirect('index')


def clear_cart(request):
    user_cart = CartForAuthenticatedUser(request)
    order = user_cart.get_cart_info()['order']
    order_products = order.orderproduct_set.all()
    for order_product in order_products:
        quantity = order_product.quantity
        product = order_product.product
        order_product.delete()
        product.quantity += quantity
        product.save()

    return redirect('my_cart')


def about_us(request):
    context = {
        'title': 'О нас'
    }
    return render(request, 'digital/about_us.html', context)
