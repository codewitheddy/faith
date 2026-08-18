# Complete cPanel Deployment Guide - Summary

Your Wyatt Collection Django app is ready to deploy to cPanel from GitHub!

## 📦 What You Have

✅ **Code Repository**: https://github.com/codewitheddy/faith.git
✅ **All Dependencies**: Listed in `requirements.txt`
✅ **Email System**: Configured and tested
✅ **Database Ready**: SQLite or PostgreSQL compatible
✅ **Static Files**: WhiteNoise configured
✅ **Heroku Code**: Removed ✓

## 🚀 Deployment Options

### ⚡ Quick Start (5 minutes)
If you're experienced with deployment:
- See: **`CPANEL_QUICKSTART.md`**

### 📋 Step-by-Step Guide (Recommended)
Complete walkthrough with explanations:
- See: **`CPANEL_GITHUB_DEPLOYMENT.md`**

### ✓ Deployment Checklist
Track your progress during deployment:
- See: **`DEPLOYMENT_CHECKLIST.md`**

## 🎯 High-Level Steps

1. **SSH into cPanel**
   ```bash
   ssh username@wyatt.co.ke
   cd ~/public_html
   ```

2. **Clone Repository**
   ```bash
   git clone https://github.com/codewitheddy/faith.git .
   ```

3. **Setup Python Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Configure Environment (.env)**
   ```bash
   nano .env
   # Add all required variables (see guide for full list)
   ```

5. **Initialize Database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic --noinput
   ```

6. **Configure in cPanel**
   - Go to: **Setup Python App** (or Python App Manager)
   - Create Application
   - Select Python 3.9+
   - Set Application Root: `/home/username/public_html`
   - Startup File: `jewellery_site/wsgi.py`
   - Entry Point: `application`

7. **Test & Go Live**
   ```bash
   touch jewellery_site/wsgi.py  # Restart
   curl https://wyatt.co.ke      # Test
   ```

## 📁 Key Files in Repository

```
faith/
├── CPANEL_QUICKSTART.md              ← 5-min quick guide
├── CPANEL_GITHUB_DEPLOYMENT.md       ← Full step-by-step
├── DEPLOYMENT_CHECKLIST.md           ← Track progress
├── deploy.sh                         ← Automation script
├── manage.py                         ← Django management
├── jewellery_site/
│   ├── settings.py                   ← Email & DB config
│   └── wsgi.py                       ← Passenger WSGI entry
├── shop/
│   ├── models.py                     ← Database models
│   ├── views.py                      ← Order handling
│   ├── email_utils.py                ← Email functions
│   └── templates/
│       └── emails/
│           ├── order_confirmation.html
│           └── order_completed.html
├── requirements.txt                  ← Python packages
├── .env.example                      ← Environment template
└── .htaccess                         ← URL routing
```

## 🔧 Configuration Needed (.env)

Create `.env` file on cPanel server with:

```ini
# Core Settings
SECRET_KEY=your-django-secret-key
DEBUG=False
ALLOWED_HOSTS=wyatt.co.ke,www.wyatt.co.ke

# Database (SQLite is default)
DATABASE_URL=sqlite:///db.sqlite3
# OR PostgreSQL (if your host provides it)
# DATABASE_URL=postgresql://user:pass@localhost:5432/dbname

# Email Configuration (Already Set Up)
EMAIL_HOST=mail.wyatt.co.ke
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=info@wyatt.co.ke
EMAIL_HOST_PASSWORD=Kangemi254.@
DEFAULT_FROM_EMAIL=WYATT COLLECTION <info@wyatt.co.ke>

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## 📧 Email System

**Already Configured!** ✓

- **SMTP Server**: mail.wyatt.co.ke (Port 587 TLS)
- **From Address**: info@wyatt.co.ke
- **Display Name**: WYATT COLLECTION
- **Features**:
  - Order confirmation email on checkout
  - Order completion email when admin marks as delivered
  - Test command: `python manage.py send_test_email --to email@example.com`

## 🔒 Security Notes

1. **Never commit .env** - It's in `.gitignore`
2. **Use environment variables** for all secrets
3. **Keep DEBUG=False** in production
4. **Use HTTPS only** (enabled by default in settings)
5. **Backup database regularly** - Add to cPanel backups
6. **Monitor logs** - Check `logs/myadmin.log` and `error_log`

## 📊 Monitoring

After deployment, monitor these:

```bash
# Application logs
tail -f logs/myadmin.log

# Web server errors
tail -f error_log

# Current status
git status
git log -1

# Email test
python manage.py send_test_email --to admin@example.com
```

## 🔄 Future Updates

To update code after initial deployment:

**Option A: Manual (30 seconds)**
```bash
ssh username@wyatt.co.ke
cd ~/public_html
git pull origin main
touch jewellery_site/wsgi.py
```

**Option B: Automated Script**
```bash
bash deploy.sh
```

**Option C: GitHub Webhooks**
- Configure in GitHub Settings → Webhooks
- Auto-deploys on push to main branch

## ❓ Troubleshooting

### 500 Error
```bash
tail -50 error_log
tail -50 logs/myadmin.log
python manage.py migrate  # Run migrations if needed
```

### Static files not loading (404)
```bash
python manage.py collectstatic --noinput
# Check .htaccess allows /static/
```

### Email not working
```bash
# Test email
python manage.py send_test_email --to test@example.com

# Verify config
cat .env | grep EMAIL

# Check cPanel email account exists
# Verify password is correct
```

### "ModuleNotFoundError"
```bash
source venv/bin/activate
pip install -r requirements.txt
touch jewellery_site/wsgi.py
```

## 📞 Getting Help

1. **Check logs first**: `tail -50 error_log`
2. **Read the full guide**: `CPANEL_GITHUB_DEPLOYMENT.md`
3. **Use checklist**: `DEPLOYMENT_CHECKLIST.md`
4. **Contact hosting**: cPanel support for server issues

## ✅ Success Indicators

After deployment, you should see:

- ✓ Website loads at https://wyatt.co.ke
- ✓ Admin panel at https://wyatt.co.ke/admin/
- ✓ Order form works and submits
- ✓ Confirmation email received on new order
- ✓ Admin can mark orders as delivered
- ✓ Completion email received
- ✓ No errors in logs
- ✓ Static files load (CSS, images, JS)

## 📋 Deployment Status

| Component | Status | Notes |
|-----------|--------|-------|
| Code Repo | ✓ Ready | https://github.com/codewitheddy/faith.git |
| Django App | ✓ Ready | Version 6.0.2 |
| Email System | ✓ Ready | cPanel SMTP configured |
| Database | ✓ Ready | SQLite included |
| Static Files | ✓ Ready | WhiteNoise configured |
| Documentation | ✓ Ready | All guides included |
| Heroku Code | ✓ Removed | Clean for cPanel |

## 🎉 You're Ready!

Your application is fully prepared for cPanel deployment. Choose your deployment method above and follow the relevant guide.

**Estimated time**: 15-30 minutes (first deployment)

---

**Questions?** See the detailed guides:
- Quick: `CPANEL_QUICKSTART.md`
- Complete: `CPANEL_GITHUB_DEPLOYMENT.md`  
- Checklist: `DEPLOYMENT_CHECKLIST.md`

**Last Updated**: August 18, 2026
**App**: Wyatt Collection Django Shop
**Version**: Production Ready
