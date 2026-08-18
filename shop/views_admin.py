from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import (
    TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView, View
)
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.db.models import Q, Sum, Count, Avg, F, Min, Max
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.http import HttpResponse, JsonResponse
from datetime import timedelta
from decimal import Decimal
import csv

from .models import Product, Category, Order, OrderItem, Wishlist, ProductVariant
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


class AdminLogoutView(View):
    """Custom logout view for MyAdmin"""
    
    def get(self, request):
        """Handle GET request for logout"""
        from django.contrib.auth import logout
        
        if request.user.is_authenticated:
            username = request.user.username
            
            # Log logout
            import logging
            logger = logging.getLogger('myadmin')
            logger.info(f"User {username} logged out from IP {request.META.get('REMOTE_ADDR')}")
            
            # Logout user
            logout(request)
            messages.success(request, f'You have been logged out successfully.')
        
        return redirect('/myadmin/login/')
    
    def post(self, request):
        """Handle POST request for logout (for CSRF-protected forms)"""
        return self.get(request)


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
        
        # Low stock products (stock_quantity <= reorder_level)
        low_stock_products = Product.objects.filter(
            is_available=True,
            stock_quantity__gt=0,
            stock_quantity__lte=F('reorder_level')
        ).order_by('stock_quantity')[:10]
        
        # Out of stock products
        out_of_stock_products = Product.objects.filter(
            is_available=True,
            stock_quantity=0
        ).count()
        
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
            'low_stock_products': low_stock_products,
            'out_of_stock_count': out_of_stock_products,
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
        queryset = Product.objects.select_related('category').annotate(
            variant_count=Count('variants', distinct=True)
        ).order_by('-created_at')
        
        # Search functionality
        search_query = self.request.GET.get('search', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query) |
                Q(category__name__icontains=search_query)
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
        
        # Variants filter
        variants_filter = self.request.GET.get('variants', '').strip()
        if variants_filter == 'has':
            queryset = queryset.filter(variants__isnull=False).distinct()
        elif variants_filter == 'none':
            queryset = queryset.filter(variants__isnull=True)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search_query'] = self.request.GET.get('search', '')
        context['category_filter'] = self.request.GET.get('category', '')
        context['availability_filter'] = self.request.GET.get('availability', '')
        context['variants_filter'] = self.request.GET.get('variants', '')
        return context


@staff_required
class ProductExportView(View):
    """CSV export of products respecting current filters"""

    def get(self, request):
        view = ProductListView()
        view.request = request
        products = view.get_queryset().select_related('category')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products_export.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Category', 'Price (KES)', 'Sale Price (KES)', 'On Sale', 'Available', 'Variants', 'Views', 'Created'])
        for p in products:
            writer.writerow([
                p.name,
                p.category.name if p.category else '',
                str(p.price),
                str(p.sale_price) if p.sale_price else '',
                'Yes' if p.on_sale else 'No',
                'Yes' if p.is_available else 'No',
                p.variant_count,
                p.view_count,
                p.created_at.strftime('%Y-%m-%d'),
            ])
        return response


@staff_required
class ProductCreateView(CreateView):
    """Create a new product"""
    model = Product
    form_class = ProductForm
    template_name = 'myadmin/products/add.html'
    success_url = reverse_lazy('myadmin:product_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Save variants from hidden JSON field
        variants_json = self.request.POST.get('variants_json', '[]')
        try:
            import json
            variants = json.loads(variants_json)
            for i, v in enumerate(variants):
                name = v.get('name', '').strip()
                if not name:
                    continue
                from decimal import Decimal
                ProductVariant.objects.create(
                    product=self.object,
                    name=name,
                    price_adjustment=Decimal(str(v.get('price_adjustment', 0))),
                    is_available=bool(v.get('is_available', True)),
                    sort_order=i,
                )
        except json.JSONDecodeError as e:
            import logging
            logger = logging.getLogger('myadmin')
            logger.warning(f"Failed to parse variants JSON for product {self.object.id}: {str(e)}")
        except Exception as e:
            import logging
            logger = logging.getLogger('myadmin')
            logger.error(f"Failed to create variants for product {self.object.id}: {str(e)}")
        
        messages.success(self.request, f'Product "{form.instance.name}" created successfully!')
        return response

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
    """Delete a product - order history is preserved with '[Deleted Product]' placeholder"""
    model = Product
    template_name = 'myadmin/products/delete_confirm.html'
    success_url = reverse_lazy('myadmin:product_list')
    
    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        
        # Get order item count before deletion
        order_item_count = OrderItem.objects.filter(product=product).count()
        product_name = product.name
        
        # Product can be deleted - order items will show "[Deleted Product]"
        response = super().delete(request, *args, **kwargs)
        
        if order_item_count > 0:
            messages.warning(
                request,
                f'Product "{product_name}" deleted. It appears in {order_item_count} order(s), '
                f'which will now show "[Deleted Product]".'
            )
        else:
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
            # Count order items before deletion
            order_item_count = OrderItem.objects.filter(product__in=products).count()
            product_count = products.count()
            
            # Delete all selected products
            # Order items will retain quantity and price but product field becomes NULL
            products.delete()
            
            if order_item_count > 0:
                messages.warning(
                    request,
                    f'{product_count} product(s) deleted. They appeared in {order_item_count} order(s), '
                    f'which will now show "[Deleted Product]" for those items.'
                )
            else:
                messages.success(request, f'{product_count} product(s) deleted successfully.')
        
        return redirect('myadmin:product_list')


# Order Views
def _filtered_orders(request):
    """Shared order queryset builder for list, bulk actions and CSV export."""
    queryset = Order.objects.prefetch_related('items__product').order_by('-created_at')

    search_query = request.GET.get('search', '').strip()
    if search_query:
        queryset = queryset.filter(
            Q(order_number__icontains=search_query) |
            Q(customer_name__icontains=search_query) |
            Q(customer_phone__icontains=search_query) |
            Q(customer_email__icontains=search_query) |
            Q(customer_address__icontains=search_query)
        )

    status_filter = request.GET.get('status', '').strip()
    if status_filter:
        queryset = queryset.filter(status=status_filter)

    date_from = request.GET.get('date_from', '').strip()
    date_to = request.GET.get('date_to', '').strip()
    if date_from:
        queryset = queryset.filter(created_at__date__gte=date_from)
    if date_to:
        queryset = queryset.filter(created_at__date__lte=date_to)

    return queryset


def _get_order_filters_context(request):
    return {
        'search_query': request.GET.get('search', ''),
        'status_filter': request.GET.get('status', ''),
        'date_from': request.GET.get('date_from', ''),
        'date_to': request.GET.get('date_to', ''),
    }


@staff_required
class OrderListView(ListView):
    """List all orders with search and filters"""
    model = Order
    template_name = 'myadmin/orders/list.html'
    context_object_name = 'orders'
    paginate_by = 20

    def get_queryset(self):
        return _filtered_orders(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Order.STATUS_CHOICES
        context.update(_get_order_filters_context(self.request))

        # Per-status counts (respecting search/date filters, ignoring status filter)
        base = _filtered_orders(self.request)
        counts = {}
        for row in base.values('status').annotate(n=Count('id')):
            counts[row['status']] = row['n']
        context['status_counts'] = counts
        context['status_counts_total'] = sum(counts.values())
        return context


VALID_ORDER_TRANSITIONS = {
    'pending': ['confirmed', 'cancelled'],
    'confirmed': ['pending', 'processing', 'shipped', 'delivered', 'cancelled'],
    'processing': ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled'],
    'shipped': ['pending', 'confirmed', 'processing', 'delivered', 'cancelled'],
    'delivered': ['pending', 'confirmed', 'processing', 'shipped', 'cancelled'],
    'cancelled': ['pending', 'confirmed', 'processing', 'shipped', 'delivered'],
}


@staff_required
class OrderBulkActionView(View):
    """Handle bulk actions on orders: status updates (transition-validated) and delete"""

    def post(self, request):
        action = request.POST.get('action', '')
        order_ids = request.POST.getlist('order_ids')

        if not order_ids:
            messages.warning(request, 'No orders selected.')
            return redirect('myadmin:order_list')

        orders = Order.objects.filter(id__in=order_ids)

        if action.startswith('set_status_'):
            new_status = action.replace('set_status_', '')
            valid_statuses = [s for s, _ in Order.STATUS_CHOICES]
            if new_status not in valid_statuses:
                messages.error(request, 'Invalid status.')
                return redirect('myadmin:order_list')

            updated, skipped = 0, []
            for order in orders:
                if new_status in VALID_ORDER_TRANSITIONS.get(order.status, []):
                    order.status = new_status
                    order.save(update_fields=['status', 'updated_at'])
                    updated += 1
                else:
                    skipped.append(order.order_number)

            if updated:
                messages.success(request, f'{updated} order(s) updated to "{new_status}".')
            if skipped:
                messages.warning(
                    request,
                    f'Skipped {len(skipped)} order(s) with invalid transition: {", ".join(skipped[:5])}'
                    + ('…' if len(skipped) > 5 else '')
                )

        elif action == 'delete':
            count = orders.count()
            OrderItem.objects.filter(order__in=orders).delete()
            orders.delete()
            messages.success(request, f'{count} order(s) deleted successfully.')

        else:
            messages.warning(request, 'Unknown action.')

        # Preserve filters after bulk action
        params = []
        for key in ('search', 'status', 'date_from', 'date_to', 'page'):
            val = request.POST.get(key, '')
            if val:
                params.append(f'{key}={val}')
        url = reverse('myadmin:order_list')
        if params:
            url += '?' + '&'.join(params)
        return redirect(url)


@staff_required
class OrderExportView(View):
    """CSV export of orders respecting current filters"""

    def get(self, request):
        orders = _filtered_orders(request).select_related('user')

        import csv
        from django.http import HttpResponse
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="orders_export.csv"'

        writer = csv.writer(response)
        writer.writerow(['Order #', 'Status', 'Customer', 'Phone', 'Email', 'Address', 'Items', 'Total (KES)', 'Created'])
        for order in orders:
            writer.writerow([
                order.order_number,
                order.get_status_display(),
                order.customer_name,
                order.customer_phone,
                order.customer_email,
                order.customer_address.replace('\n', ' ') if order.customer_address else '',
                sum(item.quantity for item in order.items.all()),
                str(order.total_amount),
                order.created_at.strftime('%Y-%m-%d %H:%M'),
            ])
        return response


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
        next_url = self.request.POST.get('next', '')
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={self.request.get_host()}):
            return next_url
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

        messages.success(self.request, f'Order {self.object.order_number} status updated to {form.cleaned_data["status"]}.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid status transition. Please check the allowed transitions.')
        next_url = self.request.POST.get('next', '')
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={self.request.get_host()}):
            return redirect(next_url)
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

        # Date range — default last 30 days
        date_to = timezone.now().date()
        date_from = date_to - timedelta(days=30)

        if self.request.GET.get('date_from'):
            try:
                date_from = timezone.datetime.strptime(self.request.GET['date_from'], '%Y-%m-%d').date()
            except ValueError:
                pass
        if self.request.GET.get('date_to'):
            try:
                date_to = timezone.datetime.strptime(self.request.GET['date_to'], '%Y-%m-%d').date()
            except ValueError:
                pass

        # Previous period (same length) for comparison
        period_days = (date_to - date_from).days or 1
        prev_date_to = date_from - timedelta(days=1)
        prev_date_from = prev_date_to - timedelta(days=period_days)

        # Current period orders
        orders = Order.objects.filter(created_at__date__range=[date_from, date_to])
        paid_orders = orders.filter(status__in=['confirmed', 'processing', 'shipped', 'delivered'])

        # Previous period orders
        prev_orders = Order.objects.filter(created_at__date__range=[prev_date_from, prev_date_to])
        prev_paid = prev_orders.filter(status__in=['confirmed', 'processing', 'shipped', 'delivered'])

        # ── Core metrics ──────────────────────────────────
        total_revenue = paid_orders.aggregate(s=Sum('total_amount'))['s'] or Decimal('0')
        prev_revenue  = prev_paid.aggregate(s=Sum('total_amount'))['s'] or Decimal('0')

        total_orders = orders.count()
        prev_total_orders = prev_orders.count()

        # AOV — average order value of paid orders only
        aov = paid_orders.aggregate(a=Avg('total_amount'))['a'] or Decimal('0')
        prev_aov = prev_paid.aggregate(a=Avg('total_amount'))['a'] or Decimal('0')

        # Conversion rate: paid orders / total orders × 100
        conversion_rate = round((paid_orders.count() / total_orders * 100), 1) if total_orders else 0
        prev_conversion = round((prev_paid.count() / prev_total_orders * 100), 1) if prev_total_orders else 0

        # ── Period-over-period deltas ─────────────────────
        def pct_change(current, previous):
            if not previous:
                return None
            return round(float((current - previous) / previous * 100), 1)

        revenue_delta     = pct_change(total_revenue, prev_revenue)
        orders_delta      = pct_change(total_orders, prev_total_orders)
        aov_delta         = pct_change(aov, prev_aov)
        conversion_delta  = pct_change(conversion_rate, prev_conversion)

        # ── Daily sales trend (revenue + order count per day) ─
        from django.db.models.functions import TruncDate
        daily_qs = (
            paid_orders
            .annotate(day=TruncDate('created_at'))
            .values('day')
            .annotate(revenue=Sum('total_amount'), count=Count('id'))
            .order_by('day')
        )

        # Build complete date range (fill gaps with 0)
        from datetime import date as date_type
        day_map = {row['day']: row for row in daily_qs}
        trend_labels, trend_revenue, trend_orders = [], [], []
        current = date_from
        while current <= date_to:
            trend_labels.append(current.strftime('%b %d'))
            row = day_map.get(current)
            trend_revenue.append(float(row['revenue']) if row else 0)
            trend_orders.append(row['count'] if row else 0)
            current += timedelta(days=1)

        # ── Top products ──────────────────────────────────
        top_products_quantity = (
            OrderItem.objects
            .filter(order__created_at__date__range=[date_from, date_to])
            .values('product__name')
            .annotate(total_quantity=Sum('quantity'))
            .order_by('-total_quantity')[:8]
        )

        top_products_revenue = (
            OrderItem.objects
            .filter(order__created_at__date__range=[date_from, date_to])
            .values('product__name')
            .annotate(total_revenue=Sum(F('quantity') * F('price')))
            .order_by('-total_revenue')[:8]
        )

        # ── Order status distribution ─────────────────────
        order_status_distribution = (
            orders.values('status')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        # ── Category revenue breakdown ────────────────────
        category_revenue = (
            OrderItem.objects
            .filter(order__created_at__date__range=[date_from, date_to])
            .values('product__category__name')
            .annotate(revenue=Sum(F('quantity') * F('price')), units=Sum('quantity'))
            .order_by('-revenue')
        )

        import json
        context.update({
            'date_from': date_from,
            'date_to': date_to,
            'period_days': period_days,
            # Core metrics
            'total_revenue': total_revenue,
            'total_orders': total_orders,
            'aov': aov,
            'conversion_rate': conversion_rate,
            # Deltas
            'revenue_delta': revenue_delta,
            'orders_delta': orders_delta,
            'aov_delta': aov_delta,
            'conversion_delta': conversion_delta,
            # Chart data (JSON for JS)
            'trend_labels_json': json.dumps(trend_labels),
            'trend_revenue_json': json.dumps(trend_revenue),
            'trend_orders_json': json.dumps(trend_orders),
            # Tables
            'top_products_quantity': top_products_quantity,
            'top_products_revenue': top_products_revenue,
            'order_status_distribution': order_status_distribution,
            'category_revenue': category_revenue,
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



# User Management Views
@staff_required
class UserListView(ListView):
    """List all staff users"""
    model = None  # Will use User model
    template_name = 'myadmin/users/list.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def get_queryset(self):
        from django.contrib.auth.models import User
        queryset = User.objects.filter(is_staff=True).order_by('-date_joined')
        
        # Search functionality
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(username__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            )
        
        # Filter by status
        status_filter = self.request.GET.get('status', '')
        if status_filter == 'active':
            queryset = queryset.filter(is_active=True)
        elif status_filter == 'inactive':
            queryset = queryset.filter(is_active=False)
        
        # Filter by role
        role_filter = self.request.GET.get('role', '')
        if role_filter == 'superuser':
            queryset = queryset.filter(is_superuser=True)
        elif role_filter == 'staff':
            queryset = queryset.filter(is_superuser=False)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['status_filter'] = self.request.GET.get('status', '')
        context['role_filter'] = self.request.GET.get('role', '')
        return context


@staff_required
class UserCreateView(View):
    """Create a new staff user"""
    template_name = 'myadmin/users/form.html'
    
    def get(self, request):
        from .forms_admin import UserCreateForm
        form = UserCreateForm()
        return render(request, self.template_name, {
            'form': form,
            'title': 'Create New User',
            'action': 'Create'
        })
    
    def post(self, request):
        from django.contrib.auth.models import User
        from .forms_admin import UserCreateForm
        
        form = UserCreateForm(request.POST)
        
        if form.is_valid():
            # Create user
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data.get('email', ''),
                password=form.cleaned_data['password1'],
                first_name=form.cleaned_data.get('first_name', ''),
                last_name=form.cleaned_data.get('last_name', '')
            )
            
            user.is_staff = form.cleaned_data.get('is_staff', True)
            user.is_superuser = form.cleaned_data.get('is_superuser', False)
            user.save()
            
            # Log action
            import logging
            logger = logging.getLogger('myadmin')
            logger.info(f"User {request.user.username} created new user: {user.username}")
            
            messages.success(request, f'User "{user.username}" created successfully.')
            return redirect('myadmin:user_list')
        
        return render(request, self.template_name, {
            'form': form,
            'title': 'Create New User',
            'action': 'Create'
        })


@staff_required
class UserUpdateView(View):
    """Update an existing staff user"""
    template_name = 'myadmin/users/form.html'
    
    def get(self, request, pk):
        from django.contrib.auth.models import User
        from .forms_admin import UserEditForm
        
        user = get_object_or_404(User, pk=pk, is_staff=True)
        
        form = UserEditForm(initial={
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
        })
        
        return render(request, self.template_name, {
            'form': form,
            'user_obj': user,
            'title': f'Edit User: {user.username}',
            'action': 'Update'
        })
    
    def post(self, request, pk):
        from django.contrib.auth.models import User
        from .forms_admin import UserEditForm
        
        user = get_object_or_404(User, pk=pk, is_staff=True)
        form = UserEditForm(request.POST)
        
        if form.is_valid():
            user.email = form.cleaned_data.get('email', '')
            user.first_name = form.cleaned_data.get('first_name', '')
            user.last_name = form.cleaned_data.get('last_name', '')
            user.is_active = form.cleaned_data.get('is_active', True)
            user.is_staff = form.cleaned_data.get('is_staff', True)
            user.is_superuser = form.cleaned_data.get('is_superuser', False)
            user.save()
            
            # Log action
            import logging
            logger = logging.getLogger('myadmin')
            logger.info(f"User {request.user.username} updated user: {user.username}")
            
            messages.success(request, f'User "{user.username}" updated successfully.')
            return redirect('myadmin:user_list')
        
        return render(request, self.template_name, {
            'form': form,
            'user_obj': user,
            'title': f'Edit User: {user.username}',
            'action': 'Update'
        })


@staff_required
class UserPasswordChangeView(View):
    """Change user password"""
    template_name = 'myadmin/users/password_change.html'
    
    def get(self, request, pk):
        from django.contrib.auth.models import User
        from .forms_admin import UserPasswordChangeForm
        
        user = get_object_or_404(User, pk=pk, is_staff=True)
        form = UserPasswordChangeForm()
        
        return render(request, self.template_name, {
            'form': form,
            'user_obj': user
        })
    
    def post(self, request, pk):
        from django.contrib.auth.models import User
        from .forms_admin import UserPasswordChangeForm
        
        user = get_object_or_404(User, pk=pk, is_staff=True)
        form = UserPasswordChangeForm(request.POST)
        
        if form.is_valid():
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            
            # Log action
            import logging
            logger = logging.getLogger('myadmin')
            logger.info(f"User {request.user.username} changed password for user: {user.username}")
            
            messages.success(request, f'Password for "{user.username}" changed successfully.')
            return redirect('myadmin:user_list')
        
        return render(request, self.template_name, {
            'form': form,
            'user_obj': user
        })


@staff_required
class UserDeleteView(View):
    """Delete a staff user"""
    template_name = 'myadmin/users/delete_confirm.html'
    
    def get(self, request, pk):
        from django.contrib.auth.models import User
        user = get_object_or_404(User, pk=pk, is_staff=True)
        
        # Prevent deleting yourself
        if user == request.user:
            messages.error(request, 'You cannot delete your own account.')
            return redirect('myadmin:user_list')
        
        return render(request, self.template_name, {'user_obj': user})
    
    def post(self, request, pk):
        from django.contrib.auth.models import User
        user = get_object_or_404(User, pk=pk, is_staff=True)
        
        # Prevent deleting yourself
        if user == request.user:
            messages.error(request, 'You cannot delete your own account.')
            return redirect('myadmin:user_list')
        
        username = user.username
        user.delete()
        
        # Log action
        import logging
        logger = logging.getLogger('myadmin')
        logger.info(f"User {request.user.username} deleted user: {username}")
        
        messages.success(request, f'User "{username}" deleted successfully.')
        return redirect('myadmin:user_list')


# Product Performance View
@staff_required
class ProductPerformanceView(TemplateView):
    """Product performance: sales, views, wishlist, low-sellers"""
    template_name = 'myadmin/products/performance.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # All products with sales data annotated
        products = Product.objects.select_related('category').annotate(
            total_sold=Sum('orderitem__quantity'),
            total_revenue=Sum(F('orderitem__quantity') * F('orderitem__price')),
            order_count=Count('orderitem__order', distinct=True),
            wishlist_count=Count('wishlist', distinct=True),
        ).order_by('-total_sold')

        # Split into top sellers (sold at least 1) and zero sellers
        top_sellers = [p for p in products if p.total_sold]
        zero_sellers = [p for p in products if not p.total_sold]

        # Low performers: sold something but in bottom 20% by quantity
        if top_sellers:
            max_sold = top_sellers[0].total_sold or 1
            low_threshold = max(1, max_sold * 0.2)
            low_performers = [p for p in top_sellers if p.total_sold <= low_threshold]
        else:
            low_performers = []

        # Overall totals
        total_views = sum(p.view_count for p in products)
        total_sold_units = sum(p.total_sold or 0 for p in products)

        # Conversion rate per product (views → purchases)
        for p in products:
            if p.view_count and p.total_sold:
                p.conversion = round((p.total_sold / p.view_count) * 100, 1)
            else:
                p.conversion = 0

        # Most wishlisted
        most_wishlisted = sorted(products, key=lambda p: p.wishlist_count, reverse=True)[:10]

        context.update({
            'top_sellers': top_sellers[:20],
            'zero_sellers': zero_sellers,
            'low_performers': low_performers[:10],
            'most_wishlisted': most_wishlisted,
            'all_products': products,
            'total_views': total_views,
            'total_sold_units': total_sold_units,
            'total_products': products.count(),
            'unavailable_count': products.filter(is_available=False).count(),
        })
        return context


# Customer Insights View
@staff_required
class CustomerInsightsView(TemplateView):
    """Understand buyers: new vs returning, CLV, geography, activity timeline"""
    template_name = 'myadmin/customers/insights.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        import json
        from django.db.models.functions import TruncDate, TruncMonth

        all_orders = Order.objects.filter(
            status__in=['confirmed', 'processing', 'shipped', 'delivered']
        )

        # ── New vs Returning ─────────────────────────────
        # Group by customer_phone (most reliable identifier for WhatsApp orders)
        phone_order_counts = (
            Order.objects
            .values('customer_phone')
            .annotate(order_count=Count('id'))
        )
        new_customers      = sum(1 for c in phone_order_counts if c['order_count'] == 1)
        returning_customers = sum(1 for c in phone_order_counts if c['order_count'] > 1)
        total_unique        = new_customers + returning_customers

        # ── Customer Lifetime Value (CLV) ────────────────
        # Per unique phone: total spend, order count, first/last order
        clv_data = (
            Order.objects
            .values('customer_phone', 'customer_name')
            .annotate(
                total_spent=Sum('total_amount'),
                order_count=Count('id'),
                first_order=Min('created_at'),
                last_order=Max('created_at'),
            )
            .order_by('-total_spent')
        )

        top_customers = list(clv_data[:20])
        avg_clv = (
            Order.objects
            .values('customer_phone')
            .annotate(spent=Sum('total_amount'))
            .aggregate(avg=Avg('spent'))['avg'] or Decimal('0')
        )

        # ── Geographic data ──────────────────────────────
        # Extract city/area from customer_address — use last non-empty line or first word
        from collections import Counter

        def extract_location(address):
            if not address:
                return 'Unknown'
            lines = [l.strip() for l in address.strip().splitlines() if l.strip()]
            if lines:
                # Take last line as most likely city/area
                loc = lines[-1].split(',')[-1].strip()
                return loc if loc else lines[-1]
            return 'Unknown'

        addresses = Order.objects.values_list('customer_address', flat=True)
        location_counter = Counter(extract_location(a) for a in addresses)
        # Top 15 locations
        top_locations = [
            {'location': loc, 'count': cnt}
            for loc, cnt in location_counter.most_common(15)
            if loc and loc != 'Unknown'
        ]
        unknown_count = location_counter.get('Unknown', 0)

        # ── Activity Timeline ────────────────────────────
        # Monthly new unique customers (first order per phone per month)
        # Get first order date per phone
        first_orders = (
            Order.objects
            .values('customer_phone')
            .annotate(first_date=Min('created_at'))
        )
        monthly_new: Counter = Counter()
        for row in first_orders:
            key = row['first_date'].strftime('%Y-%m') if row['first_date'] else None
            if key:
                monthly_new[key] += 1

        # Monthly total orders
        monthly_orders_qs = (
            Order.objects
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(count=Count('id'), revenue=Sum('total_amount'))
            .order_by('month')
        )

        timeline_labels, timeline_new, timeline_total, timeline_revenue = [], [], [], []
        for row in monthly_orders_qs:
            label = row['month'].strftime('%b %Y')
            key   = row['month'].strftime('%Y-%m')
            timeline_labels.append(label)
            timeline_total.append(row['count'])
            timeline_new.append(monthly_new.get(key, 0))
            timeline_revenue.append(float(row['revenue'] or 0))

        # ── Repeat purchase rate ─────────────────────────
        repeat_rate = round(returning_customers / total_unique * 100, 1) if total_unique else 0

        # ── Orders per customer distribution ────────────
        order_freq = Counter(c['order_count'] for c in phone_order_counts)
        freq_labels = [f'{k} order{"s" if k > 1 else ""}' for k in sorted(order_freq)[:8]]
        freq_values = [order_freq[k] for k in sorted(order_freq)[:8]]

        context.update({
            # New vs returning
            'new_customers': new_customers,
            'returning_customers': returning_customers,
            'total_unique': total_unique,
            'repeat_rate': repeat_rate,
            # CLV
            'top_customers': top_customers,
            'avg_clv': avg_clv,
            # Geography
            'top_locations': top_locations,
            'unknown_count': unknown_count,
            # Timeline
            'timeline_labels_json': json.dumps(timeline_labels),
            'timeline_new_json': json.dumps(timeline_new),
            'timeline_total_json': json.dumps(timeline_total),
            'timeline_revenue_json': json.dumps(timeline_revenue),
            # Frequency
            'freq_labels_json': json.dumps(freq_labels),
            'freq_values_json': json.dumps(freq_values),
        })
        return context


@staff_required
class ProductVariantsSaveView(View):
    """Save all variants for a product via AJAX (replaces existing variants)."""

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        try:
            import json
            data = json.loads(request.body)
            variants = data.get('variants', [])

            # Delete all existing variants and recreate
            product.variants.all().delete()
            created = []
            for i, v in enumerate(variants):
                name = v.get('name', '').strip()
                if not name:
                    continue
                try:
                    adj = Decimal(str(v.get('price_adjustment', 0)))
                except Exception:
                    adj = Decimal('0')
                variant = ProductVariant.objects.create(
                    product=product,
                    name=name,
                    price_adjustment=adj,
                    is_available=bool(v.get('is_available', True)),
                    sort_order=i,
                )
                created.append({'id': variant.id, 'name': variant.name,
                                 'price_adjustment': str(variant.price_adjustment),
                                 'is_available': variant.is_available})

            return JsonResponse({'success': True, 'variants': created})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)


@staff_required
class ProductStockUpdateView(View):
    """
    AJAX endpoint to update stock for one or many products.

    Single:  POST { product_id: 5,  stock_quantity: 20 }
    Bulk:    POST { updates: [{product_id: 5, stock_quantity: 20}, ...] }
    Both accept an optional 'mode': 'set' (default) | 'add' | 'subtract'
    """

    def post(self, request):
        import json
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

        mode = data.get('mode', 'set')   # 'set' | 'add' | 'subtract'
        updates = data.get('updates')    # bulk list

        # Normalise to a list of (product_id, qty) pairs
        if updates is None:
            # Single-product shorthand
            product_id = data.get('product_id')
            qty        = data.get('stock_quantity')
            if product_id is None or qty is None:
                return JsonResponse({'success': False, 'error': 'product_id and stock_quantity are required'}, status=400)
            updates = [{'product_id': product_id, 'stock_quantity': qty}]

        results = []
        errors  = []

        for item in updates:
            pid = item.get('product_id')
            qty = item.get('stock_quantity')

            try:
                qty = int(qty)
            except (TypeError, ValueError):
                errors.append({'product_id': pid, 'error': 'Invalid quantity'})
                continue

            try:
                product = Product.objects.get(pk=pid)
            except Product.DoesNotExist:
                errors.append({'product_id': pid, 'error': 'Product not found'})
                continue

            if mode == 'add':
                new_qty = max(0, product.stock_quantity + qty)
            elif mode == 'subtract':
                new_qty = max(0, product.stock_quantity - qty)
            else:                      # 'set'
                new_qty = max(0, qty)

            product.stock_quantity = new_qty
            product.save(update_fields=['stock_quantity'])

            results.append({
                'product_id': product.pk,
                'name': product.name,
                'stock_quantity': new_qty,
                'is_low_stock': product.is_low_stock,
                'is_out_of_stock': product.is_out_of_stock,
            })

        import logging
        logger = logging.getLogger('myadmin')
        logger.info(
            f"User {request.user.username} updated stock for "
            f"{len(results)} product(s) (mode={mode})"
        )

        return JsonResponse({
            'success': True,
            'updated': results,
            'errors': errors,
        })
