# cPanel Django Deployment from GitHub

Complete step-by-step guide to deploy your Django app from GitHub to cPanel.

## Prerequisites
- cPanel account with SSH access enabled
- GitHub repository: https://github.com/codewitheddy/faith.git
- Domain: wyatt.co.ke (or your domain)
- Python 3.9+ available on cPanel server

## Step 1: Connect to cPanel via SSH

```bash
# Open Terminal/PowerShell and connect to your cPanel server
ssh username@wyatt.co.ke
# or
ssh username@your-cpanel-ip

# If using a specific port (usually 22, but ask hosting provider)
ssh -p 22 username@wyatt.co.ke
```

Replace `username` with your cPanel username.

## Step 2: Navigate to Your Domain Directory

```bash
# Check available domains
cd ~
ls -la

# Navigate to your public_html or specific domain folder
cd public_html
# or if you have a specific domain folder:
cd ~/public_html/wyatt.co.ke
# or
cd ~/myshop (depending on your setup)

# Check current location
pwd
```

## Step 3: Clone the Repository from GitHub

```bash
# If directory is empty, clone directly:
git clone https://github.com/codewitheddy/faith.git .

# If you want to clone into a specific folder:
git clone https://github.com/codewitheddy/faith.git myshop_app

# Then navigate into it:
cd myshop_app
```

## Step 4: Set Up Python Environment

```bash
# Check Python version available
python3 --version
# Should be 3.9 or higher

# Create a virtual environment in your app directory
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

## Step 5: Install Python Dependencies

```bash
# Make sure you're in the activated virtual environment
# Install all requirements
pip install --upgrade pip
pip install -r requirements.txt

# This will install:
# - Django 6.0.2
# - psycopg2-binary (PostgreSQL)
# - python-decouple (environment variables)
# - Pillow (image processing)
# - cloudinary (image hosting)
# - whitenoise (static files)
# - gunicorn (WSGI server)
# - sentry-sdk (error tracking - optional)
```

## Step 6: Configure Environment Variables

```bash
# Create .env file in your project root
nano .env
# or
vi .env

# Add these configuration variables:
```

```
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=wyatt.co.ke,www.wyatt.co.ke,your-cpanel-ip

# Database (if using PostgreSQL - ask hosting provider for details)
DATABASE_URL=postgresql://user:password@localhost:5432/database_name
# Or if using SQLite (default):
DATABASE_URL=sqlite:///db.sqlite3

# Email Configuration
EMAIL_HOST=mail.wyatt.co.ke
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=info@wyatt.co.ke
EMAIL_HOST_PASSWORD=Kangemi254.@
DEFAULT_FROM_EMAIL=WYATT COLLECTION <info@wyatt.co.ke>

# Cloudinary (optional - for image hosting)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Sentry (optional - error tracking)
SENTRY_DSN=your-sentry-dsn

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

Save the file (Ctrl+X, then Y, then Enter if using nano)

## Step 7: Collect Static Files

```bash
# Make sure you're in the activated virtual environment
python manage.py collectstatic --noinput

# This collects all CSS, JS, images into staticfiles/ directory
```

## Step 8: Set Up Database

```bash
# Run migrations to set up database tables
python manage.py migrate

# Create a superuser account for admin
python manage.py createsuperuser
# Follow prompts to create admin account
```

## Step 9: Configure cPanel for Django (Passenger WSGI)

### Option A: Using cPanel's Python Application Manager (Recommended)

1. Log into cPanel
2. Go to **Setup Python App** (or **Python App Manager**)
3. Click **Create Application**
4. Configure:
   - **Python Version**: 3.9+ (or latest available)
   - **Application Root**: `/home/username/public_html/myshop` (your app path)
   - **Application Startup File**: `jewellery_site/wsgi.py`
   - **Application Entry Point**: `application`
5. Click **Create**

cPanel will generate necessary files automatically.

### Option B: Manual Passenger WSGI Setup

If Option A isn't available, create a `passenger_wsgi.py` file:

```bash
# Create passenger_wsgi.py in your project root
nano passenger_wsgi.py
```

Add this content:

```python
import sys
import os

# Add project directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Setup Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'jewellery_site.settings'

# Import WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## Step 10: Verify .htaccess File

The `.htaccess` file in your project root should already be configured. Verify it exists:

```bash
ls -la | grep htaccess

# You should see: -rw-r--r-- .htaccess
```

If missing, create it (check your repository for .htaccess).

## Step 11: Set File Permissions

```bash
# Make sure permissions are correct
chmod 755 .
chmod 755 manage.py

# Set write permissions for media and logs
chmod 755 media/
chmod 755 logs/

# Ensure static files are readable
chmod -R 755 staticfiles/
```

## Step 12: Restart the Application

```bash
# Via SSH, touch the wsgi.py file to restart Passenger
touch jewellery_site/wsgi.py

# Or restart via cPanel:
# 1. Go to cPanel > Setup Python App
# 2. Find your application
# 3. Click "Restart"
```

## Step 13: Test Your Application

```bash
# Test if the app is running
curl https://wyatt.co.ke

# Check for errors in logs
tail -f logs/myadmin.log

# Or check error logs
tail -f error_log
```

Visit your domain in a browser:
- **Main site**: https://wyatt.co.ke
- **Admin panel**: https://wyatt.co.ke/admin/

## Step 14: Set Up Auto-Updates from GitHub

To automatically pull updates from GitHub when you push code:

### Option A: Manual Pull (Easiest)

```bash
# SSH into cPanel
ssh username@wyatt.co.ke
cd ~/public_html/myshop

# Pull latest code
git pull origin main

# Restart application
touch jewellery_site/wsgi.py
```

### Option B: Webhook (Automated)

1. Go to GitHub Repository Settings
2. Click **Webhooks** > **Add webhook**
3. Configure:
   - **Payload URL**: `https://wyatt.co.ke/webhook/github/` (create this endpoint in your app)
   - **Content type**: `application/json`
   - **Events**: `Push events`
4. Your app will auto-update when you push to GitHub

## Troubleshooting

### Issue: "ModuleNotFoundError" or "ImportError"

**Solution**: Make sure virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Permission denied" on files

**Solution**: Fix permissions:
```bash
chmod 755 manage.py
chmod -R 755 staticfiles/
chmod -R 755 media/
```

### Issue: Static files not loading (404 errors on CSS/JS)

**Solution**: Collect static files:
```bash
python manage.py collectstatic --noinput
```

### Issue: Email not sending

**Solution**: Verify email configuration in `.env`:
```bash
nano .env
# Check EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
```

### Issue: Database connection error

**Solution**: Check DATABASE_URL in `.env`:
```bash
# Test SQLite (default):
ls -la db.sqlite3

# If using PostgreSQL, verify credentials
```

### Issue: 500 Internal Server Error

**Solution**: Check error logs:
```bash
tail -50 error_log
tail -50 logs/myadmin.log

# Run migrations if needed
python manage.py migrate

# Restart application
touch jewellery_site/wsgi.py
```

## Important Notes

1. **Never commit .env file** - It's in .gitignore (keep secrets safe)
2. **Use environment variables** for sensitive data
3. **Always use HTTPS** in production
4. **Keep DEBUG=False** in production
5. **Regularly backup** your database and media files
6. **Monitor logs** for errors: `logs/myadmin.log`

## Email System Verification

Your app has email configured for order notifications:

```bash
# Send test email from cPanel terminal
python manage.py send_test_email --to your-email@example.com
```

Check if you receive the test email. If not, verify:
- EMAIL_HOST_PASSWORD is correct
- firewall allows SMTP connections on port 587
- Email account (info@wyatt.co.ke) exists on cPanel

## Next Steps

1. Deploy to cPanel following steps above
2. Test the website at https://wyatt.co.ke
3. Place test orders to verify email notifications
4. Monitor logs for any errors
5. Set up automated backups in cPanel

## Support

If you encounter issues:
1. Check error logs: `logs/myadmin.log` and `error_log`
2. Verify `.env` configuration
3. Check file permissions (755 for directories, 644 for files)
4. Restart Passenger application: `touch jewellery_site/wsgi.py`
5. Contact cPanel support if Passenger-related issues persist

---

**Last Updated**: August 18, 2026
**Django Version**: 6.0.2
**Python**: 3.9+
**Hosting**: cPanel with Passenger WSGI
