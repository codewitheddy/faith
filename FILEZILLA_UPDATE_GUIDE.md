# FileZilla Update Guide for cPanel Django Site

## 📋 Quick Reference

### What You Need
- FileZilla Client installed
- cPanel FTP credentials
- Modified files ready to upload

---

## 🔧 Step 1: Get FTP Credentials from cPanel

### Option A: Use cPanel FTP Account
1. Log into cPanel
2. Go to **Files → FTP Accounts**
3. Use existing FTP account or create new one
4. Note down:
   - **FTP Server**: Usually `ftp.yourdomain.com` or your server IP
   - **Username**: Your FTP username
   - **Password**: Your FTP password
   - **Port**: 21 (FTP) or 22 (SFTP - recommended)

### Option B: Use Main cPanel Account (Recommended)
- **Host**: `ftp.yourdomain.com` or server IP
- **Username**: Your cPanel username
- **Password**: Your cPanel password
- **Port**: 21 (FTP) or 22 (SFTP)

---

## 🚀 Step 2: Connect with FileZilla

### Open FileZilla
1. Launch FileZilla
2. Click **File → Site Manager** (or Ctrl+S)

### Add New Site
1. Click **New Site** button
2. Enter site name (e.g., "My Django Site")

### Configure Connection

#### For SFTP (Secure - Recommended)
```
Protocol: SFTP - SSH File Transfer Protocol
Host: yourdomain.com (or server IP)
Port: 22
Logon Type: Normal
User: your_cpanel_username
Password: your_cpanel_password
```

#### For FTP (Standard)
```
Protocol: FTP - File Transfer Protocol
Host: ftp.yourdomain.com
Port: 21
Encryption: Use explicit FTP over TLS if available
Logon Type: Normal
User: your_ftp_username
Password: your_ftp_password
```

### Connect
1. Click **Connect**
2. If prompted about unknown host key (SFTP), click **OK** to trust
3. You should now see your server files on the right side

---

## 📁 Step 3: Navigate to Your Django Project

### Find Your Project Directory
1. In the **Remote site** panel (right side), navigate to:
   ```
   /home/your_username/jewellery_site/
   ```
   or wherever you deployed your Django project

2. You should see folders like:
   ```
   jewellery_site/
   shop/
   static/
   manage.py
   passenger_wsgi.py
   requirements.txt
   ```

---

## 📤 Step 4: Upload Modified Files

### For the AJAX Category Filter Fix

#### Files to Upload:
1. **shop/views.py**
2. **shop/templates/home.html**
3. **shop/templates/partials/products_grid.html** (new file)

### Upload Process

#### Method 1: Drag and Drop
1. **Local site** (left): Navigate to your project folder on your computer
2. **Remote site** (right): Navigate to the same folder on server
3. Drag files from left to right
4. Confirm overwrite when prompted

#### Method 2: Right-Click Upload
1. In **Local site** (left), navigate to the file
2. Right-click the file
3. Select **Upload**
4. Confirm overwrite

### Upload Each File:

#### 1. Upload shop/views.py
```
Local:  D:\Nira Jewelery\shop\views.py
Remote: /home/username/jewellery_site/shop/views.py
```
- Navigate to `shop/` folder on both sides
- Upload `views.py`
- Confirm overwrite

#### 2. Upload shop/templates/home.html
```
Local:  D:\Nira Jewelery\shop\templates\home.html
Remote: /home/username/jewellery_site/shop/templates/home.html
```
- Navigate to `shop/templates/` folder
- Upload `home.html`
- Confirm overwrite

#### 3. Create and Upload shop/templates/partials/products_grid.html
```
Local:  D:\Nira Jewelery\shop\templates\partials\products_grid.html
Remote: /home/username/jewellery_site/shop/templates/partials/products_grid.html
```
- On remote side, create `partials` folder if it doesn't exist:
  - Right-click in `templates/` folder
  - Select **Create directory**
  - Name it `partials`
- Upload `products_grid.html` to the `partials/` folder

---

## 🔄 Step 5: Restart Your Application

### Option A: Via cPanel (Recommended)
1. Log into cPanel
2. Go to **Setup Python App**
3. Find your application
4. Click **Restart** button

### Option B: Via FileZilla (Create restart file)
1. Navigate to your project root: `/home/username/jewellery_site/`
2. Create folder `tmp` if it doesn't exist:
   - Right-click → **Create directory** → Name: `tmp`
3. Inside `tmp` folder, create empty file `restart.txt`:
   - Right-click → **Create file** → Name: `restart.txt`
4. Or update timestamp of existing `restart.txt`:
   - Right-click `restart.txt` → **Delete**
   - Right-click → **Create file** → Name: `restart.txt`

---

## ✅ Step 6: Verify Upload

### Check Files Were Uploaded
1. In FileZilla, navigate to each uploaded file
2. Check **Size** and **Modified** date match your local files
3. Right-click file → **View/Edit** to verify content (optional)

### Test on Website
1. Open your website in browser
2. Clear browser cache (Ctrl+Shift+Delete)
3. Test category filtering
4. Should now work smoothly without page reload

---

## 🎯 Quick Update Workflow

### For Future Updates:

1. **Connect to Server**
   - Open FileZilla
   - Click on your saved site
   - Click **Connect**

2. **Navigate to Project**
   - Remote: `/home/username/jewellery_site/`

3. **Upload Modified Files**
   - Drag and drop changed files
   - Confirm overwrite

4. **Restart Application**
   - Create/update `tmp/restart.txt`
   - Or use cPanel restart button

5. **Test**
   - Clear browser cache
   - Test changes on website

---

## 🔍 Troubleshooting

### Can't Connect
**Issue**: Connection refused or timeout

**Solutions**:
- Check host address (try server IP instead of domain)
- Verify port (21 for FTP, 22 for SFTP)
- Check firewall isn't blocking FileZilla
- Try FTP instead of SFTP or vice versa
- Contact hosting provider for correct FTP details

### Wrong Directory
**Issue**: Can't find project files

**Solutions**:
- Look in `/home/username/` directory
- Check `/home/username/public_html/`
- Ask hosting provider for correct path
- Use cPanel File Manager to find project location

### Permission Denied
**Issue**: Can't upload or overwrite files

**Solutions**:
- Check file permissions (should be 644 for files, 755 for directories)
- Make sure you're using correct FTP account
- Try using main cPanel account instead of FTP sub-account
- Contact hosting provider if permissions are locked

### Upload Fails
**Issue**: Upload starts but fails

**Solutions**:
- Check internet connection
- Try uploading smaller files first
- Use **Transfer → Transfer Type → Binary** for Python files
- Disable antivirus temporarily
- Try different transfer mode (Active/Passive)

### Changes Not Showing
**Issue**: Uploaded files but website unchanged

**Solutions**:
1. **Restart application**:
   ```
   Create/update: /home/username/jewellery_site/tmp/restart.txt
   ```

2. **Clear browser cache**:
   - Chrome: Ctrl+Shift+Delete
   - Firefox: Ctrl+Shift+Delete
   - Or use Incognito/Private mode

3. **Check file was actually uploaded**:
   - Verify file size and date in FileZilla
   - View file content to confirm

4. **Check for Python errors**:
   - SSH into server: `tail -f ~/logs/error_log`
   - Or check cPanel error logs

---

## 📊 FileZilla Settings for Best Performance

### Transfer Settings
1. **Edit → Settings → Transfers**
2. Set **Maximum simultaneous transfers**: 2-3
3. Enable **Use multiple connections for transfers**

### Connection Settings
1. **Edit → Settings → Connection**
2. Set **Timeout**: 60 seconds
3. Set **Number of retries**: 3

### FTP Settings (if using FTP)
1. **Edit → Settings → FTP**
2. Set **Transfer mode**: Passive (recommended)
3. If passive doesn't work, try Active

---

## 🎨 FileZilla Interface Guide

### Left Side (Local Site)
- Your computer files
- Navigate like Windows Explorer
- Shows your project files

### Right Side (Remote Site)
- Server files (cPanel)
- Your Django project on server
- Where you upload to

### Bottom Panel
- Transfer queue
- Shows upload/download progress
- Failed transfers

### Top Panel
- Quick connect bar
- Host, Username, Password, Port
- Connect button

---

## 📝 Files to Upload for Category Filter Fix

### Required Files (3 files):
```
✓ shop/views.py
✓ shop/templates/home.html
✓ shop/templates/partials/products_grid.html (new)
```

### Upload Locations:
```
Local → Remote

shop/views.py 
→ /home/username/jewellery_site/shop/views.py

shop/templates/home.html 
→ /home/username/jewellery_site/shop/templates/home.html

shop/templates/partials/products_grid.html 
→ /home/username/jewellery_site/shop/templates/partials/products_grid.html
```

---

## ⚡ Quick Commands

### Create Directory
- Right-click in remote panel → **Create directory**

### Create File
- Right-click in remote panel → **Create file**

### Delete File
- Right-click file → **Delete**

### Rename File
- Right-click file → **Rename**

### View/Edit File
- Right-click file → **View/Edit**
- Opens in default text editor
- Save and close to upload changes

### Download File
- Drag from right (remote) to left (local)
- Or right-click → **Download**

### Upload File
- Drag from left (local) to right (remote)
- Or right-click → **Upload**

---

## 🔐 Security Tips

### Use SFTP Instead of FTP
- More secure (encrypted)
- Port 22 instead of 21
- Same credentials as SSH

### Save Password Securely
- FileZilla can save passwords
- Or use password manager
- Don't share FTP credentials

### Use Strong Passwords
- Change default passwords
- Use unique password for FTP
- Enable 2FA on cPanel if available

---

## 📱 Alternative: cPanel File Manager

If FileZilla doesn't work, use cPanel File Manager:

1. Log into cPanel
2. Go to **Files → File Manager**
3. Navigate to your project
4. Click **Upload** button
5. Select files to upload
6. Confirm overwrite
7. Restart application

---

## ✅ Post-Update Checklist

After uploading files:

- [ ] All 3 files uploaded successfully
- [ ] File sizes match local files
- [ ] Application restarted (tmp/restart.txt created)
- [ ] Browser cache cleared
- [ ] Website tested
- [ ] Category filtering works smoothly
- [ ] No JavaScript errors in console
- [ ] Cart still works
- [ ] Products display correctly

---

## 🎉 Summary

### To Update Your Site:
1. **Connect**: Open FileZilla, connect to your server
2. **Navigate**: Go to `/home/username/jewellery_site/`
3. **Upload**: Drag modified files from left to right
4. **Restart**: Create/update `tmp/restart.txt`
5. **Test**: Clear cache and test website

### Time Required:
- First time: 10-15 minutes
- Future updates: 2-3 minutes

### Files for This Update:
- shop/views.py
- shop/templates/home.html
- shop/templates/partials/products_grid.html

**You're ready to update your site!** 🚀
