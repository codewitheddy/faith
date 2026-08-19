# Heroku Cart Sync Debugging Guide

## Issue
Cart items show in the cart modal but product cards don't sync (quantity selectors don't appear).

## Root Causes

### 1. Product ID Mismatch
**Symptom**: Cart shows items but console says "Add button not found"
**Cause**: Cart has product IDs that don't exist on current page
**Solution**: 
- Products might have been deleted/recreated with different IDs
- Clear cart and re-add products
- Or navigate to page 1 where those products exist

### 2. Session Persistence Issue
**Symptom**: Cart works locally but not on Heroku
**Cause**: Session backend differences between local and production
**Solution**: Already configured with `cached_db` backend

### 3. Type Mismatch
**Symptom**: IDs don't match even though they look the same
**Cause**: String vs Number comparison
**Solution**: Use `String()` for all comparisons (already implemented)

## Debugging Steps

### Step 1: Check Console Logs
Open browser console and look for:
```
=== CART DATA ON PAGE LOAD ===
Cart items: [{id: "1", quantity: 2}, ...]
Available product IDs on page: ["5", "6", "7", "8"]
```

If cart item IDs don't match available IDs, that's the problem!

### Step 2: Clear Cart
If IDs don't match, clear the cart:
1. Open cart modal
2. Remove all items
3. Re-add products from current page

### Step 3: Check Database
Products might have been deleted. Check in MyAdmin:
1. Go to `/myadmin/products/`
2. Verify products exist with the IDs shown in cart

### Step 4: Clear Sessions (if needed)
On Heroku:
```bash
heroku run python manage.py clearsessions
```

## Prevention

### For Development
1. Don't delete products that are in carts
2. Use fixtures to maintain consistent product IDs
3. Test cart sync after each deployment

### For Production
1. Implement cart cleanup on page load (remove invalid items)
2. Add product availability check
3. Show user-friendly message for removed products

## Quick Fix for Users

If cart shows items but they don't sync:

1. **Clear Browser Cache**: Hard refresh (Ctrl+Shift+R)
2. **Clear Cart**: Remove all items and re-add
3. **Check Product Page**: Make sure products still exist

## Code Changes Made

### 1. String Comparison (✓ Done)
All ID comparisons now use `String()` for consistency

### 2. Enhanced Logging (✓ Done)
Console now shows:
- Product ID types
- Available IDs on page
- Detailed sync status

### 3. Next Steps (To Do)
- Add automatic cart cleanup for invalid items
- Show toast notification for removed products
- Add cart validation endpoint

## Testing Checklist

- [ ] Add product to cart
- [ ] Refresh page - quantity selector should show
- [ ] Navigate to different page - cart count should persist
- [ ] Navigate back - quantity selector should show
- [ ] Remove from cart modal - product card should reset
- [ ] Clear browser cache - cart should persist
- [ ] Deploy to Heroku - all above should work

## Common Issues

### Issue: "Add button not found"
**Fix**: Product IDs in cart don't match products on page
- Check console for "Available product IDs on page"
- Compare with cart item IDs
- Clear cart if IDs don't match

### Issue: Cart count shows but no items in modal
**Fix**: Session data corrupted
- Clear sessions: `heroku run python manage.py clearsessions`
- Clear browser cookies
- Re-add items

### Issue: Works locally but not on Heroku
**Fix**: Check these differences:
- Database IDs might be different
- Session backend configuration
- Static files cache (update version number)

## Monitoring

Add to Sentry (when configured):
- Track cart sync failures
- Monitor session issues
- Alert on high error rates

## Support

If issue persists:
1. Check Heroku logs: `heroku logs --tail`
2. Check browser console for errors
3. Verify session configuration in settings.py
4. Test with fresh browser session (incognito mode)

