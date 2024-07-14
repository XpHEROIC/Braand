from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductList.as_view(), name='index'),
    path('contact/', ContactList.as_view(), name='contact'),
    path('about/', AboutList.as_view(), name='about'),
    path('category/<slug:slug>/', CategoryView.as_view(), name='category_detail'),
    path('product/<slug:slug>/', ProductDetail.as_view(), name='product_detail'),
    path('registration/', login_register, name='login_register'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('add_favorite/<slug:slug>/', save_favourite_product, name='add_favorite'),
    path('my_favorite/', FavoriteProductView.as_view(), name='my_favorite'),
    path('cart/', cart, name='cart'),
    path('to_cart/<int:product_id>/<str:action>/', to_cart, name='to_cart'),
    path('checkout/', checkout, name='checkout'),
    path('search/', SearchResults.as_view(), name='search'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('success/', successPatment, name='success')
    # path('payment/', create_checkout_session, name='payment')


    # path('search/', SearchView.as_view(), name='search'),
]
