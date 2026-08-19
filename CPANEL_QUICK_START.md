# cPanel Deployment - Quick Start Guide

## 🚀 Fast Track Deployment (30 minutes)

This is a condensed version for experienced developers. For detailed instructions, see `CPANEL_DEPLOYMENT_READY.md`.

## Prerequisites

- cPanel account with Python support
- Database credentials
- Cloudinary credentials
- Domain name (optional)

## Step 1: cPanel Setup (5 min)

### Create Database
```
cPanel → MySQL/PostgreSQL Databases
→ Create database: username_jewellery
→ Create user: username_jewellery
→ Add user to database (ALL PRIVILEGES)
→ Save credentials
```

### Create Python App
```
cPanel → Setup Python App
→ Create Application
→ Python 3.9+
→ App root: jewellery_site
→ App URL: /
→ Startup file: passenger_wsgi.py
→ Entry point: application
→ Create
→ Note virtual environment path
```

## Step 2: Upload Project (5 min)

### Option A: Git (Recommended)
```bash
cd ~/jewellery_site
git clone https://github.com/yourusername/repo.git .
```

### Option B: File Manager
```
1. Zip project locally
2. Upload to cPanel File Manager
3. Extract in ~/jewellery_site
4. Delete zip
```

## Step 3: Configure (10 min)

### Create .env file
```bash
cd ~/jewellery_site
nano .env
```

Paste and update:
```env
SECRET_KEY=<generate-new-one>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://username_jewellery:password@localhost:5432/username_jewellery
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

Generate SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Install & Setup
```bash
# Activate virtual environment (use path from Step 1)
source /home/username/virtualenv/jewellery_site/3.9/bin/activate

# Install dependencies
pip install -r requirements.txt

# Django setup
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
python manage.py clearsessions
```

## Step 4: Static Files (5 min)

### Create .htaccess in public_html
```apache
RewriteEngine On
RewriteBase /

RewriteCond %{REQUEST_URI} ^/static/ [OR]
RewriteCond %{REQUEST_URI} ^/media/
RewriteRule ^(.*)$ - [L]

RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ passenger_wsgi.py [L]
```

### Create symlinks
```bash
cd ~/public_html
ln -s ~/jewellery_site/staticfiles static
ln -s ~/jewellery_site/media media
```

## Step 5: Restart & Test (5 min)

### Restart
```bash
touch ~/jewellery_site/tmp/restart.txt
```

Or: cPanel → Setup Python App → Restart

### Test
```
✓ Homepage loads
✓ Products display
✓ Add to cart works
✓ Cart count correct
✓ Checkout works
✓ /myadmin/ login works
```

## Quick Commands

```bash
# Activate venv
source /home/username/virtualenv/jewellery_site/3.9/bin/activate

# Update code
cd ~/jewellery_site
git pull
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
touch tmp/restart.txt

# View logs
tail -f ~/logs/error_log

# Clear sessions
python manage.py clearsessions

# Django shell
python manage.py shell
```

## Troubleshooting

### 500 Error
```bash
tail -f ~/logs/error_log
chmod 755 ~/jewellery_site
chmod 644 ~/jewellery_site/*.py
touch ~/jewellery_site/tmp/restart.txt
```

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
cd ~/public_html
ln -sf ~/jewellery_site/staticfiles static
```

### Database Error
```bash
cat ~/.env  # Check credentials
python manage.py dbshell  # Test connection
```

### Cart Issues
```bash
python manage.py clearsessions
touch ~/jewellery_site/tmp/restart.txt
```

## Files Checklist

- [x] requirements.txt
- [x] .env.example
- [x] passenger_wsgi.py
- [x] .gitignore
- [ ] .env (create on server)
- [ ] .htaccess (create on server)

## Environment Variables

Required in `.env`:
- SECRET_KEY (generate new)
- DEBUG (False)
- ALLOWED_HOSTS (your domain)
- DATABASE_URL (from cPanel)
- CLOUDINARY_CLOUD_NAME
- CLOUDINARY_API_KEY
- CLOUDINARY_API_SECRET

## Default Credentials

Admin panel: `/myadmin/`
- Username: admin
- Password: admin123

**Change after first login!**

## Success Indicators

✅ No errors in logs
✅ Homepage loads with products
✅ Cart count accurate
✅ Cart persists across pages
✅ Checkout creates orders
✅ MyAdmin accessible
✅ Static files load
✅ Images from Cloudinary load

## Post-Deployment

1. Test all features
2. Monitor logs for 24h
3. Set up backups
4. Install SSL certificate
5. Update DNS if needed

## Need More Details?

See `CPANEL_DEPLOYMENT_READY.md` for:
- Detailed explanations
- Security configuration
- Performance optimization
- Backup strategies
- Monitoring setup

## Support

- Error logs: `~/logs/error_log`
- Django docs: https://docs.djangoproject.com
- cPanel docs: https://docs.cpanel.net

---

**Total Time: ~30 minutes**
**Difficulty: Medium**
**Success Rate: High** 🎯
