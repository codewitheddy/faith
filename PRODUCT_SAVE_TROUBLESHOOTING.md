# Product Save Troubleshooting Guide

## Why Products May Not Save

If you add a product but it doesn't save, here are the most common reasons and how to fix them:

### 1. **Duplicate Product Name** ⚠️
**Problem:** You tried to add a product with a name that already exists  
**Solution:** Use a unique product name. Check existing products first or modify the name slightly (e.g., "Gold Ring" → "Gold Ring - Premium")  
**Where to check:** Admin → Products → List

### 2. **Missing Required Fields**
**Problem:** One or more required fields were left blank:
- **Product Name** - Must be at least 3 characters
- **Category** - Must select a category from the dropdown
- **Price** - Must enter a price in KES
- **Short Description** - Cannot be empty
- **Full Description** - Cannot be empty

**Solution:** Fill in all required fields before clicking "Save Product"  
**Visual indicator:** Fields with a red asterisk (*) are required

### 3. **Invalid Price**
**Problem:** Price validation failed because:
- Price is blank or zero
- Price is negative
- Price exceeds 999,999.99
- Price has more than 2 decimal places (e.g., 10.999)

**Solution:** Enter a valid price with max 2 decimal places (e.g., 5000.00, 299.99)

### 4. **Image File Issues**
**Problem:** Image upload failed because:
- File is corrupted or invalid
- File is larger than 5MB
- File format is not supported (only JPEG, PNG, WebP allowed)
- GIF, BMP, TIFF and other formats are rejected

**Solution:** 
- Use JPEG, PNG, or WebP format
- Compress image if larger than 5MB
- Or provide an image URL instead (paste the link in "Or Image URL" field)

### 5. **Category Not Selected**
**Problem:** You didn't select a category from the dropdown  
**Solution:** Click the Category dropdown and select a category. If no categories exist, create one first (Admin → Categories → Add)

### 6. **Database Connection Issue** (rare)
**Problem:** Database connection dropped or locked  
**Symptom:** Timeout or generic error message  
**Solution:** 
- Wait a moment and try again
- Refresh the page and try again
- Check server logs if problem persists

---

## How to Add a Product Successfully

### Step-by-Step:

1. **Navigate to Admin Panel**
   - Go to Admin → Products → Add Product

2. **Fill Basic Info**
   - Product Name: Use a unique, descriptive name (min 3 characters)
   - Category: Select from dropdown
   - Price (KES): Enter the price (e.g., 5000.00)
   - Sale Price (KES): Optional - only fill if product is on sale
   - Short Description: Brief text shown on product cards (max 150 characters)
   - Full Description: Detailed description with features, materials, etc.

3. **Add Product Image** (Choose one):
   - **Upload Image:** Click "Choose File" and select a JPEG, PNG, or WebP image (max 5MB)
   - **Or Image URL:** Paste a link to an external image
   - **Or Base64:** Paste base64-encoded image data (advanced)

4. **Add Variants** (Optional):
   - Click "+ Add Variant" to add size, color, or material options
   - Enter variant name and price adjustment
   - Check "Available" if variant is in stock

5. **Set Availability** (Sidebar):
   - Check "Available for purchase" if product should be sold
   - Uncheck to hide from customers

6. **Save Product**
   - Click "Save Product" button

7. **Check Success**
   - You should see a green success message
   - Redirected to product list
   - Product appears in the list

---

## Error Messages & Solutions

| Error Message | Cause | Solution |
|---|---|---|
| "Product name must be at least 3 characters long" | Name too short | Use a name with at least 3 characters |
| "A product named [name] already exists" | Duplicate name | Use a different, unique product name |
| "Price is required" | Price field blank | Enter a price in KES |
| "Price must be non-negative" | Negative price | Enter a positive price |
| "Price exceeds maximum value (999,999.99)" | Price too high | Use a price under 999,999.99 |
| "Image file size cannot exceed 5MB" | File too large | Use a smaller image or compress it |
| "Invalid image format" | Wrong file type | Use JPEG, PNG, or WebP only |
| "Invalid or corrupted image file" | Bad image file | Try a different image or re-save/export it |
| "Please correct the errors below" | Multiple validation errors | Check all fields for errors (red text) |

---

## Quick Checklist Before Saving

- [ ] Product name is unique and at least 3 characters
- [ ] Category is selected
- [ ] Price is entered (format: 0000.00)
- [ ] Short description is filled in
- [ ] Full description is filled in
- [ ] At least one image source is provided (upload, URL, or base64)
- [ ] No error messages in red text
- [ ] If on sale: Sale Price is less than regular Price

---

## Still Having Issues?

1. **Check the error message** - Read any red error text carefully
2. **Refresh the page** - Sometimes browser caches issues
3. **Try a different product name** - In case of hidden duplicates
4. **Try without variants first** - Add product, then add variants after
5. **Use an image URL instead** - If file upload is problematic
6. **Check browser console** - Press F12 and look for JavaScript errors (red messages)

---

## Recent Improvements

✅ Form now displays all validation errors clearly  
✅ Better error messages for duplicate product names  
✅ Variant creation errors are now logged for debugging  
✅ Required fields are marked with asterisk (*)
