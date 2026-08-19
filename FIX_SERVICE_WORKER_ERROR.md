# Fix Service Worker Error on Shop Page

## Error
```
Failed to fetch sw.js
FetchEvent for "http://127.0.0.1:8000/shop/" resulted in a network error response
TypeError: Failed to fetch at sw.js:69:31
```

## Cause
Your browser has cached an old Service Worker (sw.js) that no longer exists. When trying to load the shop page, the Service Worker tries to fetch the non-existent file and crashes.

---

## Solution: Clear Browser Cache

### Option 1: Chrome/Edge/Brave (Easiest)

1. **Open DevTools:** Press `F12`
2. **Go to Application tab:** Click "Application" in the top menu
3. **Clear Service Workers:**
   - Click "Service Workers" on the left
   - Click "Unregister" for any registered workers
4. **Clear Storage:**
   - Click "Storage" → "Clear site data" (bottom of sidebar)
5. **Refresh:** Press `Ctrl+Shift+R` (hard refresh)

### Option 2: Chrome/Edge (Settings)

1. Press `Ctrl+Shift+Delete` to open Clear Browsing Data
2. Select "All time" for time range
3. Check:
   - ☑ Cookies and other site data
   - ☑ Cached images and files
4. Click "Clear data"
5. Refresh the page: `Ctrl+Shift+R`

### Option 3: Firefox

1. Press `F12` to open DevTools
2. Go to "Storage" tab
3. Click "Service Workers" on the left
4. Click "Unregister" next to any workers
5. Press `Ctrl+Shift+Delete` to clear cache
6. Refresh: `Ctrl+Shift+R`

### Option 4: Safari

1. **Preferences** → **Privacy**
2. Check "Prevent cross-site tracking"
3. **Develop** → **Empty Caches** (if visible)
4. Or: **Safari** → **Clear History** → "All history"
5. Refresh: `Cmd+Shift+R`

---

## Quick Test After Clearing

1. **Hard refresh** shop page: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
2. **Check DevTools** (F12) → Console for errors
3. **If resolved:** Shop page should load with products
4. **If still broken:** Try a different browser (rules out local caching)

---

## Why This Happened

- **Old Deployment:** A previous version of the site might have registered a Service Worker
- **Code Removed:** The sw.js file was removed but Service Worker wasn't unregistered
- **Browser Cache:** Browser keeps trying to use the old Service Worker registration
- **Conflicts:** Old cache conflicts with new code

---

## Prevention for Future

**Don't register Service Workers unless:**
1. ✅ You have a valid use case (offline support, caching strategy)
2. ✅ You will maintain it long-term
3. ✅ You have unregistration/update strategy

**Currently:** Your site doesn't need a Service Worker, so no registration is set up.

---

## Still Having Issues?

### Try These Steps:

1. **Clear cookies:** Settings → Clear browsing data → "All time" → Cookies
2. **Disable extensions:** Temporarily disable browser extensions (may cache content)
3. **Incognito mode:** Try in a private/incognito window (bypasses local cache)
4. **Different browser:** Test in Firefox, Chrome, Safari, or Edge
5. **Fresh installation:** If problem persists, reinstall browser

### Debug in DevTools:

Press `F12` and check:
- **Console tab:** Are there any JavaScript errors?
- **Network tab:** Is `/shop/` returning 200 OK or an error?
- **Application tab:** Are there cached responses?

---

## Expected Behavior After Fix

✅ Shop page loads normally
✅ Products display (if any exist in database)
✅ No console errors
✅ Search and filtering work
✅ Cart functionality works

---

## Related Issue

All products were deleted in a database migration earlier. If you see a blank shop page after fixing this error, that's expected - you need to restore products or re-add them. See `CRITICAL_ISSUE_RESOLVED.md` for recovery options.

---

**Status:** Browser-side fix  
**Difficulty:** Easy (just cache clearing)  
**Time:** 2-3 minutes
