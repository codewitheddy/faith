from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
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
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
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
    
    is_available = models.BooleanField(default=True)
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
    
    def __str__(self):
        return self.name
