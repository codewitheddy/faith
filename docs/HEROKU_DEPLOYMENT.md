# Heroku Deployment Guide - POPSHOP.KE

## Prerequisites

1. **Heroku Account**: Sign up at https://heroku.com
2. **Heroku CLI**: Install from https://devcenter.heroku.com/articles/heroku-cli
3. **Git**: Ensure Git is installed

## Files Created for Deployment

✅ `Procfile` - Tells Heroku how to run your app
✅ `runtime.txt` - Specifies Python version
✅ `requirements.txt` - Updated with production dependencies
✅ `.env.example` - Template for environment variables
✅ `settings.py` - Updated with production configurations

## Step-by-Step Deployment

### 1. Install Heroku CLI

**Windows:**
```bash
# Download installer from https://devcenter.heroku.com/articles/heroku-cli
```

**Mac:**
```bash
brew tap heroku/brew && brew install heroku
```

**Linux:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

### 2. Login to Heroku

```bash
heroku login
```

This will open a browser window for authentication.

### 3. Initialize Git Repository (if not already done)

```bash
git init
git add .
git commit -m "Initial commit - POPSHOP jewellery site"
```

### 4. Create Heroku App

```bash
heroku create your-app-name
# Example: heroku create popshop-jewellery
```

Or let Heroku generate a name:
```bash
heroku create
```

### 5. Add PostgreSQL Database

```bash
heroku addons:create heroku-postgresql:essential-0
```

This creates a PostgreSQL database (free tier).

### 6. Set Environment Variables

```bash
# Generate a new secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Set the secret key
heroku config:set SECRET_KEY="your-generated-secret-key"

# Set debug to False
heroku config:set DEBUG=False

# Set allowed hosts (replace with your Heroku app URL)
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"
```

### 7. Deploy to Heroku

```bash
git push heroku main
```

Or if your branch is named master:
```bash
git push heroku master
```

### 8. Run Migrations

```bash
heroku run python manage.py migrate
```

### 9. Create Superuser

```bash
heroku run python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### 10. Collect Static Files

```bash
heroku run python manage.py collectstatic --noinput
```

### 11. Create Sample Products (Optional)

```bash
heroku run python manage.py create_sample_products
```

### 12. Open Your App

```bash
heroku open
```

## Post-Deployment Configuration

### Access Admin Panel

Visit: `https://your-app-name.herokuapp.com/admin/`

### View Logs

```bash
heroku logs --tail
```

### Check App Status

```bash
heroku ps
```

## Environment Variables Reference

Set these on Heroku:

```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.herokuapp.com
DATABASE_URL=postgres://... (automatically set by Heroku)
```

## Updating Your App

After making changes:

```bash
git add .
git commit -m "Description of changes"
git push heroku main
```

If you changed models:
```bash
heroku run python manage.py makemigrations
heroku run python manage.py migrate
```

## Custom Domain Setup (Optional)

### 1. Add Domain to Heroku

```bash
heroku domains:add www.yourdomain.com
heroku domains:add yourdomain.com
```

### 2. Update DNS Settings

Add these records at your domain registrar:

**CNAME Record:**
- Host: www
- Value: your-app-name.herokuapp.com

**ALIAS/ANAME Record (or URL Redirect):**
- Host: @
- Value: your-app-name.herokuapp.com

### 3. Update Allowed Hosts

```bash
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com,www.yourdomain.com,yourdomain.com"
```

### 4. Enable SSL (Free)

```bash
heroku certs:auto:enable
```

## Media Files (Product Images)

### Option 1: Use Cloudinary (Recommended)

1. Sign up at https://cloudinary.com
2. Install package:
```bash
pip install django-cloudinary-storage
```

3. Add to requirements.txt and configure in settings.py

### Option 2: Use AWS S3

1. Create S3 bucket
2. Install boto3:
```bash
pip install django-storages boto3
```

3. Configure in settings.py

### Option 3: Heroku Ephemeral Storage (Not Recommended)

Note: Files uploaded to Heroku are deleted when the app restarts (dyno cycling).

## Troubleshooting

### App Won't Start

```bash
heroku logs --tail
```

Check for errors in the logs.

### Static Files Not Loading

```bash
heroku run python manage.py collectstatic --noinput
```

### Database Issues

```bash
heroku pg:info
heroku run python manage.py migrate
```

### Reset Database (CAUTION: Deletes all data)

```bash
heroku pg:reset DATABASE_URL
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

## Scaling Your App

### Check Current Dynos

```bash
heroku ps
```

### Scale Up (Paid)

```bash
heroku ps:scale web=2
```

### Scale Down

```bash
heroku ps:scale web=1
```

## Monitoring

### View Metrics

```bash
heroku logs --tail
```

### Add Monitoring (Optional)

```bash
heroku addons:create papertrail
heroku addons:create newrelic
```

## Cost Optimization

### Free Tier Includes:
- 550-1000 dyno hours/month
- PostgreSQL database (10,000 rows)
- SSL certificate

### Upgrade Options:
- Hobby ($7/month): No sleep, custom domains
- Standard ($25/month): Better performance
- Performance ($250+/month): High traffic

## Backup Strategy

### Manual Backup

```bash
heroku pg:backups:capture
heroku pg:backups:download
```

### Automatic Backups (Paid)

```bash
heroku addons:create heroku-postgresql:standard-0
```

## Security Checklist

✅ DEBUG=False in production
✅ SECRET_KEY is unique and secret
✅ ALLOWED_HOSTS is properly configured
✅ SSL/HTTPS enabled
✅ Database credentials secured
✅ Admin panel has strong password
✅ Regular backups configured

## Support

- Heroku Docs: https://devcenter.heroku.com/
- Django Deployment: https://docs.djangoproject.com/en/6.0/howto/deployment/
- Heroku Support: https://help.heroku.com/

## Quick Commands Reference

```bash
# Deploy
git push heroku main

# Logs
heroku logs --tail

# Run commands
heroku run python manage.py <command>

# Database
heroku pg:info
heroku pg:psql

# Config
heroku config
heroku config:set KEY=value

# Restart
heroku restart

# Open app
heroku open

# Open admin
heroku open /admin/
```

## Success!

Your POPSHOP jewellery e-commerce site is now live on Heroku! 🎉

Access your site at: `https://your-app-name.herokuapp.com`

Admin panel: `https://your-app-name.herokuapp.com/admin/`

