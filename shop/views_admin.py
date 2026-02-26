from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import (
    TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView, View
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Sum, Count, Avg, F
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from datetime import timedelta
from decimal import Decimal
import csv

from .models import Product, Category, Order, OrderItem
from .forms_admin import ProductForm, CategoryForm, OrderStatusForm


# Authentication decorator
def is_staff_or_superuser(user):
    """Check if user is staff or superuser"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


# Decorator for all admin views
staff_required = method_decorator(
    user_passes_test(is_staff_or_superuser, login_url='/myadmin/login/'),
    name='dispatch'
)


# Authentication Views
class AdminLoginView(LoginView):
    """Custom login view for MyAdmin"""
    template_name = 'myadmin/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('myadmin:dashboard')
    
    def form_valid(self, form):
        user = form.get_user()
        if not (user.is_staff or user.is_superuser):
            messages.error(self.request, 'Access denied. Staff privileges required.')
            return self.form_invalid(form)
        
        # Log successful login
        import logging
        logger = logging.getLogger('myadmin')
        logger.info(f"User {user.username} logged in from IP {self.request.META.get('REMOTE_ADDR')}")
        
        messages.success(self.request, f'Welcome back, {user.username}!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        # Log failed login attempt
        import logging
        logger = logging.getLogger('myadmin')
        username = form.data.get('username', 'unknown')
        logger.warning(f"Failed login attempt for username: {username} from IP: {self.request.META.get('REMOTE_ADDR')}")
        
        messages.error(self.request, 'Invalid credentials. Please try again.')
        return super().form_invalid(form)


class AdminLogoutView(LogoutView):
    """Custom logout view for MyAdmin"""
    next_page = '/myadmin/login/'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, 'You have been logged out successfully.')
        return super().dispatch(request, *args, **kwargs)


# Dashboard View
@staff_required
class DashboardView(TemplateView):
    """Main dashboard with KPIs and recent orders"""
    template_name = 'myadmin/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calculate current month start
        current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Calculate KPIs
        # Total revenue for current month (only confirmed and completed orders)
        total_revenue = Order.objects.filter(
            created_at__gte=current_month,
            status__in=['confirmed', 'processing', 'shipped', 'delivered']
        ).aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal('0.00')
        
        # Total orders for current month
        total_orders = Order.objects.filter(
            created_at__gte=current_month
        ).count()
        
        # Total unique customers (based on unique customer names)
        total_customers = Order.objects.values('customer_name').distinct().count()
        
        # Total active products
        total_products = Product.objects.filter(is_available=True).count()
        
        # Recent orders (last 10)
        recent_orders = Order.objects.select_related().order_by('-created_at')[:10]
        
        # Order status distribution
        status_distribution = Order.objects.values('status').annotate(
            count=Count('id')
        ).order_by('-count')
        
        context.update({
            'total_revenue': total_revenue,
            'total_orders': total_orders,
            'total_customers': total_customers,
            'total_products': total_products,
            'recent_orders': recent_orders,
            'status_distribution': status_distribution,
        })
        
        return context


# Product Views
@staff_required
class ProductListView(ListView):
    """List all products with search and filters"""
    model = Product
    template_name = 'myadmin/products/list.html'
    context_object_name = 'products'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Product.objects.select_related('category').order_by('-created_at')
        
        # Search functionality
        search_query = self.request.GET.get('search', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        # Category filter
        category_filter = self.request.GET.get('category', '').strip()
        if category_filter:
            queryset = queryset.filter(category_id=category_filter)
        
        # Availability filter
        availability_filter = self.request.GET.get('availability', '').strip()
        if availability_filter == 'available':
            queryset = queryset.filter(is_available=True)
        elif availability_filter == 'unavailable':
            queryset = queryset.filter(is_available=False)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search_query'] = self.request.GET.get('search', '')
        context['category_filter'] = self.request.GET.get('category', '')
        context['availability_filter'] = self.request.GET.get('availability', '')
        return context


@staff_required
class ProductCreateView(CreateView):
    """Create a new product"""
    model = Product
    form_class = ProductForm
    template_name = 'myadmin/products/add.html'
    success_url = reverse_lazy('myadmin:product_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Product "{form.instance.name}" created successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


@staff_required
class ProductUpdateView(UpdateView):
    """Update an existing product"""
    model = Product
    form_class = ProductForm
    template_name = 'myadmin/products/edit.html'
    success_url = reverse_lazy('myadmin:product_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Product "{form.instance.name}" updated successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


@staff_required
class ProductDeleteView(DeleteView):
    """Delete a product with referential integrity check"""
    model = Product
    template_name = 'myadmin/products/delete_confirm.html'
    success_url = reverse_lazy('myadmin:product_list')
    
    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        
        # Check for associated order items
        order_item_count = OrderItem.objects.filter(product=product).count()
        if order_item_count > 0:
            messages.error(
                request,
                f'Cannot delete "{product.name}" because it appears in {order_item_count} order(s). '
                f'Products with order history cannot be deleted.'
            )
            return redirect('myadmin:product_list')
        
        product_name = product.name
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Product "{product_name}" deleted successfully!')
        return response


@staff_required
class ProductBulkActionView(View):
    """Handle bulk actions on products"""
    
    def post(self, request):
        action = request.POST.get('action')
        product_ids = request.POST.getlist('product_ids')
        
        if not product_ids:
            messages.warning(request, 'No products selected.')
            return redirect('myadmin:product_list')
        
        products = Product.objects.filter(id__in=product_ids)
        
        if action == 'mark_available':
            count = products.update(is_available=True)
            messages.success(request, f'{count} product(s) marked as available.')
        
        elif action == 'mark_unavailable':
            count = products.update(is_available=False)
            messages.success(request, f'{count} product(s) marked as unavailable.')
        
        elif action == 'delete':
            # Check for order items
            if OrderItem.objects.filter(product__in=products).exists():
                messages.error(request, 'Cannot delete products with associated orders.')
            else:
                count = products.count()
                products.delete()
                messages.success(request, f'{count} product(s) deleted successfully.')
        
        return redirect('myadmin:product_list')


# Order Views
@staff_required
class OrderListView(ListView):
    """List all orders with search and filters"""
    model = Order
    template_name = 'myadmin/orders/list.html'
    context_object_name = 'orders'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Order.objects.prefetch_related('items__product').order_by('-created_at')
        
        # Search functionality
        search_query = self.request.GET.get('search', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(order_number__icontains=search_query) | 
                Q(customer_name__icontains=search_query)
            )
        
        # Status filter
        status_filter = self.request.GET.get('status', '').strip()
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Date range filter
        date_from = self.request.GET.get('date_from', '').strip()
        date_to = self.request.GET.get('date_to', '').strip()
        if date_from and date_to:
            queryset = queryset.filter(created_at__date__range=[date_from, date_to])
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Order.STATUS_CHOICES
        context['search_query'] = self.request.GET.get('search', '')
        context['status_filter'] = self.request.GET.get('status', '')
        context['date_from'] = self.request.GET.get('date_from', '')
        context['date_to'] = self.request.GET.get('date_to', '')
        return context


@staff_required
class OrderDetailView(DetailView):
    """View order details"""
    model = Order
    template_name = 'myadmin/orders/detail.html'
    context_object_name = 'order'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        
        # Get order items with products
        order_items = order.items.select_related('product').all()
        
        # Calculate subtotal sum
        subtotal_sum = sum(item.get_subtotal() for item in order_items)
        
        # Status form for updating
        context['status_form'] = OrderStatusForm(instance=order)
        context['order_items'] = order_items
        context['subtotal_sum'] = subtotal_sum
        
        return context


@staff_required
class OrderStatusUpdateView(UpdateView):
    """Update order status"""
    model = Order
    form_class = OrderStatusForm
    template_name = 'myadmin/orders/detail.html'
    
    def get_success_url(self):
        return reverse_lazy('myadmin:order_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        # Log status change
        import logging
        logger = logging.getLogger('myadmin')
        logger.info(
            f"Order {self.object.order_number} status changed from "
            f"{self.object.status} to {form.cleaned_data['status']} "
            f"by {self.request.user.username}"
        )
        
        messages.success(self.request, f'Order status updated to {form.cleaned_data["status"]}.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid status transition. Please check the allowed transitions.')
        return redirect('myadmin:order_detail', pk=self.object.pk)


# Category Views
@staff_required
class CategoryListView(ListView):
    """List all categories"""
    model = Category
    template_name = 'myadmin/categories/list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.annotate(
            product_count=Count('products')
        ).order_by('name')


@staff_required
class CategoryCreateView(CreateView):
    """Create a new category"""
    model = Category
    form_class = CategoryForm
    template_name = 'myadmin/categories/form.html'
    success_url = reverse_lazy('myadmin:category_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Category "{form.instance.name}" created successfully!')
        return super().form_valid(form)


@staff_required
class CategoryUpdateView(UpdateView):
    """Update an existing category"""
    model = Category
    form_class = CategoryForm
    template_name = 'myadmin/categories/form.html'
    success_url = reverse_lazy('myadmin:category_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Category "{form.instance.name}" updated successfully!')
        return super().form_valid(form)


@staff_required
class CategoryDeleteView(DeleteView):
    """Delete a category with referential integrity check"""
    model = Category
    template_name = 'myadmin/categories/delete_confirm.html'
    success_url = reverse_lazy('myadmin:category_list')
    
    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        
        # Check for associated products
        if category.products.exists():
            product_count = category.products.count()
            messages.error(
                request,
                f'Cannot delete "{category.name}" because it has {product_count} associated product(s).'
            )
            return redirect('myadmin:category_list')
        
        category_name = category.name
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Category "{category_name}" deleted successfully!')
        return response


# Analytics Views
@staff_required
class AnalyticsView(TemplateView):
    """Analytics dashboard with reports"""
    template_name = 'myadmin/analytics/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get date range from request or default to last 30 days
        date_to = timezone.now().date()
        date_from = date_to - timedelta(days=30)
        
        if self.request.GET.get('date_from'):
            date_from = timezone.datetime.strptime(self.request.GET.get('date_from'), '%Y-%m-%d').date()
        if self.request.GET.get('date_to'):
            date_to = timezone.datetime.strptime(self.request.GET.get('date_to'), '%Y-%m-%d').date()
        
        # Filter orders by date range
        orders = Order.objects.filter(created_at__date__range=[date_from, date_to])
        
        # Calculate metrics
        total_revenue = orders.filter(
            status__in=['confirmed', 'processing', 'shipped', 'delivered']
        ).aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal('0.00')
        
        total_orders = orders.count()
        
        average_order_value = orders.aggregate(
            Avg('total_amount')
        )['total_amount__avg'] or Decimal('0.00')
        
        # Top products by quantity
        top_products_quantity = OrderItem.objects.filter(
            order__created_at__date__range=[date_from, date_to]
        ).values('product__name').annotate(
            total_quantity=Sum('quantity')
        ).order_by('-total_quantity')[:10]
        
        # Top products by revenue
        top_products_revenue = OrderItem.objects.filter(
            order__created_at__date__range=[date_from, date_to]
        ).values('product__name').annotate(
            total_revenue=Sum(F('quantity') * F('price'))
        ).order_by('-total_revenue')[:10]
        
        # Order status distribution
        order_status_distribution = orders.values('status').annotate(
            count=Count('id')
        ).order_by('-count')
        
        context.update({
            'date_from': date_from,
            'date_to': date_to,
            'total_revenue': total_revenue,
            'total_orders': total_orders,
            'average_order_value': average_order_value,
            'top_products_quantity': top_products_quantity,
            'top_products_revenue': top_products_revenue,
            'order_status_distribution': order_status_distribution,
        })
        
        return context


@staff_required
class AnalyticsExportView(View):
    """Export analytics data as CSV"""
    
    def get(self, request):
        # Get date range
        date_to = timezone.now().date()
        date_from = date_to - timedelta(days=30)
        
        if request.GET.get('date_from'):
            date_from = timezone.datetime.strptime(request.GET.get('date_from'), '%Y-%m-%d').date()
        if request.GET.get('date_to'):
            date_to = timezone.datetime.strptime(request.GET.get('date_to'), '%Y-%m-%d').date()
        
        # Create CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="analytics_{date_from}_{date_to}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Order Number', 'Customer', 'Total', 'Status', 'Date'])
        
        orders = Order.objects.filter(
            created_at__date__range=[date_from, date_to]
        ).order_by('-created_at')
        
        for order in orders:
            writer.writerow([
                order.order_number,
                order.customer_name,
                order.total_amount,
                order.get_status_display(),
                order.created_at.strftime('%Y-%m-%d %H:%M')
            ])
        
        return response
