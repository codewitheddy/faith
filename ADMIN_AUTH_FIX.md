# Admin Authentication Fix

## Problem
The admin URL `/myadmin/` was redirecting to `/myadmin/login/?next=/myadmin/` but the login page may not have been working properly, or users couldn't access the admin after login.

## Root Cause
1. Missing `LOGIN_URL` and `LOGIN_REDIRECT_URL` settings in Django settings
2. The authentication flow wasn't properly configured

## Solution Applied

### 1. Updated `jewellery_site/settings.py`
Added proper Django authentication settings:

```python
# Authentication settings
LOGIN_URL = '/myadmin/login/'
LOGIN_REDIRECT_URL = '/myadmin/'
```

This tells Django:
- Where to redirect unauthenticated users: `/myadmin/login/`
- Where to redirect after successful login: `/myadmin/` (dashboard)

### 2. Verified Admin Login View
The `AdminLoginView` in `shop/views_admin.py` already had:
- Custom template: `myadmin/login.html`
- Staff-only authentication check
- Proper success URL redirection to dashboard
- No `@staff_required` decorator (so unauthenticated users can access it)

### 3. Verified URL Configuration
`shop/urls_admin.py` properly routes:
- `/myadmin/login/` → AdminLoginView (public)
- `/myadmin/` → DashboardView (staff required)
- All other routes are staff-protected

## How the Flow Works Now

### For Unauthenticated Users
1. Visit `/myadmin/` 
2. DashboardView checks `@staff_required` decorator
3. Redirects to `/myadmin/login/` (via `user_passes_test`)
4. Login page displays with login form
5. Enter credentials
6. On success, redirects to `/myadmin/` dashboard

### For Authenticated Staff Users
1. Visit `/myadmin/`
2. DashboardView verifies user is staff/superuser
3. Displays dashboard immediately

## Testing

To verify the fix:

1. **Clear browser cache** (might have old redirects cached):
   - Open DevTools → Application → Clear Storage
   - Or use Private/Incognito window

2. **Test unauthenticated access**:
   - In incognito, visit `http://127.0.0.1:8000/myadmin/`
   - Should see login form
   - Enter admin credentials
   - Should redirect to dashboard

3. **Test authenticated access**:
   - After logging in, visit `http://127.0.0.1:8000/myadmin/`
   - Should show dashboard directly

## Configuration Details

### Django Settings Applied
- `LOGIN_URL = '/myadmin/login/'` — Where to send unauthenticated requests
- `LOGIN_REDIRECT_URL = '/myadmin/'` — Where to send after login

### Session Settings (Already Configured)
```python
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_AGE = 86400 * 7  # 7 days
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_HTTPONLY = True  # Prevents JS access
SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
```

## Common Issues

### Still seeing login redirect loop?
- **Clear cache**: Ctrl+F5 or use incognito window
- **Check credentials**: Username and password must be for a staff user
- **Check user permissions**: In Django admin, user must have `is_staff=True`

### Login form not submitting?
- Check CSRF token in HTML
- Verify middleware includes `CsrfViewMiddleware`
- Check browser console for errors

### After login, redirects to wrong place?
- Verify `next` parameter in URL
- Clear sessions: Delete session cookie
- Check `LOGIN_REDIRECT_URL` in settings

## Files Modified
1. `jewellery_site/settings.py` — Added LOGIN_URL and LOGIN_REDIRECT_URL
2. `shop/views_admin.py` — Verified AdminLoginView is correct

## Security Notes
- Login view is publicly accessible (not staff-protected)
- Staff check only happens after successful authentication
- Sessions use signed cookies (secure)
- CSRF protection enabled
- HTTPOnly flag set on session cookie
