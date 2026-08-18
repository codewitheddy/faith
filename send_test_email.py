#!/usr/bin/env python
"""
Send a simple test email to verify cPanel email configuration
Run with: python manage.py shell < send_test_email.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jewellery_site.settings')
django.setup()

from django.core.mail import EmailMultiAlternatives
from django.conf import settings

print("=" * 70)
print("SENDING TEST EMAIL")
print("=" * 70)

# Email configuration
subject = "Test Email - Wyatt Collection"
recipient_email = "edwinmuliro64@gmail.com"

# HTML content
html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; background: #f9f9f9; }
        .header { background: #0f3460; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }
        .content { background: white; padding: 30px; border-radius: 0 0 5px 5px; }
        .success { background: #e8f5e9; padding: 15px; border-left: 4px solid #2e7d32; margin: 20px 0; border-radius: 3px; }
        .footer { text-align: center; padding: 20px; color: #666; font-size: 12px; border-top: 1px solid #eee; margin-top: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✓ Test Email Success!</h1>
        </div>
        
        <div class="content">
            <p>Hello Edwin,</p>
            
            <div class="success">
                <strong>✓ Email system is working!</strong><br>
                Your cPanel email (info@wyatt.co.ke) is properly configured with Django.
            </div>
            
            <p>This is a test email from <strong>Wyatt Collection</strong> to verify that:</p>
            <ul>
                <li>✓ Django email backend is configured correctly</li>
                <li>✓ SMTP connection to mail.wyatt.co.ke:465 is working</li>
                <li>✓ Emails can be sent to external addresses</li>
                <li>✓ HTML formatting is rendering properly</li>
            </ul>
            
            <p><strong>Email Configuration Details:</strong></p>
            <ul>
                <li>From: info@wyatt.co.ke</li>
                <li>SMTP Host: mail.wyatt.co.ke</li>
                <li>SMTP Port: 465 (SSL)</li>
                <li>Status: ✓ Active</li>
            </ul>
            
            <p style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; color: #666; font-size: 12px;">
                This confirms that order confirmation and completion emails will now be automatically sent to customers when:
                <br>1. They place an order (confirmation)
                <br>2. You mark their order as delivered (completion)
            </p>
        </div>
        
        <div class="footer">
            <p><strong>Wyatt Collection</strong></p>
            <p>Premium Menswear | Kenya 🇰🇪</p>
            <p>Email System Fully Operational</p>
        </div>
    </div>
</body>
</html>
"""

# Plain text fallback
text_content = """
Test Email - Wyatt Collection

✓ Email system is working!

Your cPanel email (info@wyatt.co.ke) is properly configured with Django.

This is a test email from Wyatt Collection to verify that:
✓ Django email backend is configured correctly
✓ SMTP connection to mail.wyatt.co.ke:465 is working
✓ Emails can be sent to external addresses
✓ HTML formatting is rendering properly

Email Configuration Details:
- From: info@wyatt.co.ke
- SMTP Host: mail.wyatt.co.ke
- SMTP Port: 465 (SSL)
- Status: ✓ Active

This confirms that order confirmation and completion emails will now be automatically sent to customers when:
1. They place an order (confirmation)
2. You mark their order as delivered (completion)

---
Wyatt Collection
Premium Menswear | Kenya 🇰🇪
Email System Fully Operational
"""

try:
    print(f"\nSending to: {recipient_email}")
    print(f"From: {settings.DEFAULT_FROM_EMAIL}")
    print(f"SMTP Host: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
    
    # Create email
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient_email],
    )
    email.attach_alternative(html_content, "text/html")
    
    # Send
    result = email.send(fail_silently=False)
    
    print("\n" + "=" * 70)
    print("✓ TEST EMAIL SENT SUCCESSFULLY!")
    print("=" * 70)
    print(f"\n✓ Email sent to: {recipient_email}")
    print(f"✓ From: {settings.DEFAULT_FROM_EMAIL}")
    print(f"✓ Subject: {subject}")
    print("\nCheck your inbox (and spam folder) for the test email.")
    print("\nIf you received this, the email system is fully operational!")
    print("=" * 70)
    
except Exception as e:
    print("\n" + "=" * 70)
    print("✗ FAILED TO SEND EMAIL")
    print("=" * 70)
    print(f"\nError: {str(e)}")
    print(f"Error Type: {type(e).__name__}")
    
    print("\nTroubleshooting steps:")
    print("1. Verify EMAIL_HOST_PASSWORD is set in .env file")
    print("2. Check that mail.wyatt.co.ke is accessible")
    print("3. Verify firewall allows port 465")
    print("4. Check EMAIL_HOST_USER matches (info@wyatt.co.ke)")
    print("\nEmail Configuration Current Values:")
    print(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"  EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
    print(f"  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"  DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print("=" * 70)
