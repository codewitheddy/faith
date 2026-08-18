from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('cart/', views.cart, name='cart'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('get-cart/', views.get_cart, name='get_cart'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('api/product/<int:product_id>/stock/', views.product_stock_api, name='product_stock_api'),
    path('checkout/', views.checkout, name='checkout'),
    path('filter-products/', views.filter_products, name='filter_products'),
    path('search-suggest/', views.search_suggest, name='search_suggest'),
    # Account
    path('register/', views.register, name='register'),
    path('login/', views.account_login, name='login'),
    path('logout/', views.account_logout, name='logout'),
    path('account/', views.account_dashboard, name='account_dashboard'),
    path('account/orders/', views.account_orders, name='account_orders'),
    path('account/orders/<str:order_number>/', views.account_order_detail, name='account_order_detail'),
    path('account/wishlist/', views.account_wishlist, name='account_wishlist'),
    path('account/profile/', views.account_profile, name='account_profile'),
    path('wishlist/toggle/', views.toggle_wishlist, name='toggle_wishlist'),
]
