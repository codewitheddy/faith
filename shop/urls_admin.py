from django.urls import path
from . import views_admin

app_name = 'myadmin'

urlpatterns = [
    # Authentication
    path('login/', views_admin.AdminLoginView.as_view(), name='login'),
    path('logout/', views_admin.AdminLogoutView.as_view(), name='logout'),
    
    # Dashboard
    path('', views_admin.DashboardView.as_view(), name='dashboard'),
    
    # Products
    path('products/', views_admin.ProductListView.as_view(), name='product_list'),
    path('products/add/', views_admin.ProductCreateView.as_view(), name='product_add'),
    path('products/performance/', views_admin.ProductPerformanceView.as_view(), name='product_performance'),
    path('products/<int:pk>/edit/', views_admin.ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', views_admin.ProductDeleteView.as_view(), name='product_delete'),
    path('products/bulk-action/', views_admin.ProductBulkActionView.as_view(), name='product_bulk_action'),
    path('products/export/', views_admin.ProductExportView.as_view(), name='product_export'),
    path('products/<int:pk>/variants/', views_admin.ProductVariantsSaveView.as_view(), name='product_variants_save'),
    path('products/stock-update/', views_admin.ProductStockUpdateView.as_view(), name='product_stock_update'),

    # Orders
    path('orders/', views_admin.OrderListView.as_view(), name='order_list'),
    path('orders/bulk-action/', views_admin.OrderBulkActionView.as_view(), name='order_bulk_action'),
    path('orders/export/', views_admin.OrderExportView.as_view(), name='order_export'),
    path('orders/<int:pk>/', views_admin.OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/update-status/', views_admin.OrderStatusUpdateView.as_view(), name='order_update_status'),
    
    # Categories
    path('categories/', views_admin.CategoryListView.as_view(), name='category_list'),
    path('categories/add/', views_admin.CategoryCreateView.as_view(), name='category_add'),
    path('categories/<int:pk>/edit/', views_admin.CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', views_admin.CategoryDeleteView.as_view(), name='category_delete'),
    
    # Analytics
    path('analytics/', views_admin.AnalyticsView.as_view(), name='analytics'),
    path('analytics/export/', views_admin.AnalyticsExportView.as_view(), name='analytics_export'),
    path('customers/', views_admin.CustomerInsightsView.as_view(), name='customer_insights'),
    
    # User Management
    path('users/', views_admin.UserListView.as_view(), name='user_list'),
    path('users/add/', views_admin.UserCreateView.as_view(), name='user_add'),
    path('users/<int:pk>/edit/', views_admin.UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/password/', views_admin.UserPasswordChangeView.as_view(), name='user_password_change'),
    path('users/<int:pk>/delete/', views_admin.UserDeleteView.as_view(), name='user_delete'),

    # Hero Slides
    path('hero-slides/', views_admin.HeroSlideListView.as_view(), name='heroslide_list'),
    path('hero-slides/add/', views_admin.HeroSlideCreateView.as_view(), name='heroslide_add'),
    path('hero-slides/<int:pk>/edit/', views_admin.HeroSlideUpdateView.as_view(), name='heroslide_edit'),
    path('hero-slides/<int:pk>/delete/', views_admin.HeroSlideDeleteView.as_view(), name='heroslide_delete'),
]
