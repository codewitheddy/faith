from django.contrib import admin
from django.db.models import Avg, Sum, Count
from django.template.response import TemplateResponse
from .models import Category, Product

# Customize admin site headers
admin.site.site_header = "POPSHOP ADMIN"
admin.site.site_title = "POPSHOP Admin Portal"
admin.site.index_title = "Welcome to POPSHOP Administration"


# Context processor for sidebar counts
def get_sidebar_context():
    """Get counts for sidebar badges"""
    return {
        'total_products': Product.objects.count(),
        'total_categories': Category.objects.count(),
    }


# Custom admin index view with analytics
def admin_index(request):
    # Get statistics
    total_products = Product.objects.count()
    available_products = Product.objects.filter(is_available=True).count()
    total_categories = Category.objects.count()
    
    # Calculate average price and total value
    stats = Product.objects.filter(is_available=True).aggregate(
        avg_price=Avg('price'),
        total_value=Sum('price')
    )
    avg_price = stats['avg_price'] or 0
    total_value = stats['total_value'] or 0
    
    # Category breakdown
    category_stats = []
    categories = Category.objects.annotate(product_count=Count('products'))
    for category in categories:
        if total_products > 0:
            percentage = (category.product_count / total_products) * 100
        else:
            percentage = 0
        category_stats.append({
            'name': category.name,
            'count': category.product_count,
            'percentage': percentage
        })
    
    # Sort by count descending
    category_stats.sort(key=lambda x: x['count'], reverse=True)
    
    # Recent products
    recent_products = Product.objects.order_by('-created_at')[:5]
    
    context = {
        'total_products': total_products,
        'available_products': available_products,
        'total_categories': total_categories,
        'avg_price': avg_price,
        'total_value': total_value,
        'category_stats': category_stats,
        'recent_products': recent_products,
    }
    
    # Get the default admin index context
    from django.contrib.admin.sites import site
    context.update(site.each_context(request))
    
    return TemplateResponse(request, 'admin/index.html', context)


# Override the admin index view
admin.site.index = admin_index


# Add context processor to all admin views
from django.contrib.admin import AdminSite

original_each_context = AdminSite.each_context

def custom_each_context(self, request):
    context = original_each_context(self, request)
    context.update(get_sidebar_context())
    return context

AdminSite.each_context = custom_each_context


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'product_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'created_at']
    list_filter = ['category', 'is_available', 'created_at']
    list_editable = ['is_available', 'price']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description', 'short_description']
    date_hierarchy = 'created_at'
    list_per_page = 20
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category')
        }),
        ('Description', {
            'fields': ('short_description', 'description')
        }),
        ('Pricing & Availability', {
            'fields': ('price', 'is_available')
        }),
        ('Media', {
            'fields': ('image',),
            'description': 'Upload product image (recommended: square images, min 800x800px)'
        }),
    )
    
    actions = ['make_available', 'make_unavailable']
    
    def make_available(self, request, queryset):
        updated = queryset.update(is_available=True)
        self.message_user(request, f'{updated} product(s) marked as available.')
    make_available.short_description = 'Mark selected products as available'
    
    def make_unavailable(self, request, queryset):
        updated = queryset.update(is_available=False)
        self.message_user(request, f'{updated} product(s) marked as unavailable.')
    make_unavailable.short_description = 'Mark selected products as unavailable'
