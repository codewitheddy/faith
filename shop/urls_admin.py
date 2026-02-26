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
    path('products/<int:pk>/edit/', views_admin.ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', views_admin.ProductDeleteView.as_view(), name='product_delete'),
    path('products/bulk-action/', views_admin.ProductBulkActionView.as_view(), name='product_bulk_action'),
    
    # Orders
    path('orders/', views_admin.OrderListView.as_view(), name='order_list'),
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
]
