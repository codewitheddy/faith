# cPanel Deployment Checklist

## Pre-Deployment (Local)

- [x] Cart system tested and working locally
- [x] MyAdmin panel fully functional
- [x] All features tested
- [x] requirements.txt created
- [x] .env.example created
- [x] passenger_wsgi.py created
- [x] .gitignore configured
- [ ] Final local test completed
- [ ] Database backup created (if needed)

## cPanel Setup

- [ ] cPanel account accessed
- [ ] Database created (MySQL or PostgreSQL)
- [ ] Database user created with strong password
- [ ] User added to database with ALL PRIVILEGES
- [ ] Database credentials saved securely
- [ ] Python App created in cPanel
- [ ] Virtual environment path noted

## File Upload

- [ ] Project uploaded to cPanel (Git/FTP/File Manager)
- [ ] Files extracted in correct directory
- [ ] .env file created with production values
- [ ] passenger_wsgi.py in project root
- [ ] File permissions set correctly (755 for dirs, 644 for files)

## Configuration

- [ ] Virtual environment activated
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Static files collected: `python manage.py collectstatic --noinput`
- [ ] Migrations run: `python manage.py migrate`
- [ ] Superuser created: `python manage.py createsuperuser`
- [ ] Sessions cleared: `python manage.py clearsessions`
- [ ] .htaccess configured in public_html
- [ ] Static files symlinked

## Testing

### Homepage
- [ ] Homepage loads without errors
- [ ] Products display correctly
- [ ] Images load from Cloudinary
- [ ] CSS styles applied
- [ ] JavaScript working

### Cart System
- [ ] Add product to cart
- [ ] Cart count updates correctly
- [ ] Cart persists on page refresh
- [ ] Cart persists across pages
- [ ] Quantity increase/decrease works
- [ ] Remove item works
- [ ] Cart modal displays correctly
- [ ] Cart count never goes negative

### Checkout
- [ ] Checkout form displays
- [ ] Form validation works
- [ ] Order saves to database
- [ ] WhatsApp message generates correctly
- [ ] Cart clears after checkout

### MyAdmin Panel
- [ ] Login page loads: `/myadmin/`
- [ ] Login works with credentials
- [ ] Dashboard displays correctly
- [ ] Product list loads
- [ ] Add product works
- [ ] Edit product works
- [ ] Delete product works
- [ ] Order list loads
- [ ] Order details display
- [ ] Category management works
- [ ] User management works
- [ ] Analytics dashboard works
- [ ] Logout works

### Mobile Testing
- [ ] Homepage responsive
- [ ] Cart works on mobile
- [ ] Checkout works on mobile
- [ ] MyAdmin works on mobile

## Security

- [ ] DEBUG = False in .env
- [ ] Strong SECRET_KEY generated
- [ ] ALLOWED_HOSTS configured
- [ ] SSL certificate installed
- [ ] HTTPS redirect working
- [ ] Secure cookies enabled
- [ ] .env not in Git repository

## Performance

- [ ] Static files loading fast
- [ ] Images optimized via Cloudinary
- [ ] Page load times acceptable
- [ ] No console errors
- [ ] No server errors in logs

## Backup

- [ ] Database backup configured
- [ ] Backup schedule set (daily/weekly)
- [ ] Backup location secured
- [ ] Restore procedure tested

## Monitoring

- [ ] Error logs accessible: `~/logs/error_log`
- [ ] Access logs accessible: `~/logs/access_log`
- [ ] Log monitoring set up
- [ ] Error notification configured (optional)

## Documentation

- [ ] Admin credentials documented securely
- [ ] Database credentials documented securely
- [ ] Cloudinary credentials documented
- [ ] Update procedure documented
- [ ] Troubleshooting guide reviewed

## Go Live

- [ ] Domain DNS configured
- [ ] Domain pointing to cPanel
- [ ] SSL certificate active
- [ ] Final full test completed
- [ ] Stakeholders notified
- [ ] Site live and accessible

## Post-Deployment

- [ ] Monitor error logs for 24 hours
- [ ] Test all features again
- [ ] Verify cart persistence
- [ ] Check order creation
- [ ] Monitor performance
- [ ] Collect user feedback

## Quick Commands Reference

```bash
# Activate virtual environment
source /home/username/virtualenv/jewellery_site/3.9/bin/activate

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Clear sessions
python manage.py clearsessions

# Restart application
touch ~/jewellery_site/tmp/restart.txt

# View error logs
tail -f ~/logs/error_log

# Check Python version
python --version

# List installed packages
pip list
```

## Troubleshooting Quick Fixes

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
ln -s ~/jewellery_site/staticfiles static
```

### Database Connection Error
```bash
cat ~/.env  # Check credentials
python manage.py dbshell  # Test connection
```

### Cart Issues
```bash
python manage.py clearsessions
touch ~/jewellery_site/tmp/restart.txt
```

## Success Criteria

✅ All checklist items completed
✅ No errors in logs
✅ All features working
✅ Cart persisting correctly
✅ Orders saving to database
✅ MyAdmin fully functional
✅ Mobile responsive
✅ SSL active
✅ Performance acceptable

## Notes

- Keep this checklist handy during deployment
- Check off items as you complete them
- Document any issues encountered
- Save all credentials securely
- Test thoroughly before going live

**Deployment Date**: _______________
**Deployed By**: _______________
**Domain**: _______________
**Status**: _______________
