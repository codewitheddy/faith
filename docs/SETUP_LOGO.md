# 🎨 Logo Setup Guide

## Quick Steps

1. **Save your logo image** (the one you provided) to:
   ```
   static/images/logo.png
   ```

2. **Recommended specifications:**
   - Format: PNG (transparent background preferred)
   - Dimensions: 400-600px width × 100-150px height
   - File size: Under 200KB for optimal loading

3. **The logo will automatically:**
   - Display at 50px height on desktop
   - Scale to 40px height on mobile
   - Have a subtle hover effect (scale 1.05)
   - Link back to homepage when clicked

## Alternative: Use a Different Image

If you want to use a different logo file name or format:

1. Save your logo in `static/images/` with any name
2. Update line in `shop/templates/home.html`:
   ```html
   <img src="{% static 'images/YOUR_LOGO_NAME.png' %}" alt="The POPSHOP.KE" class="logo">
   ```

## Navigation Bar Features

✅ Fixed position (stays at top while scrolling)
✅ Transparent background with blur effect
✅ Shadow increases on scroll
✅ Responsive mobile menu (hamburger icon)
✅ Cart icon with live count
✅ Smooth hover animations on links

## Testing

After adding the logo:
1. Run: `python manage.py runserver`
2. Visit: http://127.0.0.1:8000/
3. Check that logo appears in navigation bar
4. Test mobile view (resize browser or use dev tools)
5. Verify logo links back to homepage

## Troubleshooting

**Logo not showing?**
- Ensure file is named exactly `logo.png`
- Check file is in `static/images/` directory
- Clear browser cache (Ctrl+Shift+R)
- Verify file permissions

**Logo too large/small?**
- Adjust the `.logo` height in CSS (currently 50px)
- Or resize your image file before uploading
