"""
Custom Admin Dashboard for The POPSHOP.KE
Provides statistics, charts, and reports for the admin interface
"""
from django.db.models import Count, Sum, Avg, Min, Max, Q
from django.utils import timezone
from datetime import timedelta
from .models import Product, Category


def get_dashboard_stats():
    """Get comprehensive statistics for the admin dashboard"""
    
    # Basic counts
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    available_products = Product.objects.filter(is_available=True).count()
    unavailable_products = Product.objects.filter(is_available=False).count()
    
    # Time-based statistics
    now = timezone.now()
    thirty_days_ago = now - timedelta(days=30)
    seven_days_ago = now - timedelta(days=7)
    
    products_this_month = Product.objects.filter(created_at__gte=thirty_days_ago).count()
    products_this_week = Product.objects.filter(created_at__gte=seven_days_ago).count()
    
    # Price statistics
    price_stats = Product.objects.aggregate(
        avg_price=Avg('price'),
        min_price=Min('price'),
        max_price=Max('price'),
        total_inventory_value=Sum('price')
    )
    
    # Category statistics
    category_stats = Category.objects.annotate(
        product_count=Count('products'),
        available_count=Count('products', filter=Q(products__is_available=True)),
        avg_price=Avg('products__price')
    ).order_by('-product_count')
    
    # Top categories
    top_categories = category_stats[:5]
    
    # Recent products
    recent_products = Product.objects.select_related('category').order_by('-created_at')[:10]
    
    # Products by availability
    availability_data = {
        'available': available_products,
        'unavailable': unavailable_products
    }
    
    # Products added over time (last 30 days)
    products_by_day = []
    for i in range(30, -1, -1):
        day = now - timedelta(days=i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        count = Product.objects.filter(
            created_at__gte=day_start,
            created_at__lt=day_end
        ).count()
        products_by_day.append({
            'date': day_start.strftime('%Y-%m-%d'),
            'count': count
        })
    
    # Price distribution
    price_ranges = [
        {'label': 'Under Ksh 500', 'min': 0, 'max': 500},
        {'label': 'Ksh 500-1000', 'min': 500, 'max': 1000},
        {'label': 'Ksh 1000-2000', 'min': 1000, 'max': 2000},
        {'label': 'Ksh 2000-5000', 'min': 2000, 'max': 5000},
        {'label': 'Over Ksh 5000', 'min': 5000, 'max': 999999},
    ]
    
    price_distribution = []
    for range_data in price_ranges:
        count = Product.objects.filter(
            price__gte=range_data['min'],
            price__lt=range_data['max']
        ).count()
        price_distribution.append({
            'label': range_data['label'],
            'count': count
        })
    
    return {
        'total_products': total_products,
        'total_categories': total_categories,
        'available_products': available_products,
        'unavailable_products': unavailable_products,
        'products_this_month': products_this_month,
        'products_this_week': products_this_week,
        'avg_price': price_stats['avg_price'] or 0,
        'min_price': price_stats['min_price'] or 0,
        'max_price': price_stats['max_price'] or 0,
        'total_inventory_value': price_stats['total_inventory_value'] or 0,
        'category_stats': category_stats,
        'top_categories': top_categories,
        'recent_products': recent_products,
        'availability_data': availability_data,
        'products_by_day': products_by_day,
        'price_distribution': price_distribution,
    }


def get_category_chart_data():
    """Get data for category distribution chart"""
    categories = Category.objects.annotate(
        product_count=Count('products')
    ).order_by('-product_count')[:10]
    
    return {
        'labels': [cat.name for cat in categories],
        'data': [cat.product_count for cat in categories]
    }


def get_price_trend_data():
    """Get average price trend over time"""
    now = timezone.now()
    months_data = []
    
    for i in range(6, -1, -1):
        month_start = (now - timedelta(days=30*i)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if i > 0:
            month_end = (now - timedelta(days=30*(i-1))).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            month_end = now
        
        avg_price = Product.objects.filter(
            created_at__gte=month_start,
            created_at__lt=month_end
        ).aggregate(avg=Avg('price'))['avg'] or 0
        
        months_data.append({
            'month': month_start.strftime('%b %Y'),
            'avg_price': float(avg_price)
        })
    
    return months_data


def get_inventory_alerts():
    """Get alerts for inventory management"""
    alerts = []
    
    # Categories with no products
    empty_categories = Category.objects.annotate(
        product_count=Count('products')
    ).filter(product_count=0)
    
    for cat in empty_categories:
        alerts.append({
            'type': 'warning',
            'message': f'Category "{cat.name}" has no products',
            'action': 'Add products to this category'
        })
    
    # Unavailable products
    unavailable_count = Product.objects.filter(is_available=False).count()
    if unavailable_count > 0:
        alerts.append({
            'type': 'info',
            'message': f'{unavailable_count} product(s) marked as unavailable',
            'action': 'Review unavailable products'
        })
    
    # Products without images
    no_image_count = Product.objects.filter(Q(image='') | Q(image__isnull=True)).count()
    if no_image_count > 0:
        alerts.append({
            'type': 'warning',
            'message': f'{no_image_count} product(s) without images',
            'action': 'Upload product images'
        })
    
    return alerts
