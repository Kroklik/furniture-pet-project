from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductList.as_view(), name='index'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('category_page/<slug:slug>/', CategoryView.as_view(), name='category_page'),
    path('register/', register_view, name='register'),
    path('product_detail/<slug:slug>/', ProductDetail.as_view(), name='product_detail'),
    path('add_favorite/<slug:slug>/', save_favorite_product, name='add_favorite'),
    path('favorite_products/', FavoriteProductsView.as_view(), name='my_favorite'),
    path('profile/<int:pk>', profile_view, name='profile'),
    path('edit_profile/<int:pk>/', edit_profile_view, name='edit_profile'),
    path('edit_account/<int:pk>/', edit_account_view, name='edit_account'),
    path('chg_account/', chg_account_view, name='chg_account'),
    path('chg_profile/', chg_profile, name='chg_profile'),
    path('to_cart/<int:pk>/<str:action>/', to_cart_view, name='to_cart'),
    path('my_cart/', my_cart_view, name='my_cart'),
    path('search/', SearchResults.as_view(), name='search'),
    path('address/', contacts, name='contacts'),
    path('checkout/', checkout, name='checkout'),
    path('payment/', create_checkout_session, name='payment'),
    path('success/', success_payment, name='success'),
    path('clear_cart/', clear_cart, name='clear_cart'),
    path('about_us/', about_us, name='about_us')



]
