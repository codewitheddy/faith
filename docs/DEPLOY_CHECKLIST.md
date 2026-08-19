# Deployment Checklist - Image Storage Update

## Pre-Deployment Checklist ✅

- [x] Database migrations created
- [x] Database migrations tested locally
- [x] Product model updated with new fields
- [x] Admin interface updated
- [x] Template updated to use get_image_url()
- [x] Management commands created and tested
- [x] Sample products added with external URLs
- [x] Local testing completed successfully
- [x] Documentation created
- [x] Changes committed to git

## Deployment Commands

### Step 1: Push to Heroku
```bash
git push heroku main
```

### Step 2: Run Migrations
```bash
heroku run python manage.py migrate
```

### Step 3: Verify Deployment
```bash
# Check if app is running
heroku ps

# Check logs for errors
heroku logs --tail
```

### Step 4: Add Sample Products (Optional)
```bash
heroku run python manage.py add_products_with_urls
```

### Step 5: Test the Site
Visit: https://popshop-b0a78a8569b1.herokuapp.com/

Check:
- [ ] Homepage loads
- [ ] Products display with images
- [ ] Admin accessible
- [ ] Can add new product with URL
- [ ] Images load correctly

## Post-Deployment Verification

### Test Admin
1. Go to: https://popshop-b0a78a8569b1.herokuapp.com/admin/
2. Login: admin / PopShop2024!
3. Go to Products → Add Product
4. Test adding product with external URL:
   - Name: Test Product
   - Category: Rings
   - Short description: Test description
   - Description: Test full description
   - Price: 1000
   - Image URL: https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=800&q=80
5. Save and view on homepage

### Test Frontend
1. Visit homepage
2. Check if new products show images
3. Click on product to view modal
4. Verify image displays correctly
5. Test on mobile view

## Rollback Plan (If Needed)

If something goes wrong:

```bash
# Rollback to previous release
heroku rollback

# Or rollback migrations
heroku run python manage.py migrate shop 0001
```

## Optional: Remove Cloudinary

If you want to fully remove Cloudinary after confirming everything works:

### Step 1: Update requirements.txt
Remove these lines:
```
cloudinary==1.41.0
django-cloudinary-storage==0.3.0
```

### Step 2: Update settings.py
Remove from INSTALLED_APPS:
```python
'cloudinary_storage',
'cloudinary',
```

Remove Cloudinary configuration:
```python
CLOUDINARY_STORAGE = {...}
```

### Step 3: Remove Heroku Config
```bash
heroku config:unset CLOUDINARY_CLOUD_NAME
heroku config:unset CLOUDINARY_API_KEY
heroku config:unset CLOUDINARY_API_SECRET
```

### Step 4: Deploy
```bash
git add .
git commit -m "Remove Cloudinary dependency"
git push heroku main
```

## Success Criteria

Deployment is successful when:
- ✅ Site loads without errors
- ✅ Existing products still display
- ✅ New products with URLs display correctly
- ✅ Admin can add products with URLs
- ✅ No console errors
- ✅ Images load fast

## Troubleshooting

### Images not loading?
- Check URL is publicly accessible
- Test URL in browser directly
- Verify URL is in image_url field
- Check browser console for errors

### Migration errors?
```bash
# Check migration status
heroku run python manage.py showmigrations

# Run migrations again
heroku run python manage.py migrate
```

### Admin not showing new fields?
- Clear browser cache
- Hard refresh (Ctrl+Shift+R)
- Check if migrations ran successfully

## Support Resources

- `IMAGE_STORAGE_OPTIONS.md` - Technical details
- `QUICK_IMAGE_GUIDE.md` - Simple how-to
- `DEPLOYMENT_UPDATE.md` - Deployment guide
- `IMAGE_STORAGE_COMPLETE.md` - Summary

## Contact

If issues persist:
1. Check Heroku logs: `heroku logs --tail`
2. Check Django admin for errors
3. Verify database migrations
4. Review documentation files

## Timeline

- **Development**: Completed ✅
- **Local Testing**: Completed ✅
- **Documentation**: Completed ✅
- **Ready to Deploy**: YES ✅

## Next Actions

1. Run deployment commands above
2. Test thoroughly
3. Add your 200 products using Imgur URLs
4. (Optional) Remove Cloudinary if desired

---

**Ready to deploy!** 🚀
