from random import randint

import stripe
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from .models import *
from .forms import LoginForm, RegisterForm, ReviewForm, CustomerForm, ShippingForm, ProfileForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import get_cart_data, CartForAuthenticatedUser
# from shop_project import settings


# Create your views here.


class ProductList(ListView):
    model = Product
    context_object_name = 'categories'
    extra_context = {
        'title': 'Главная старница'
    }
    template_name = 'shop/index.html'

    def get_queryset(self):
        categories = Category.objects.filter(parent=None)
        return categories


class ContactList(ListView):
    model = Product
    extra_context = {
        'title': 'Контакты'
    }
    template_name = 'shop/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review_form.save()
        return super().get(request, *args, **kwargs)


class AboutList(ListView):
    model = Product
    extra_context = {
        'title': 'О сайте'
    }
    template_name = 'shop/about.html'


class CategoryView(ListView):
    model = Product
    context_object_name = 'products'
    extra_context = {
        'title': f'Котегории'
    }
    template_name = 'shop/category_page.html'

    # Method products for slug
    def get_queryset(self):
        main_category = Category.objects.get(slug=self.kwargs['slug'])
        subcategories = main_category.subcategories.all()
        products = Product.objects.filter(category__in=subcategories)

        return products


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        product = Product.objects.get(slug=self.kwargs['slug'])
        get_product = Product.objects.all()
        context['title'] = f'{product.category}: {product.title}'
        context['get_product'] = get_product


        return context


def login_register(request):
    context = {
        'form': LoginForm(),
        'form2': RegisterForm()
    }

    return render(request, 'shop/login_register.html', context)


def register(request):
    form = RegisterForm(data=request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Регистрация прошла успешною. Войдите в аккаунт')
        return redirect('index')


    else:
        for field in form.errors:
            messages.error(request, form.errors[field].as_text())

    return redirect('index')


def user_login(request):
    if not request.user.is_authenticated:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Успешный вход')
            return redirect('index')
        else:
            messages.warning(request, 'Не верный логин или пароль')
            return redirect('login_register')
    else:
        return redirect('index')


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.warning(request, 'Вы вышли из аккаунта')
        page = request.META.get('HTTP_REFERER', 'index')
        return redirect(page)
    else:
        return redirect('index')


def save_favourite_product(request, slug):
    user = request.user if request.user.is_authenticated else None
    product = Product.objects.get(slug=slug)
    favourite_products = FavouriteProducts.objects.filter(user=user)
    if user:
        if product in [i.product for i in favourite_products]:
            fav_product = FavouriteProducts.objects.get(user=user, product=product)
            fav_product.delete()
            messages.warning(request, 'Товар удалён из Избранного')
            print(f'Tовар {product.title} удалён из Избранного')
        else:
            FavouriteProducts.objects.create(user=user, product=product)
            messages.success(request, 'Товар добавлен в Избранное')
            print(f'Tовар {product.title} добавлен в Избранное')

    page = request.META.get('HTTP_REFERER', 'index')
    return redirect(page)


# Функция для страницы избранного товара
class FavoriteProductView(LoginRequiredMixin, ListView):
    model = FavouriteProducts
    context_object_name = 'products'
    template_name = 'shop/favorite_product.html'
    login_url = 'index'

    def get_queryset(self):
        user = self.request.user
        favs = FavouriteProducts.objects.filter(user=user)
        products = [i.product for i in favs]
        return products


# Function for page cart
def cart(request):
    if request.user.is_authenticated:
        cart_info = get_cart_data(request)

        context = {
            'title': 'Корзина покупателя',
            'order': cart_info['order'],
            'products': cart_info['products'],
            'cart_total_quantity': cart_info['cart_total_quantity']
        }

        return render(request, 'shop/cart.html', context)
    else:
        return redirect('index')


# Function for add product to cart
def to_cart(request, product_id, action):
    if request.user.is_authenticated:
        user_cart = CartForAuthenticatedUser(request, product_id, action)
        page = request.META.get('HTTP_REFERER', 'index')
        if action == 'add':
            messages.success(request, 'Товар добавден в карзину')
        else:
            messages.warning(request, 'Товар удалён из карзины')
        return redirect(page)
    else:
        messages.error(request, 'Авторизуйтесь что-бы добавить товар в карзину')
        page = request.META.get('HTTP_REFERER', 'index')
        return redirect(page)

# Function page of ckeck
def checkout(request):
    if request.user.is_authenticated:
        cart_info = get_cart_data(request)

        context = {
            'cart_total_quantity': cart_info['cart_total_quantity'],
            'order': cart_info['order'],
            'items': cart_info['products'],

            'customer_form': CustomerForm(),
            'shipping_form': ShippingForm(),
            'title': 'Оформление заказа'
        }
        return render(request, 'shop/checkout.html', context)
    else:
        return redirect('index')


class SearchResults(ProductList):
    def get_queryset(self):
        word = self.request.GET.get('q')
        cinemas = Product.objects.filter(title__iregex=word)  # По данному слову находим фильмы
        print(cinemas)
        return cinemas


def profile_edit(request):
    if request.user.is_authenticated:
        cart_info = get_cart_data(request)

        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)

        if request.method == 'POST':
            form = ProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Ваши данные успешно изменены')
                return redirect('profile_edit')
        else:
            form = ProfileForm(instance=profile)
        context = {
            'title': 'Корзина покупателя',
            'order': cart_info['order'],
            'products': cart_info['products'],
            'cart_total_quantity': cart_info['cart_total_quantity'],
            'form': form
        }
        return render(request, 'shop/profile_edit.html', context)
    else:
        return redirect('index')



# def create_checkout_session(request):
#     stripe.api_key = settings.STRIPE_SECRET_KEY
#     if request.method == 'POST':
#         user_cart = CartForAuthenticatedUser(request)
#         cart_info = user_cart.get_cart_info()
#
#         customer_form = CustomerForm(data=request.POST)
#         if customer_form.is_valid():
#             customer = Customer.objects.get(user=request.user)
#             customer.first_name = customer_form.cleaned_data['first_name']
#             customer.last_name = customer_form.cleaned_data['last_name']
#             customer.save()
#
#         shipping_form = ShippingForm(data=request.POST)
#         if shipping_form.is_valid():
#             address = shipping_form.save(commit=False)
#             address.customer = Customer.objects.get(user=request.user)
#             address.order = user_cart.get_cart_info()['order']
#             address.save()
#
#         total_price = cart_info['cart_total_price']
#         session = stripe.checkout.Session.create(
#             line_items=[{
#                 'price_data': {
#                     'currency': 'usd',
#                     'product_data': {
#                         'name': 'Покупка на Loft Mebel',
#                     },
#                     'unit_amount': int(total_price)
#                 },
#                 'quantity': 1
#             }],
#             mode='payment',
#             success_url=request.build_absolute_uti(reverse('index')),
#             cancel_url=request.build_absolute_uti(reverse('cart'))
#         )
#
#         return redirect(session.url, 303)


def successPatment(request):
    # user_cart = CartForAuthenticatedUser
    # user_cart.clear()
    messages.success(request, 'Ваша оплата прошла успешно')
    return redirect('index')











