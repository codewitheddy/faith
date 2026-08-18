# cPanel Deployment Checklist

Quick checklist for deploying to cPanel from GitHub.

## Pre-Deployment (Local Machine)

- [ ] Code committed and pushed to GitHub
  ```bash
  git status
  git add .
  git commit -m "Ready for deployment"
  git push origin main
  ```

- [ ] All Heroku references removed ✓
- [ ] .env file configured locally
- [ ] Email settings verified
- [ ] Database migrations created locally
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

## SSH Setup

- [ ] SSH access enabled on cPanel account
- [ ] Known hostname/IP of cPanel server
- [ ] SSH username ready
- [ ] Can connect: `ssh username@wyatt.co.ke`

## On cPanel Server

### Initial Setup
- [ ] Navigate to domain directory
  ```bash
  cd ~/public_html
  # or
  cd ~/myshop
  ```

- [ ] Clone repository
  ```bash
  git clone https://github.com/codewitheddy/faith.git .
  # or
  cd myshop && git clone https://github.com/codewitheddy/faith.git .
  ```

- [ ] Create virtual environment
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- [ ] Install dependencies
  ```bash
  pip install --upgrade pip
  pip install -r requirements.txt
  ```

### Configuration
- [ ] Create .env file with all variables
  ```bash
  nano .env
  ```
  
  Required variables:
  - [ ] SECRET_KEY (Django secret)
  - [ ] DEBUG=False (for production)
  - [ ] ALLOWED_HOSTS (your domain)
  - [ ] DATABASE_URL (or use SQLite)
  - [ ] EMAIL_HOST_PASSWORD (cPanel email password)
  - [ ] All EMAIL_* variables

- [ ] Verify .env contains no errors
  ```bash
  cat .env
  ```

### Database & Static Files
- [ ] Run migrations
  ```bash
  python manage.py migrate
  ```

- [ ] Create superuser (admin account)
  ```bash
  python manage.py createsuperuser
  ```

- [ ] Collect static files
  ```bash
  python manage.py collectstatic --noinput
  ```

### Permissions
- [ ] Set correct file permissions
  ```bash
  chmod 755 manage.py
  chmod -R 755 staticfiles/
  chmod -R 755 media/
  chmod -R 755 logs/
  ```

### Passenger WSGI Setup
- [ ] passenger_wsgi.py exists and is correct
  ```bash
  ls -la passenger_wsgi.py
  cat passenger_wsgi.py
  ```

- [ ] OR Use cPanel's Setup Python App
  - [ ] Go to cPanel > Setup Python App
  - [ ] Create Application with:
    - Python Version: 3.9+
    - Application Root: /home/username/public_html/myshop
    - Startup File: jewellery_site/wsgi.py
    - Entry Point: application

- [ ] .htaccess file exists
  ```bash
  ls -la .htaccess
  ```

### Testing
- [ ] Restart application
  ```bash
  touch jewellery_site/wsgi.py
  ```

- [ ] Test website loads
  ```bash
  curl -I https://wyatt.co.ke
  # or visit in browser
  ```

- [ ] Admin page works
  ```
  https://wyatt.co.ke/admin/
  ```

- [ ] Static files load (check CSS, images appear)

- [ ] Send test email
  ```bash
  python manage.py send_test_email --to your-email@example.com
  ```

- [ ] Check email received

- [ ] Test checkout process with test order

- [ ] Verify order confirmation email sent

### Logging & Monitoring
- [ ] Check application logs
  ```bash
  tail -20 logs/myadmin.log
  tail -20 error_log
  ```

- [ ] No errors in logs

- [ ] Email system working (confirmed by test)

## Post-Deployment

- [ ] Document any custom configurations
- [ ] Set up automated backups in cPanel
- [ ] Monitor error logs for first 24 hours
- [ ] Set up alert for critical errors
- [ ] Brief team on deployment
- [ ] Update deployment documentation

## Updating Code Later

When you make changes and want to redeploy:

```bash
# SSH into cPanel
ssh username@wyatt.co.ke
cd ~/public_html/myshop

# Activate environment
source venv/bin/activate

# Pull latest code
git pull origin main

# Install any new dependencies
pip install -r requirements.txt

# Run any new migrations
python manage.py migrate

# Collect static files if changed
python manage.py collectstatic --noinput

# Restart app
touch jewellery_site/wsgi.py
```

Or use the automated script:
```bash
bash deploy.sh
```

## Troubleshooting

### App not loading (500 error)

```bash
# Check errors
tail -50 error_log
tail -50 logs/myadmin.log

# Common issues:
# 1. .env file missing or incorrect
# 2. Database migrations not run
# 3. Virtual environment not activated
# 4. Permissions issue
```

### Static files not loading (404 errors)

```bash
# Collect static files again
python manage.py collectstatic --noinput

# Check permissions
ls -la staticfiles/

# Check .htaccess allows static files
```

### Email not working

```bash
# Test email
python manage.py send_test_email --to test@example.com

# Check .env email config
cat .env | grep EMAIL

# Verify credentials are correct
```

### "ModuleNotFoundError" errors

```bash
# Reactivate environment
source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt

# Restart app
touch jewellery_site/wsgi.py
```

## Quick Commands Reference

```bash
# SSH in
ssh username@wyatt.co.ke

# Activate virtual environment
source ~/public_html/myshop/venv/bin/activate

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser

# Test email
python manage.py send_test_email --to your-email@example.com

# Restart app
touch jewellery_site/wsgi.py

# Check logs
tail -20 logs/myadmin.log
tail -20 error_log

# Pull latest code
git pull origin main

# Check status
git status
```

---

**Status**: Ready for deployment
**Environment**: cPanel with Passenger WSGI
**Django**: 6.0.2
**Repository**: https://github.com/codewitheddy/faith.git
