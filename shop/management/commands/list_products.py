from django.core.management.base import BaseCommand
from shop.models import Category, Product

class Command(BaseCommand):
    help = 'Lists all products in the database'

    def handle(self, *args, **kwargs):
        categories = Category.objects.all()
        
        self.stdout.write(self.style.SUCCESS('\n=== PRODUCT INVENTORY ===\n'))
        
        for category in categories:
            products = category.products.filter(is_available=True)
            self.stdout.write(self.style.WARNING(f'\n{category.name.upper()} ({products.count()} products)'))
            self.stdout.write('-' * 60)
            
            for product in products:
                has_image = '📷' if product.image else '❌'
                self.stdout.write(f'{has_image} {product.name}')
                self.stdout.write(f'   Price: Ksh {product.price:,.2f}')
                self.stdout.write(f'   {product.short_description}')
                self.stdout.write('')
        
        total_products = Product.objects.filter(is_available=True).count()
        total_categories = categories.count()
        
        self.stdout.write(self.style.SUCCESS(f'\nTotal: {total_categories} categories, {total_products} products'))
        self.stdout.write(self.style.WARNING('\n📷 = Has image | ❌ = No image\n'))
