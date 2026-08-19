# Pre-Deployment Checklist for cPanel

## 🎯 Before Running Cleanup

### Code Review
- [ ] All features tested locally
- [ ] No console errors in browser
- [ ] All forms working correctly
- [ ] Cart system working
- [ ] MyAdmin panel functional
- [ ] Database migrations up to date

### Git Status
- [ ] All changes committed to Git
- [ ] Working branch is clean
- [ ] Pushed to remote repository (optional)
- [ ] Tagged release version (optional)

### Environment Variables
- [ ] .env.example is up to date
- [ ] All required variables documented
- [ ] No sensitive data in code

### Database
- [ ] Migrations created for all model changes
- [ ] No pending migrations: `python manage.py showmigrations`
- [ ] Database backup created (if needed)

---

## 🧹 Run Cleanup Script

```bash
python cleanup_for_deployment.py
```

This will:
- Remove compiled Python files (*.pyc)
- Remove __pycache__ directories
- Remove log files
- Remove SQLite database
- Remove temporary files
- Organize documentation into docs/ folder
- Create deployment package list

---

## ✅ After Cleanup Verification

### Essential Files Present
- [ ] manage.py
- [ ] passenger_wsgi.py
- [ ] requirements.txt
- [ ] runtime.txt
- [ ] .htaccess
- [ ] robots.txt
- [ ] .gitignore
- [ ] .env.example

### Essential Directories Present
- [ ] jewellery_site/
- [ ] shop/
- [ ] static/
- [ ] shop/templates/
- [ ] shop/migrations/

### Documentation Present
- [ ] README.md
- [ ] DEPLOYMENT_README.md
- [ ] CPANEL_DEPLOYMENT_READY.md
- [ ] POSTGRESQL_SETUP_GUIDE.md

### Verification Commands
```bash
# Check Python syntax
python -m py_compile jewellery_site/settings.py

# Run Django checks
python manage.py check

# Verify migrations
python manage.py showmigrations

# Test deployment readiness
python verify_deployment_ready.py
```

---

## 📦 Prepare for Upload

### Review Package List
- [ ] Check DEPLOYMENT_PACKAGE_LIST.txt
- [ ] Verify all necessary files included
- [ ] Confirm no sensitive files included

### Create Upload Archive (Optional)
```bash
# Create ZIP for upload
zip -r deployment.zip \
  manage.py \
  passenger_wsgi.py \
  requirements.txt \
  runtime.txt \
  .htaccess \
  robots.txt \
  .env.example \
  jewellery_site/ \
  shop/ \
  static/ \
  -x "*.pyc" "*__pycache__*" "*.log"
```

Or use Git:
```bash
# Create clean export
git archive -o deployment.zip HEAD
```

---

## 🔐 Security Check

### Code Security
- [ ] DEBUG = False in production (.env)
- [ ] SECRET_KEY will be generated new for production
- [ ] No hardcoded passwords in code
- [ ] No API keys in code
- [ ] .env in .gitignore

### File Permissions (will set on server)
- [ ] Directories: 755
- [ ] Files: 644
- [ ] manage.py: 755

### Sensitive Data
- [ ] No customer data in code
- [ ] No real emails in fixtures
- [ ] No production credentials in repository

---

## 📊 Performance Check

### Static Files
- [ ] CSS minified (optional)
- [ ] JavaScript minified (optional)
- [ ] Images optimized
- [ ] Cloudinary configured

### Database
- [ ] Indexes on frequently queried fields
- [ ] No N+1 query issues
- [ ] Connection pooling configured

### Caching
- [ ] Cache configuration set
- [ ] Session backend configured (db)

---

## 📝 Documentation Check

### Deployment Guides
- [ ] CPANEL_DEPLOYMENT_READY.md reviewed
- [ ] POSTGRESQL_SETUP_GUIDE.md reviewed
- [ ] Environment variables documented

### Credentials Prepared
- [ ] cPanel login ready
- [ ] Cloudinary credentials ready
- [ ] Domain name ready (if applicable)
- [ ] Admin credentials decided

---

## 🚀 Ready for Deployment

### Final Verification
```bash
# Run all checks
python verify_deployment_ready.py

# Expected output:
# ✓ All required files present
# ✓ All required directories present
# ✓ Configuration files complete
# ✓ Database migrations ready
# Status: READY FOR DEPLOYMENT
```

### Deployment Steps Preview
1. Upload files to cPanel
2. Create PostgreSQL database
3. Create .env file on server
4. Install dependencies
5. Run migrations
6. Collect static files
7. Create superuser
8. Test and go live

---

## 📋 Deployment Day Checklist

### Before Upload
- [ ] Backup current production (if updating)
- [ ] Notify users of maintenance (if applicable)
- [ ] Set maintenance mode (if applicable)

### During Upload
- [ ] Upload all files
- [ ] Verify file structure
- [ ] Set file permissions
- [ ] Create .env file

### After Upload
- [ ] Test database connection
- [ ] Run migrations
- [ ] Collect static files
- [ ] Create superuser
- [ ] Test all features
- [ ] Monitor error logs

### Go Live
- [ ] Remove maintenance mode
- [ ] Test from different devices
- [ ] Monitor for errors
- [ ] Notify users (if applicable)

---

## 🆘 Rollback Plan

### If Issues Occur
1. Check error logs: `tail -f ~/logs/error_log`
2. Review Django logs
3. Check database connection
4. Verify .env configuration
5. Restore from backup if needed

### Rollback Commands
```bash
# Restore database backup
psql -U user dbname < backup.sql

# Restore files
# (restore from backup)

# Restart application
touch ~/jewellery_site/tmp/restart.txt
```

---

## ✅ Post-Deployment Verification

### Functionality Tests
- [ ] Homepage loads
- [ ] Products display
- [ ] Cart works
- [ ] Checkout works
- [ ] MyAdmin login works
- [ ] All admin features work

### Performance Tests
- [ ] Page load times acceptable (<2s)
- [ ] Images load from Cloudinary
- [ ] Static files load correctly
- [ ] No console errors

### Security Tests
- [ ] HTTPS working
- [ ] Secure cookies set
- [ ] Admin panel protected
- [ ] No sensitive data exposed

### Monitoring
- [ ] Error logs clean
- [ ] No database errors
- [ ] Session management working
- [ ] Cart persistence working

---

## 📞 Support Contacts

### If You Need Help
- cPanel support: [Your hosting provider]
- Django documentation: https://docs.djangoproject.com
- PostgreSQL documentation: https://www.postgresql.org/docs/

### Useful Commands Reference
```bash
# Restart application
touch ~/jewellery_site/tmp/restart.txt

# View error logs
tail -f ~/logs/error_log

# Django shell
python manage.py shell

# Database shell
python manage.py dbshell

# Clear sessions
python manage.py clearsessions
```

---

## 🎉 Success Criteria

Your deployment is successful when:
- ✅ Website accessible via domain
- ✅ All pages load without errors
- ✅ Cart system works perfectly
- ✅ Orders are created successfully
- ✅ MyAdmin panel fully functional
- ✅ No errors in logs
- ✅ Performance acceptable
- ✅ Mobile responsive

---

**Ready to deploy?** Follow these steps:
1. ✅ Complete this checklist
2. ✅ Run cleanup script
3. ✅ Verify everything
4. ✅ Follow CPANEL_DEPLOYMENT_READY.md
5. ✅ Deploy and test!

**Good luck with your deployment! 🚀**
