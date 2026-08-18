# cPanel Quick Start - 5 Minute Setup

**Fast deployment guide** (for experienced users)

## 1. SSH into cPanel
```bash
ssh username@wyatt.co.ke
cd ~/public_html
```

## 2. Clone & Setup
```bash
git clone https://github.com/codewitheddy/faith.git .
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 3. Configure
```bash
# Create .env file
nano .env

# Add:
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=wyatt.co.ke,www.wyatt.co.ke
EMAIL_HOST_PASSWORD=Kangemi254.@
DATABASE_URL=sqlite:///db.sqlite3
```

## 4. Setup Database & Static Files
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

## 5. Configure cPanel
**Option A (Recommended):**
- cPanel → Setup Python App
- Create with your domain
- Python 3.9+, Startup File: `jewellery_site/wsgi.py`, Entry Point: `application`

**Option B (Manual):**
- Ensure `passenger_wsgi.py` exists in project root
- Ensure `.htaccess` is in project root

## 6. Restart & Test
```bash
touch jewellery_site/wsgi.py
```

Visit: **https://wyatt.co.ke** ✓

---

## Detailed Guide
See: **CPANEL_GITHUB_DEPLOYMENT.md**

## Full Checklist
See: **DEPLOYMENT_CHECKLIST.md**

## Issues?
```bash
tail -20 error_log
tail -20 logs/myadmin.log
```

---

**Done!** Your site is live 🚀
