"""
Management command to convert existing product images to base64 format
Usage: python manage.py convert_images_to_base64
"""
import base64
from django.core.management.base import BaseCommand
from shop.models import Product


class Command(BaseCommand):
    help = 'Convert existing product images to base64 format'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be converted without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        products = Product.objects.filter(image__isnull=False).exclude(image='')
        total = products.count()
        
        if total == 0:
            self.stdout.write(self.style.WARNING('No products with uploaded images found.'))
            return
        
        self.stdout.write(f'Found {total} products with uploaded images.')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        converted = 0
        skipped = 0
        errors = 0
        
        for product in products:
            try:
                # Check if already has base64 or URL
                if product.image_base64 or product.image_url:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Skipping {product.name} - already has base64/URL'
                        )
                    )
                    skipped += 1
                    continue
                
                # Read and encode the image
                with product.image.open('rb') as image_file:
                    image_data = image_file.read()
                    base64_data = base64.b64encode(image_data).decode('utf-8')
                    
                    # Check size (warn if > 500KB)
                    size_kb = len(base64_data) / 1024
                    if size_kb > 500:
                        self.stdout.write(
                            self.style.WARNING(
                                f'Warning: {product.name} image is {size_kb:.1f}KB (large)'
                            )
                        )
                    
                    if not dry_run:
                        product.image_base64 = base64_data
                        product.save()
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Converted {product.name} ({size_kb:.1f}KB)'
                        )
                    )
                    converted += 1
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Error converting {product.name}: {str(e)}'
                    )
                )
                errors += 1
        
        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'Converted: {converted}'))
        self.stdout.write(self.style.WARNING(f'Skipped: {skipped}'))
        if errors > 0:
            self.stdout.write(self.style.ERROR(f'Errors: {errors}'))
        
        if dry_run:
            self.stdout.write('\nRun without --dry-run to apply changes')
