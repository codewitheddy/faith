from django.core.management.base import BaseCommand
from shop.models import Category, Product

class Command(BaseCommand):
    help = 'Adds more sample products to demonstrate pagination'

    def handle(self, *args, **kwargs):
        self.stdout.write('Adding more sample products...')

        categories = {
            'necklaces': Category.objects.get(slug='necklaces'),
            'earrings': Category.objects.get(slug='earrings'),
            'bracelets': Category.objects.get(slug='bracelets'),
            'rings': Category.objects.get(slug='rings'),
            'anklets': Category.objects.get(slug='anklets'),
        }

        # Additional Products
        additional_products = [
            # More Necklaces
            {
                'name': 'Infinity Pendant Necklace',
                'category': 'necklaces',
                'short_description': 'Elegant infinity symbol necklace',
                'description': 'Beautiful infinity pendant symbolizing eternal love. Sterling silver chain with cubic zirconia accents. Perfect gift for someone special.',
                'price': 2800.00,
            },
            {
                'name': 'Layered Chain Necklace',
                'category': 'necklaces',
                'short_description': 'Trendy multi-layer necklace',
                'description': 'Modern layered necklace with three delicate chains. Gold-plated finish. Adjustable length for versatile styling.',
                'price': 3400.00,
            },
            
            # More Earrings
            {
                'name': 'Teardrop Earrings',
                'category': 'earrings',
                'short_description': 'Elegant teardrop crystal earrings',
                'description': 'Stunning teardrop-shaped earrings with brilliant crystals. Perfect for weddings and formal events. Lightweight and comfortable.',
                'price': 2600.00,
            },
            {
                'name': 'Geometric Stud Set',
                'category': 'earrings',
                'short_description': 'Modern geometric earring set',
                'description': 'Set of three pairs of geometric stud earrings. Mix and match for different looks. Hypoallergenic posts.',
                'price': 1900.00,
            },
            
            # More Bracelets
            {
                'name': 'Leather Wrap Bracelet',
                'category': 'bracelets',
                'short_description': 'Bohemian leather bracelet',
                'description': 'Stylish leather wrap bracelet with metal accents. Adjustable fit. Perfect for casual and boho styles.',
                'price': 1800.00,
            },
            {
                'name': 'Crystal Link Bracelet',
                'category': 'bracelets',
                'short_description': 'Sparkling crystal link bracelet',
                'description': 'Elegant bracelet featuring crystal-studded links. Secure clasp closure. Adds sparkle to any outfit.',
                'price': 3600.00,
            },
            
            # More Rings
            {
                'name': 'Eternity Band',
                'category': 'rings',
                'short_description': 'Classic eternity ring',
                'description': 'Timeless eternity band with continuous row of crystals. Sterling silver setting. Symbol of everlasting love.',
                'price': 3800.00,
            },
            {
                'name': 'Adjustable Midi Ring Set',
                'category': 'rings',
                'short_description': 'Set of 3 adjustable midi rings',
                'description': 'Trendy midi ring set with adjustable sizing. Mix of plain and crystal designs. Perfect for stacking.',
                'price': 1600.00,
            },
            
            # More Anklets
            {
                'name': 'Double Chain Anklet',
                'category': 'anklets',
                'short_description': 'Layered double chain anklet',
                'description': 'Chic double-strand anklet with delicate chains. Gold-plated finish. Adjustable length for perfect fit.',
                'price': 1400.00,
            },
            {
                'name': 'Crystal Charm Anklet',
                'category': 'anklets',
                'short_description': 'Anklet with crystal charms',
                'description': 'Elegant anklet featuring sparkling crystal charms. Perfect for special occasions. Comfortable all-day wear.',
                'price': 1800.00,
            },
        ]

        count = 0
        for product_data in additional_products:
            category_slug = product_data.pop('category')
            product = Product.objects.create(
                category=categories[category_slug],
                is_available=True,
                **product_data
            )
            count += 1
            self.stdout.write(f'Created: {product.name}')

        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully added {count} more products!'))
        
        total = Product.objects.filter(is_available=True).count()
        self.stdout.write(self.style.SUCCESS(f'📊 Total products now: {total}'))
        
        if total > 12:
            self.stdout.write(self.style.WARNING(f'🎉 Pagination will now be visible (showing 12 per page)'))
