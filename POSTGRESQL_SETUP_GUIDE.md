# PostgreSQL Database Setup Guide

## ✅ Current Configuration Status

Your Django project is **already configured** to use PostgreSQL! The database configuration uses `dj-database-url` which automatically parses the `DATABASE_URL` environment variable.

---

## 🔧 Database Configuration

### Current Setup (jewellery_site/settings.py)

```python
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default=f'sqlite:///{BASE_DIR / "db.sqlite3"}'),
        conn_max_age=600,  # Connection pooling - 10 minutes
        conn_health_checks=True,  # Health checks before reusing connections
    )
}
```

### Features Enabled
- ✅ **Connection Pooling**: Keeps connections alive for 10 minutes (improves performance)
- ✅ **Health Checks**: Validates connections before reuse (prevents stale connections)
- ✅ **Automatic Parsing**: Supports PostgreSQL, MySQL, SQLite via DATABASE_URL
- ✅ **Fallback**: Uses SQLite for local development if DATABASE_URL not set

---

## 📋 PostgreSQL Setup on cPanel

### Step 1: Create PostgreSQL Database

1. **Log into cPanel**
2. **Navigate to**: Databases → PostgreSQL Databases
3. **Create New Database**:
   - Database Name: `jewellery_db` (or your preferred name)
   - Click "Create Database"
   - **Note**: cPanel will prefix it with your username (e.g., `username_jewellery_db`)

### Step 2: Create Database User

1. **In the same PostgreSQL Databases section**
2. **Create New User**:
   - Username: `jewellery_user` (or your preferred name)
   - Password: Generate a strong password (use cPanel's password generator)
   - **Note**: cPanel will prefix it with your username (e.g., `username_jewellery_user`)
   - **Save the password securely!**

### Step 3: Add User to Database

1. **In the "Add User To Database" section**
2. **Select**:
   - User: `username_jewellery_user`
   - Database: `username_jewellery_db`
3. **Click "Add"**
4. **Grant Privileges**:
   - Check "ALL PRIVILEGES"
   - Click "Make Changes"

### Step 4: Note Your Credentials

After setup, you'll have:
```
Database Name: username_jewellery_db
Database User: username_jewellery_user
Database Password: [the password you created]
Database Host: localhost
Database Port: 5432 (default PostgreSQL port)
```

---

## 🔐 Configure Environment Variables

### Create .env File on Server

After uploading your project to cPanel, create `.env` file:

```env
# Django Core
SECRET_KEY=<generate-new-secret-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# PostgreSQL Database
DATABASE_URL=postgresql://username_jewellery_user:your_password_here@localhost:5432/username_jewellery_db

# Cloudinary
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### DATABASE_URL Format

```
postgresql://[user]:[password]@[host]:[port]/[database]
```

**Example**:
```
postgresql://myuser_jewellery:MyStr0ngP@ssw0rd@localhost:5432/myuser_jewellery_db
```

**Important**: 
- Replace `myuser` with your actual cPanel username
- Replace `MyStr0ngP@ssw0rd` with your actual database password
- If password contains special characters (@, :, /, etc.), URL-encode them:
  - `@` → `%40`
  - `:` → `%3A`
  - `/` → `%2F`
  - `#` → `%23`

---

## 🚀 Initialize Database

After creating the database and configuring .env:

### 1. Activate Virtual Environment
```bash
source /home/username/virtualenv/jewellery_site/3.11/bin/activate
```

### 2. Test Database Connection
```bash
python manage.py dbshell
```

If successful, you'll see PostgreSQL prompt:
```
psql (12.x)
Type "help" for help.

username_jewellery_db=>
```

Type `\q` to exit.

### 3. Run Migrations
```bash
# Check for any duplicate names first
python manage.py fix_duplicates

# Run migrations
python manage.py migrate
```

Expected output:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, shop
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  ...
  Applying shop.0004_add_unique_constraints_to_names... OK
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
```

Enter:
- Username: `admin` (or your preferred username)
- Email: your email address
- Password: strong password (will be hidden)

### 5. Verify Database
```bash
python manage.py dbshell
```

Then run:
```sql
-- List all tables
\dt

-- Check products table
SELECT COUNT(*) FROM shop_product;

-- Check categories table
SELECT COUNT(*) FROM shop_category;

-- Exit
\q
```

---

## 📊 PostgreSQL vs SQLite vs MySQL

### Why PostgreSQL? (Recommended)

| Feature | PostgreSQL | MySQL | SQLite |
|---------|-----------|-------|--------|
| **Performance** | Excellent | Good | Limited |
| **Concurrent Users** | Excellent | Good | Poor |
| **Data Integrity** | Excellent | Good | Basic |
| **JSON Support** | Native | Limited | No |
| **Full-Text Search** | Native | Basic | No |
| **Scalability** | Excellent | Good | Poor |
| **Production Ready** | ✅ Yes | ✅ Yes | ❌ No |

### PostgreSQL Advantages
- ✅ Better performance for complex queries
- ✅ Superior data integrity and ACID compliance
- ✅ Advanced features (JSON, arrays, full-text search)
- ✅ Better handling of concurrent connections
- ✅ More reliable for production workloads
- ✅ Better support for Django's advanced features

---

## 🔍 Verify PostgreSQL Setup

### Check Database Configuration
```bash
python manage.py check --database default
```

Should output:
```
System check identified no issues (0 silenced).
```

### Check Migrations Status
```bash
python manage.py showmigrations
```

Should show all migrations with `[X]` (applied):
```
admin
 [X] 0001_initial
 [X] 0002_logentry_remove_auto_add
auth
 [X] 0001_initial
 ...
shop
 [X] 0001_initial
 [X] 0002_...
 [X] 0003_...
 [X] 0004_add_unique_constraints_to_names
```

### Test Database Queries
```bash
python manage.py shell
```

Then:
```python
from shop.models import Product, Category, Order

# Check counts
print(f"Products: {Product.objects.count()}")
print(f"Categories: {Category.objects.count()}")
print(f"Orders: {Order.objects.count()}")

# Test query
products = Product.objects.filter(is_available=True)[:5]
for p in products:
    print(f"- {p.name}: Ksh {p.price}")

# Exit
exit()
```

---

## 🛠️ PostgreSQL Management Commands

### Useful Commands

```bash
# Access PostgreSQL shell
python manage.py dbshell

# Create database backup
pg_dump -U username_jewellery_user username_jewellery_db > backup.sql

# Restore database backup
psql -U username_jewellery_user username_jewellery_db < backup.sql

# Check database size
python manage.py dbshell
SELECT pg_size_pretty(pg_database_size('username_jewellery_db'));
\q
```

### PostgreSQL Shell Commands

Inside `python manage.py dbshell`:

```sql
-- List all tables
\dt

-- Describe table structure
\d shop_product

-- List all databases
\l

-- List all users
\du

-- Show current database
SELECT current_database();

-- Show current user
SELECT current_user;

-- Count records in table
SELECT COUNT(*) FROM shop_product;

-- Show table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Exit
\q
```

---

## 🔒 Security Best Practices

### 1. Strong Password
- Use at least 16 characters
- Mix uppercase, lowercase, numbers, symbols
- Use cPanel's password generator

### 2. Limited Privileges
- Only grant necessary privileges
- Don't use root/superuser for application

### 3. Connection Security
- Use localhost (not remote connections)
- Keep database on same server as application

### 4. Regular Backups
```bash
# Daily backup script
pg_dump -U username_jewellery_user username_jewellery_db > backup_$(date +%Y%m%d).sql
```

### 5. Monitor Connections
```sql
-- Check active connections
SELECT * FROM pg_stat_activity WHERE datname = 'username_jewellery_db';
```

---

## 🚨 Troubleshooting

### Issue: "FATAL: password authentication failed"

**Solution**:
1. Verify password in .env file
2. Check for special characters (URL-encode them)
3. Verify user has access to database

```bash
# Test connection manually
psql -U username_jewellery_user -d username_jewellery_db -h localhost
```

### Issue: "could not connect to server"

**Solution**:
1. Verify PostgreSQL is running
2. Check port (default: 5432)
3. Verify host is 'localhost'

```bash
# Check if PostgreSQL is running
ps aux | grep postgres
```

### Issue: "relation does not exist"

**Solution**:
Run migrations:
```bash
python manage.py migrate
```

### Issue: "too many connections"

**Solution**:
Reduce `conn_max_age` in settings.py or increase PostgreSQL max_connections:

```python
# In settings.py
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=300,  # Reduce from 600 to 300 seconds
        conn_health_checks=True,
    )
}
```

### Issue: Special Characters in Password

**Solution**:
URL-encode special characters in DATABASE_URL:

```python
# If password is: P@ssw0rd!#
# Encode as: P%40ssw0rd%21%23

DATABASE_URL=postgresql://user:P%40ssw0rd%21%23@localhost:5432/dbname
```

---

## 📈 Performance Optimization

### 1. Connection Pooling (Already Configured)
```python
conn_max_age=600  # Keep connections alive for 10 minutes
```

### 2. Database Indexes
Your models already have indexes on:
- Primary keys (automatic)
- Foreign keys (automatic)
- Unique fields (slug, name)

### 3. Query Optimization
Use `select_related()` for foreign keys (already implemented):
```python
products = Product.objects.filter(is_available=True).select_related('category')
```

### 4. Database Maintenance
```sql
-- Analyze tables (improves query planning)
ANALYZE;

-- Vacuum database (reclaim storage)
VACUUM;

-- Both together
VACUUM ANALYZE;
```

---

## 📊 Monitoring

### Check Database Performance

```sql
-- Slow queries
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Table statistics
SELECT schemaname, tablename, n_live_tup, n_dead_tup
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;

-- Index usage
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

---

## ✅ PostgreSQL Setup Checklist

- [ ] PostgreSQL database created in cPanel
- [ ] Database user created with strong password
- [ ] User added to database with ALL PRIVILEGES
- [ ] DATABASE_URL configured in .env file
- [ ] Database connection tested (`python manage.py dbshell`)
- [ ] Migrations run successfully
- [ ] Superuser created
- [ ] Database verified (tables exist, queries work)
- [ ] Backup strategy planned

---

## 🎯 Quick Reference

### DATABASE_URL Format
```
postgresql://[user]:[password]@[host]:[port]/[database]
```

### Common Commands
```bash
# Test connection
python manage.py dbshell

# Run migrations
python manage.py migrate

# Create backup
pg_dump -U user dbname > backup.sql

# Restore backup
psql -U user dbname < backup.sql
```

### PostgreSQL Shell
```sql
\dt          -- List tables
\d table     -- Describe table
\l           -- List databases
\du          -- List users
\q           -- Quit
```

---

## 📚 Additional Resources

- **PostgreSQL Documentation**: https://www.postgresql.org/docs/
- **Django Database Documentation**: https://docs.djangoproject.com/en/stable/ref/databases/
- **dj-database-url**: https://github.com/jazzband/dj-database-url

---

## 🎉 Summary

Your Django project is **ready to use PostgreSQL**! The configuration is already in place, you just need to:

1. Create PostgreSQL database in cPanel
2. Create database user
3. Configure DATABASE_URL in .env
4. Run migrations
5. Start using your production database!

PostgreSQL will provide better performance, reliability, and features compared to SQLite or MySQL for your e-commerce application.

---

**Status**: PostgreSQL Configuration Ready ✓
**Database Engine**: PostgreSQL 12+
**Connection Pooling**: Enabled (600s)
**Health Checks**: Enabled
**Production Ready**: Yes
