# Django Deployment to cPanel - Complete Guide

## Prerequisites

### What You Need:
1. cPanel hosting account with:
   - Python support (Python 3.8+)
   - PostgreSQL or MySQL database
   - SSH access (recommended)
   - Sufficient storage for your project

2. Your cPanel credentials:
   - cPanel URL
   - Username
   - Password

## Step 1: Prepare Your Project

### 1.1 Create requirements.txt
Make sure all dependencies are listed:
```bash
pip freeze > requirements.txt
```

### 1.2 Update settings.py for Production
Create a production settings file or update existing:

```python
# jewellery_site/settings.py

import os
from decouple import config

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Database - use environment variables
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # or mysql
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
```

### 1.3 Create .env.example
```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

## Step 2: Setup cPanel

### 2.1 Create Database

1. Log into cPanel
2. Go to **MySQL Databases** (or PostgreSQL)
3. Create a new database:
   - Database name: `username_popshop`
4. Create a database user:
   - Username: `username_popshop`
   - Password: (generate strong password)
5. Add user to database with ALL PRIVILEGES

### 2.2 Setup Python Application

1. In cPanel, go to **Setup Python App**
2. Click **Create Application**
3. Configure:
   - Python version: 3.9 or higher
   - Application root: `popshop` (or your project name)
   - Application URL: `/` (for main domain) or `/shop` (for subdirectory)
   - Application startup file: `passenger_wsgi.py`
   - Application Entry point: `application`

4. Click **Create**

## Step 3: Upload Your Project

### Option A: Using File Manager (Easy)

1. In cPanel, go to **File Manager**
2. Navigate to the application root directory (e.g., `/home/username/popshop`)
3. Upload your project as a ZIP file
4. Extract the ZIP file
5. Delete the ZIP file

### Option B: Using Git (Recommended)

1. In cPanel, go to **Terminal** or use SSH
2. Navigate to your application directory:
```bash
cd ~/popshop
```

3. Clone your repository:
```bash
git clone https://github.com/yourusername/your-repo.git .
```

### Option C: Using FTP/SFTP

1. Use FileZilla or similar FTP client
2. Connect to your cPanel server
3. Upload all project files to the application directory

## Step 4: Configure the Application

### 4.1 Create passenger_wsgi.py

In your project root (same level as manage.py), create:

```python
# passenger_wsgi.py
import os
import sys

# Add your project directory to the sys.path
project_home = os.path.dirname(os.path.abspath(__file__))
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variable for Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'jewellery_site.settings'

# Import Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 4.2 Create .env file

In your project root, create `.env` with your actual values:
```
SECRET_KEY=your-actual-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=username_popshop
DB_USER=username_popshop
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=5432
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### 4.3 Install Dependencies

1. In cPanel Terminal or SSH:
```bash
cd ~/popshop
source /home/username/virtualenv/popshop/3.9/bin/activate
pip install -r requirements.txt
```

## Step 5: Run Django Commands

### 5.1 Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 5.2 Run Migrations
```bash
python manage.py migrate
```

### 5.3 Create Superuser
```bash
python manage.py createsuperuser
```

### 5.4 Load Initial Data (if you have fixtures)
```bash
python manage.py loaddata your_fixture.json
```

## Step 6: Configure Static Files

### Option A: Using .htaccess (Recommended)

Create `.htaccess` in your public_html or application root:

```apache
# .htaccess
RewriteEngine On
RewriteBase /

# Serve static files directly
RewriteCond %{REQUEST_URI} ^/static/ [OR]
RewriteCond %{REQUEST_URI} ^/media/
RewriteRule ^(.*)$ - [L]

# Pass all other requests to Django
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ passenger_wsgi.py [L]
```

### Option B: Symlink Static Files

```bash
cd ~/public_html
ln -s ~/popshop/staticfiles static
ln -s ~/popshop/media media
```

## Step 7: Restart Application

In cPanel:
1. Go to **Setup Python App**
2. Find your application
3. Click **Restart** button

Or via command line:
```bash
touch ~/popshop/tmp/restart.txt
```

## Step 8: Test Your Deployment

1. Visit your domain: `https://yourdomain.com`
2. Test the following:
   - [ ] Homepage loads
   - [ ] Static files load (CSS, JS, images)
   - [ ] Products display correctly
   - [ ] Add to cart works
   - [ ] Cart persists across pages
   - [ ] MyAdmin login works
   - [ ] MyAdmin functions work

## Troubleshooting

### Issue: 500 Internal Server Error

**Check error logs:**
```bash
tail -f ~/logs/error_log
```

**Common causes:**
- Wrong Python version
- Missing dependencies
- Database connection error
- Incorrect file permissions

**Fix permissions:**
```bash
chmod 755 ~/popshop
chmod 644 ~/popshop/*.py
```

### Issue: Static Files Not Loading

**Check static files path:**
```bash
ls -la ~/popshop/staticfiles
```

**Recollect static files:**
```bash
python manage.py collectstatic --clear --noinput
```

### Issue: Database Connection Error

**Check database credentials:**
```bash
cat ~/.env
```

**Test database connection:**
```bash
python manage.py dbshell
```

### Issue: Module Not Found

**Reinstall requirements:**
```bash
pip install -r requirements.txt --force-reinstall
```

## Updating Your Application

### Method 1: Git Pull (Recommended)

```bash
cd ~/popshop
git pull origin main
source /home/username/virtualenv/popshop/3.9/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
touch tmp/restart.txt
```

### Method 2: Manual Upload

1. Upload changed files via File Manager or FTP
2. Run migrations if needed
3. Collect static files
4. Restart application

## Performance Optimization

### 1. Enable Caching

Add to settings.py:
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    }
}
```

Create cache table:
```bash
python manage.py createcachetable
```

### 2. Optimize Database

```bash
python manage.py dbshell
VACUUM ANALYZE;
```

### 3. Enable Gzip Compression

Add to .htaccess:
```apache
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript
</IfModule>
```

## Security Checklist

- [ ] DEBUG = False in production
- [ ] Strong SECRET_KEY
- [ ] ALLOWED_HOSTS configured
- [ ] HTTPS enabled (SSL certificate)
- [ ] Secure cookies enabled
- [ ] Database credentials in .env (not in code)
- [ ] .env file not in git (.gitignore)
- [ ] File permissions correct (755 for directories, 644 for files)
- [ ] Regular backups configured

## Backup Strategy

### 1. Database Backup

Create cron job in cPanel:
```bash
0 2 * * * pg_dump -U username_popshop username_popshop > ~/backups/db_$(date +\%Y\%m\%d).sql
```

### 2. Files Backup

Use cPanel Backup feature:
1. Go to **Backup** in cPanel
2. Download **Full Backup** or **Home Directory**
3. Schedule automatic backups

## Monitoring

### 1. Setup Error Logging

Add to settings.py:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/home/username/logs/django_error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### 2. Monitor Logs

```bash
tail -f ~/logs/error_log
tail -f ~/logs/django_error.log
```

## Domain Configuration

### 1. Point Domain to cPanel

Update DNS records:
- A Record: Point to your cPanel server IP
- CNAME Record: www → yourdomain.com

### 2. SSL Certificate

In cPanel:
1. Go to **SSL/TLS Status**
2. Enable **AutoSSL** for your domain
3. Or install Let's Encrypt certificate

## Support Resources

- cPanel Documentation: https://docs.cpanel.net/
- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/
- Python on cPanel: https://docs.cpanel.net/cpanel/software/python-selector/

## Quick Reference Commands

```bash
# Activate virtual environment
source /home/username/virtualenv/popshop/3.9/bin/activate

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser

# Clear sessions
python manage.py clearsessions

# Restart application
touch ~/popshop/tmp/restart.txt

# View error logs
tail -f ~/logs/error_log

# Check Python version
python --version

# List installed packages
pip list
```

## Conclusion

Your Django application should now be successfully deployed on cPanel! The cart system will work perfectly since cPanel provides a more stable environment than Heroku for session management.

**Next Steps:**
1. Test all functionality thoroughly
2. Set up regular backups
3. Monitor error logs
4. Configure domain and SSL
5. Optimize performance

Good luck with your deployment! 🚀

