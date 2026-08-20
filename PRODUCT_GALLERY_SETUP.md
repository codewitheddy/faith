# Product Gallery Images Setup

## What Was Added

### 1. **ProductGallery Model** (`shop/models.py`)
A new model to manage gallery images for product detail pages with the following fields:

- **product** (ForeignKey) - Links to the Product
- **image** (ImageField) - Upload gallery image to `product_gallery/%Y/%m/`
- **alt_text** (CharField) - Accessibility text for screen readers
- **caption** (CharField, optional) - Description text for the image
- **sort_order** (PositiveSmallIntegerField) - Controls image display order
- **is_featured** (BooleanField) - Mark as featured/hero image
- **created_at** (DateTimeField) - Auto timestamp

### 2. **ProductGalleryAdmin** (`shop/admin.py`)
Standalone admin interface for managing gallery images with:

- **List view**: Shows thumbnails, alt text, sort order, featured status
- **Inline admin**: Also available within the Product admin as `ProductGalleryInline`
- **Bulk actions**: Edit sort order and featured status directly in list
- **Image preview**: Thumbnail display in admin list
- **Search**: Search by product name, alt text, or caption
- **Date hierarchy**: Filter by creation date

### 3. **Product Detail Template** (`shop/templates/product_detail.html`)
Updated to display gallery images:

- **Thumbnail grid**: 4-column grid of gallery images below main image
- **Click to switch**: Click any thumbnail to update the main display image
- **Active highlight**: Selected thumbnail shows gold accent border
- **Responsive**: Grid adjusts for mobile (stacks to 2 columns)
- **Accessibility**: Alt text and captions preserved

### 4. **Database Migration**
Migration `0015_productgallery.py` created and applied successfully.

---

## How to Use in Admin

### Add Gallery Images to a Product

1. **Via Product Admin:**
   - Go to **Products** in the admin
   - Click on a product to edit
   - Scroll down to **Product Gallery Images** inline section
   - Click **Add another Product Gallery Image**
   - Upload image, add alt text, caption, and set sort order
   - Check **Is Featured** if it should be emphasized
   - Save

2. **Via Gallery Admin:**
   - Go to **Product Gallery** in the admin
   - Click **Add Product Gallery Image**
   - Select the product
   - Upload image and fill in details
   - Save

### Manage Existing Images

- **Reorder**: Drag or edit `sort_order` directly in list
- **Mark as Featured**: Check `is_featured` in list view
- **Edit**: Click any image to modify alt text, caption, sort order
- **Delete**: Select and use delete action
- **Search**: Search by product name, alt text, or caption

---

## Frontend Display

Gallery images appear on the product detail page:

- **Below main image**: 4-column thumbnail grid
- **Interactive**: Click any thumbnail to switch main image
- **Mobile responsive**: Collapses to 2 columns on mobile
- **Alt text**: Shown on hover for accessibility
- **Fallback**: If no gallery images exist, only main product image displays

---

## Technical Details

### Model Relationships
```
Product (1) ──── (N) ProductGallery
  ↓
  gallery_images (reverse relation)
```

Access gallery images in templates:
```django
{% for gallery_img in product.gallery_images.all %}
  <img src="{{ gallery_img.image.url }}" alt="{{ gallery_img.alt_text }}">
{% endfor %}
```

### Admin Features

- **Inline within Product**: Add/edit gallery images while editing a product
- **Standalone Gallery Admin**: Bulk upload and manage all gallery images
- **Thumbnail preview**: See small preview of image in list view
- **Sort ordering**: `sort_order` field controls display sequence
- **Featured flag**: Mark special images as featured

### File Storage

Gallery images are stored in:
```
/media/product_gallery/2026/08/image_name.jpg
```

This keeps them organized by year/month for easy management.

---

## Next Steps (Optional)

You can enhance this further with:

1. **Image carousel** - JavaScript slider for thumbnails
2. **Zoom on hover** - Magnifying glass effect on main image
3. **Lightbox** - Full-screen modal view of gallery
4. **Product videos** - Add YouTube/Vimeo videos to gallery
5. **Image optimization** - Automated thumbnail generation
6. **AI captions** - Auto-generate captions from image content

---

## Support

To verify the setup:

1. Go to Django Admin `/myadmin/`
2. Click **Product Gallery** in the left sidebar
3. Try adding a gallery image
4. View a product on the detail page to see the gallery
