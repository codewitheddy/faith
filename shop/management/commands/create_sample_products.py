from django.core.management.base import BaseCommand
from shop.models import Category, Product
from django.core.files.base import ContentFile
import requests
from io import BytesIO

class Command(BaseCommand):
    help = 'Creates sample products for the jewellery store'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample categories and products...')

        # Clear existing data
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Create Categories
        categories_data = [
            {'name': 'Necklaces', 'slug': 'necklaces'},
            {'name': 'Earrings', 'slug': 'earrings'},
            {'name': 'Bracelets', 'slug': 'bracelets'},
            {'name': 'Rings', 'slug': 'rings'},
            {'name': 'Anklets', 'slug': 'anklets'},
        ]

        categories = {}
        for cat_data in categories_data:
            category = Category.objects.create(**cat_data)
            categories[cat_data['slug']] = category
            self.stdout.write(f'Created category: {category.name}')

        # Sample Products Data
        products_data = [
            # Necklaces
            {
                'name': 'Rose Gold Heart Pendant',
                'category': 'necklaces',
                'short_description': 'Delicate rose gold heart necklace',
                'description': 'A beautiful rose gold plated heart pendant on a delicate chain. Perfect for everyday wear or special occasions. Hypoallergenic and tarnish-resistant.',
                'price': 2500.00,
            },
            {
                'name': 'Pearl Strand Necklace',
                'category': 'necklaces',
                'short_description': 'Classic freshwater pearl necklace',
                'description': 'Elegant freshwater pearl necklace with sterling silver clasp. Each pearl is hand-selected for quality and luster. A timeless piece for any wardrobe.',
                'price': 4500.00,
            },
            {
                'name': 'Crystal Choker',
                'category': 'necklaces',
                'short_description': 'Sparkling crystal choker necklace',
                'description': 'Modern choker featuring brilliant cut crystals. Adjustable length for perfect fit. Makes a statement at any event.',
                'price': 3200.00,
            },
            
            # Earrings
            {
                'name': 'Diamond Stud Earrings',
                'category': 'earrings',
                'short_description': 'Classic cubic zirconia studs',
                'description': 'Timeless stud earrings featuring brilliant cubic zirconia stones in sterling silver settings. Perfect for daily wear or special occasions.',
                'price': 1800.00,
            },
            {
                'name': 'Hoop Earrings Set',
                'category': 'earrings',
                'short_description': 'Gold-plated hoop earrings',
                'description': 'Set of three different sized hoop earrings in 18k gold plating. Lightweight and comfortable for all-day wear.',
                'price': 2200.00,
            },
            {
                'name': 'Pearl Drop Earrings',
                'category': 'earrings',
                'short_description': 'Elegant pearl dangle earrings',
                'description': 'Sophisticated drop earrings with freshwater pearls. Sterling silver hooks. Perfect for formal events and weddings.',
                'price': 2800.00,
            },
            {
                'name': 'Crystal Chandelier Earrings',
                'category': 'earrings',
                'short_description': 'Statement crystal earrings',
                'description': 'Glamorous chandelier earrings adorned with sparkling crystals. Make a bold statement at any special occasion.',
                'price': 3500.00,
            },
            
            # Bracelets
            {
                'name': 'Tennis Bracelet',
                'category': 'bracelets',
                'short_description': 'Classic crystal tennis bracelet',
                'description': 'Elegant tennis bracelet featuring a continuous line of brilliant crystals. Adjustable clasp for perfect fit. A must-have accessory.',
                'price': 3800.00,
            },
            {
                'name': 'Charm Bracelet',
                'category': 'bracelets',
                'short_description': 'Silver charm bracelet with charms',
                'description': 'Sterling silver charm bracelet with five beautiful charms. Add more charms to personalize your style.',
                'price': 2900.00,
            },
            {
                'name': 'Beaded Bracelet Set',
                'category': 'bracelets',
                'short_description': 'Colorful beaded bracelet stack',
                'description': 'Set of four stackable beaded bracelets in complementary colors. Mix and match for your perfect look.',
                'price': 1500.00,
            },
            {
                'name': 'Gold Bangle',
                'category': 'bracelets',
                'short_description': 'Elegant gold-plated bangle',
                'description': 'Sophisticated gold-plated bangle with intricate engraving. Perfect for layering or wearing alone.',
                'price': 3200.00,
            },
            
            # Rings
            {
                'name': 'Solitaire Ring',
                'category': 'rings',
                'short_description': 'Classic solitaire engagement ring',
                'description': 'Timeless solitaire ring with brilliant cubic zirconia stone. Sterling silver band. Perfect for engagements or special gifts.',
                'price': 4200.00,
            },
            {
                'name': 'Stackable Ring Set',
                'category': 'rings',
                'short_description': 'Set of 5 stackable rings',
                'description': 'Versatile set of five thin stackable rings in mixed metals. Wear together or separately for different looks.',
                'price': 2400.00,
            },
            {
                'name': 'Rose Gold Band',
                'category': 'rings',
                'short_description': 'Simple rose gold band ring',
                'description': 'Elegant rose gold plated band ring. Perfect for everyday wear or as a wedding band. Comfortable fit.',
                'price': 1800.00,
            },
            {
                'name': 'Cocktail Ring',
                'category': 'rings',
                'short_description': 'Statement crystal cocktail ring',
                'description': 'Bold cocktail ring featuring a large crystal stone surrounded by smaller accent stones. Perfect for parties and events.',
                'price': 3600.00,
            },
            
            # Anklets
            {
                'name': 'Beach Anklet',
                'category': 'anklets',
                'short_description': 'Delicate chain anklet',
                'description': 'Simple and elegant chain anklet perfect for beach days and summer outfits. Adjustable length.',
                'price': 1200.00,
            },
            {
                'name': 'Charm Anklet',
                'category': 'anklets',
                'short_description': 'Anklet with shell charms',
                'description': 'Bohemian-style anklet featuring shell and starfish charms. Perfect for vacation and casual wear.',
                'price': 1600.00,
            },
            {
                'name': 'Beaded Anklet',
                'category': 'anklets',
                'short_description': 'Colorful beaded anklet',
                'description': 'Handcrafted beaded anklet with vibrant colors. Adjustable tie closure. Great for layering.',
                'price': 900.00,
            },
        ]

        # Create Products
        for product_data in products_data:
            category_slug = product_data.pop('category')
            product = Product.objects.create(
                category=categories[category_slug],
                is_available=True,
                **product_data
            )
            self.stdout.write(f'Created product: {product.name}')

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully created {len(categories_data)} categories and {len(products_data)} products!'))
        self.stdout.write(self.style.WARNING('\nNote: Products created without images. You can add images through the admin panel.'))
