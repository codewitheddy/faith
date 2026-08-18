#!/bin/bash

# Quick cPanel Deployment Script for Django App
# Usage: bash deploy.sh

set -e  # Exit on error

echo "=========================================="
echo "WYATT COLLECTION - cPanel Deployment"
echo "=========================================="
echo ""

# Get current directory
PROJECT_ROOT=$(pwd)
echo "Project root: $PROJECT_ROOT"
echo ""

# Step 1: Activate Virtual Environment
echo "[1/7] Activating virtual environment..."
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "✗ Virtual environment not found!"
    echo "Creating new virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ Virtual environment created and activated"
fi
echo ""

# Step 2: Pull Latest Code from GitHub
echo "[2/7] Pulling latest code from GitHub..."
git pull origin main
echo "✓ Code updated from GitHub"
echo ""

# Step 3: Install/Update Dependencies
echo "[3/7] Installing Python dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo "✓ Dependencies installed"
echo ""

# Step 4: Run Database Migrations
echo "[4/7] Running database migrations..."
python manage.py migrate
echo "✓ Migrations completed"
echo ""

# Step 5: Collect Static Files
echo "[5/7] Collecting static files..."
python manage.py collectstatic --noinput > /dev/null 2>&1
echo "✓ Static files collected"
echo ""

# Step 6: Check Configuration
echo "[6/7] Verifying configuration..."
if [ -f ".env" ]; then
    echo "✓ .env file found"
else
    echo "⚠ .env file not found - make sure to create it!"
    echo "  Copy .env.example and configure with your settings"
fi
echo ""

# Step 7: Restart Application
echo "[7/7] Restarting Passenger application..."
touch jewellery_site/wsgi.py
echo "✓ Application restarted"
echo ""

echo "=========================================="
echo "✓ DEPLOYMENT COMPLETE!"
echo "=========================================="
echo ""
echo "Your site should be live at:"
echo "  https://wyatt.co.ke"
echo ""
echo "Admin panel at:"
echo "  https://wyatt.co.ke/admin/"
echo ""
echo "Next steps:"
echo "1. Visit your website to verify it's working"
echo "2. Check logs for any errors: tail -f logs/myadmin.log"
echo "3. Test email: python manage.py send_test_email --to your-email@example.com"
echo ""
echo "For issues, check error_log:"
echo "  tail -50 error_log"
echo ""
