from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    short_description = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Option 1: Store image URL (recommended for external images)
    image_url = models.URLField(max_length=500, blank=True, null=True, 
                                help_text="External image URL (e.g., from Unsplash, Imgur)")
    
    # Option 2: Store base64 image data (for small images stored in DB)
    image_base64 = models.TextField(blank=True, null=True,
                                    help_text="Base64 encoded image data")
    
    # Keep the old ImageField for backward compatibility (optional)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    # Sale pricing
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                     help_text="Leave blank if not on sale")
    is_on_sale = models.BooleanField(default=False)

    is_available = models.BooleanField(default=True)
    
    # Inventory management
    stock_quantity = models.PositiveIntegerField(default=0, help_text="Available units in stock")
    reorder_level = models.PositiveIntegerField(default=5, help_text="Minimum stock level before reorder alert")
    
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_image_url(self):
        """Return the appropriate image URL"""
        if self.image_url:
            return self.image_url
        elif self.image_base64:
            return f"data:image/jpeg;base64,{self.image_base64}"
        elif self.image:
            return self.image.url
        return None

    @property
    def effective_price(self):
        """The price customers actually pay."""
        if self.sale_price and self.sale_price < self.price:
            return self.sale_price
        return self.price

    @property
    def discount_percent(self):
        if self.sale_price and self.sale_price < self.price and self.price > 0:
            return int(round((1 - self.sale_price / self.price) * 100))
        return 0

    @property
    def on_sale(self):
        """True if a valid sale price is set (regardless of is_on_sale checkbox)."""
        return bool(self.sale_price and self.sale_price < self.price)

    @property
    def is_low_stock(self):
        """True if stock is at or below reorder level"""
        return self.stock_quantity <= self.reorder_level
    
    @property
    def is_out_of_stock(self):
        """True if product has no stock"""
        return self.stock_quantity == 0
    
    def can_order(self, quantity):
        """Check if requested quantity is available"""
        return self.stock_quantity >= quantity

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    """Optional size/colour/material variants for a product."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=100, help_text="e.g. Gold / Silver / Size S")
    price_adjustment = models.DecimalField(
        max_digits=8, decimal_places=2, default=0,
        help_text="Added to base price (use negative to reduce)"
    )
    is_available = models.BooleanField(default=True)
    stock_quantity = models.PositiveIntegerField(default=0, help_text="Stock for this specific variant")
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'name']

    def __str__(self):
        return f"{self.product.name} — {self.name}"

    @property
    def final_price(self):
        """Variant price. If price_adjustment > 0, it IS the price. If 0, use base."""
        if self.price_adjustment and self.price_adjustment > 0:
            return self.price_adjustment
        return self.product.effective_price


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField(max_length=254, blank=True)
    customer_phone = models.CharField(max_length=20)
    customer_address = models.TextField()
    notes = models.TextField(blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate order number: ORD-YYYYMMDD-XXXX
            from django.utils import timezone
            date_str = timezone.now().strftime('%Y%m%d')
            last_order = Order.objects.filter(order_number__startswith=f'ORD-{date_str}').order_by('-order_number').first()
            if last_order:
                last_num = int(last_order.order_number.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            self.order_number = f'ORD-{date_str}-{new_num:04d}'
        
        # Check if status changed to 'delivered' to send completion email
        if self.pk:  # Only for existing orders (updates, not creation)
            try:
                old_order = Order.objects.get(pk=self.pk)
                if old_order.status != 'delivered' and self.status == 'delivered':
                    # Status just changed to delivered - send completion email
                    from .email_utils import send_order_completion_email
                    send_order_completion_email(self)
            except Order.DoesNotExist:
                pass
        
        super().save(*args, **kwargs)
    
    @property
    def tracking_steps(self):
        steps = [
            ('pending',    'Placed'),
            ('confirmed',  'Confirmed'),
            ('processing', 'Processing'),
            ('shipped',    'Shipped'),
            ('delivered',  'Delivered'),
        ]
        order_index = next((i for i, (s, _) in enumerate(steps) if s == self.status), 0)
        return [
            {
                'key': s,
                'label': label,
                'number': i + 1,
                'is_current': s == self.status,
                'is_done': i < order_index,
            }
            for i, (s, label) in enumerate(steps)
        ]

    def __str__(self):
        return f"{self.order_number} - {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        product_name = self.product.name if self.product else "[Deleted Product]"
        return f"{self.quantity}x {product_name}"
    
    def get_subtotal(self):
        return self.quantity * self.price


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} → {self.product.name}"
