from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductVariant, Order, OrderItem, UserProfile, Wishlist, HeroSlide

# Customize admin site headers
admin.site.site_header = "WYATT COLLECTION ADMIN"
admin.site.site_title = "Wyatt Collection Admin"
admin.site.index_title = "Welcome to Wyatt Collection Administration"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'product_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ['name', 'price_adjustment', 'is_available', 'sort_order']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'sale_price', 'is_on_sale', 'is_available', 'created_at']
    list_editable = ['is_available', 'price', 'is_on_sale']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description', 'short_description']
    date_hierarchy = 'created_at'
    list_per_page = 20
    inlines = [ProductVariantInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category')
        }),
        ('Description', {
            'fields': ('short_description', 'description')
        }),
        ('Pricing & Availability', {
            'fields': ('price', 'sale_price', 'is_on_sale', 'is_available')
        }),
        ('Inventory Management', {
            'fields': ('stock_quantity', 'reorder_level'),
            'description': 'Set available stock and low-stock alert threshold'
        }),
        ('Media', {
            'fields': ('image_url', 'image_base64', 'image'),
            'description': 'Choose one option: 1) External URL (recommended), 2) Base64 data, or 3) Upload file'
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


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ['product', 'quantity', 'price', 'get_subtotal']
    readonly_fields = ['get_subtotal']
    
    def get_subtotal(self, obj):
        if obj.id:
            return f'Ksh {obj.get_subtotal():,.2f}'
        return '-'
    get_subtotal.short_description = 'Subtotal'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer_name', 'customer_phone', 'status', 'total_amount', 'created_at']
    search_fields = ['order_number', 'customer_name', 'customer_phone']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    list_per_page = 20
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'status', 'total_amount')
        }),
        ('Customer Details', {
            'fields': ('customer_name', 'customer_phone', 'customer_address', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_confirmed', 'mark_processing', 'mark_shipped', 'mark_delivered']
    
    def mark_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} order(s) marked as confirmed.')
    mark_confirmed.short_description = 'Mark as Confirmed'
    
    def mark_processing(self, request, queryset):
        updated = queryset.update(status='processing')
        self.message_user(request, f'{updated} order(s) marked as processing.')
    mark_processing.short_description = 'Mark as Processing'
    
    def mark_shipped(self, request, queryset):
        updated = queryset.update(status='shipped')
        self.message_user(request, f'{updated} order(s) marked as shipped.')
    mark_shipped.short_description = 'Mark as Shipped'
    
    def mark_delivered(self, request, queryset):
        updated = queryset.update(status='delivered')
        self.message_user(request, f'{updated} order(s) marked as delivered.')
    mark_delivered.short_description = 'Mark as Delivered'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city', 'created_at']
    search_fields = ['user__username', 'phone', 'city']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'added_at']
    search_fields = ['user__username', 'product__name']


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'price_adjustment', 'is_available', 'sort_order']
    list_editable = ['price_adjustment', 'is_available', 'sort_order']
    search_fields = ['product__name', 'name']


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display  = ['order', 'slide_preview', 'badge_text', 'theme', 'has_image', 'is_active']
    list_editable = ['order', 'is_active']
    list_display_links = ['slide_preview']
    ordering      = ['order']
    list_per_page = 20

    fieldsets = (
        ('Content', {
            'description': (
                'To highlight one word in the title, wrap it in double asterisks: '
                'e.g. <code>Refined **Style** for Men</code>'
            ),
            'fields': ('badge_text', 'title', 'subtitle'),
        }),
        ('Stats Row', {
            'description': 'Three figures shown below the subtitle.',
            'fields': (
                ('stat1_number', 'stat1_label'),
                ('stat2_number', 'stat2_label'),
                ('stat3_number', 'stat3_label'),
            ),
        }),
        ('Call-to-Action Buttons', {
            'fields': (
                ('btn1_text', 'btn1_url'),
                ('btn2_text', 'btn2_url'),
            ),
        }),
        ('Circle Visual', {
            'description': (
                'Paste a direct image URL to show a photo in the circle. '
                'Leave blank to show the emoji instead.'
            ),
            'fields': ('image_url', 'circle_emoji', 'badge1_text', 'badge2_text'),
        }),
        ('Background & Theme', {
            'fields': ('theme', 'bg_color'),
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active'),
        }),
    )

    # ── Custom list columns ──────────────────────────────────

    def slide_preview(self, obj):
        before, highlight, after = obj.get_title_parts()
        if highlight:
            return format_html(
                '{}<span style="color:#C9A84C;font-weight:700;"> {} </span>{}',
                before, highlight, after
            )
        return obj.title
    slide_preview.short_description = 'Title'

    def has_image(self, obj):
        if obj.image_url:
            return format_html(
                '<img src="{}" style="height:40px;width:40px;object-fit:cover;'
                'border-radius:50%;border:2px solid #C9A84C;">',
                obj.image_url
            )
        return format_html(
            '<span style="font-size:1.5rem;opacity:0.5;">{}</span>',
            obj.circle_emoji or '👔'
        )
    has_image.short_description = 'Image'
