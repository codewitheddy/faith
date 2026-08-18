#!/usr/bin/env python
"""
Test email configuration and sending functionality
Run with: python manage.py shell < test_email.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jewellery_site.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings
from shop.models import Order, OrderItem, Product
from shop.email_utils import send_order_confirmation_email, send_order_completion_email

print("=" * 70)
print("EMAIL CONFIGURATION TEST")
print("=" * 70)

# Test 1: Email settings
print("\n1. EMAIL SETTINGS:")
print(f"   EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"   EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"   EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
print(f"   EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"   DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

# Test 2: Test connection with simple email
print("\n2. TESTING SMTP CONNECTION:")
try:
    send_mail(
        subject='Test Email from Wyatt Collection',
        message='This is a test email to verify SMTP configuration is working.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.EMAIL_HOST_USER],  # Send to self for testing
        fail_silently=False,
    )
    print("   ✓ Test email sent successfully!")
except Exception as e:
    print(f"   ✗ Failed to send test email: {str(e)}")

# Test 3: Test order confirmation email template
print("\n3. TESTING ORDER CONFIRMATION EMAIL TEMPLATE:")
try:
    # Get the most recent order or create a test one
    orders = Order.objects.all().order_by('-created_at')
    if orders.exists():
        order = orders.first()
        print(f"   Using order: {order.order_number}")
        result = send_order_confirmation_email(order)
        if result:
            print(f"   ✓ Confirmation email sent to {order.customer_email}")
        else:
            print(f"   ✗ Failed to send confirmation email")
    else:
        print("   ⚠ No orders found in database for testing")
except Exception as e:
    print(f"   ✗ Error testing confirmation email: {str(e)}")

# Test 4: Test order completion email template
print("\n4. TESTING ORDER COMPLETION EMAIL TEMPLATE:")
try:
    orders = Order.objects.all().order_by('-created_at')
    if orders.exists():
        order = orders.first()
        print(f"   Using order: {order.order_number}")
        result = send_order_completion_email(order)
        if result:
            print(f"   ✓ Completion email sent to {order.customer_email}")
        else:
            print(f"   ✗ Failed to send completion email")
    else:
        print("   ⚠ No orders found in database for testing")
except Exception as e:
    print(f"   ✗ Error testing completion email: {str(e)}")

print("\n" + "=" * 70)
print("EMAIL SETUP COMPLETE!")
print("=" * 70)
print("\nNext Steps:")
print("1. Update your .env file with the following variables:")
print(f"   EMAIL_HOST_USER=info@wyatt.co.ke")
print(f"   EMAIL_HOST_PASSWORD=[your_cpanel_email_password]")
print("2. Test by placing a regular checkout order")
print("3. Check customer email for confirmation")
print("4. In admin panel, mark order as 'delivered'")
print("5. Customer should receive completion email")
print("=" * 70)
