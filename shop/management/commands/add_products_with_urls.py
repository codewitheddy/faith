"""
Management command to add sample products using external image URLs
Usage: python manage.py add_products_with_urls
"""
from django.core.management.base import BaseCommand
from shop.models import Product, Category


class Command(BaseCommand):
    help = 'Add sample products using external image URLs (Unsplash)'

    def handle(self, *args, **options):
        # Sample jewelry images from Unsplash
        sample_products = [
            {
                'name': 'Diamond Solitaire Ring',
                'category': 'Rings',
                'short_description': 'Classic diamond engagement ring',
                'description': 'Timeless solitaire ring featuring a brilliant-cut diamond set in platinum. Perfect for engagements and special occasions.',
                'price': 45000,
                'image_url': 'https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=800&q=80'
            },
            {
                'name': 'Pearl Drop Earrings',
                'category': 'Earrings',
                'short_description': 'Elegant freshwater pearl earrings',
                'description': 'Beautiful freshwater pearl drop earrings with sterling silver hooks. Adds sophistication to any outfit.',
                'price': 8500,
                'image_url': 'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=800&q=80'
            },
            {
                'name': 'Gold Chain Necklace',
                'category': 'Necklaces',
                'short_description': '18K gold chain necklace',
                'description': 'Delicate 18K gold chain necklace, perfect for layering or wearing alone. Adjustable length.',
                'price': 15000,
                'image_url': 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=800&q=80'
            },
            {
                'name': 'Tennis Bracelet',
                'category': 'Bracelets',
                'short_description': 'Classic diamond tennis bracelet',
                'description': 'Stunning tennis bracelet with round brilliant diamonds set in white gold. A timeless piece.',
                'price': 35000,
                'image_url': 'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=800&q=80'
            },
            {
                'name': 'Sapphire Pendant',
                'category': 'Necklaces',
                'short_description': 'Blue sapphire pendant necklace',
                'description': 'Exquisite blue sapphire pendant surrounded by diamonds, set in white gold with matching chain.',
                'price': 28000,
                'image_url': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=800&q=80'
            },
            {
                'name': 'Rose Gold Bangle',
                'category': 'Bracelets',
                'short_description': 'Modern rose gold bangle',
                'description': 'Contemporary rose gold bangle with minimalist design. Perfect for everyday wear.',
                'price': 12000,
                'image_url': 'https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=800&q=80'
            },
        ]
        
        created = 0
        skipped = 0
        
        for product_data in sample_products:
            # Get or create category
            category_name = product_data.pop('category')
            category, _ = Category.objects.get_or_create(name=category_name)
            
            # Check if product already exists
            if Product.objects.filter(name=product_data['name']).exists():
                self.stdout.write(
                    self.style.WARNING(f'Skipping {product_data["name"]} - already exists')
                )
                skipped += 1
                continue
            
            # Create product
            product = Product.objects.create(
                category=category,
                **product_data
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'Created: {product.name} with external URL')
            )
            created += 1
        
        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'Created: {created} products'))
        if skipped > 0:
            self.stdout.write(self.style.WARNING(f'Skipped: {skipped} products'))
        self.stdout.write('\nAll products use external image URLs from Unsplash')
