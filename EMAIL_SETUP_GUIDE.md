# Email Notification Setup Guide - Wyatt Collection

## Overview
This guide explains how to set up email notifications for customer order confirmations and completion emails using your cPanel email account (info@wyatt.co.ke).

## Configuration Files Modified

### 1. **jewellery_site/settings.py**
Added email backend configuration:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.wyatt.co.ke'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'info@wyatt.co.ke'
EMAIL_HOST_PASSWORD = '[set via environment variable]'
DEFAULT_FROM_EMAIL = 'info@wyatt.co.ke'
SERVER_EMAIL = 'info@wyatt.co.ke'
```

## Setup Instructions

### Step 1: Create .env File (if not exists)
Create or update `g:\Myshop\.env` with:
```
EMAIL_HOST_USER=info@wyatt.co.ke
EMAIL_HOST_PASSWORD=your_cpanel_email_password_here
```

⚠️ **IMPORTANT**: Replace `your_cpanel_email_password_here` with your actual cPanel email password from:
- Username: `info@wyatt.co.ke`
- Password: [Use the email account's password]

### Step 2: Verify SMTP Settings
Your cPanel email settings:
- **Incoming Server**: mail.wyatt.co.ke (IMAP Port: 993, POP3 Port: 995)
- **Outgoing Server**: mail.wyatt.co.ke (SMTP Port: 465, requires authentication)
- **SSL/TLS**: Required for port 465

## Files Created/Modified

### New Files
1. **shop/email_utils.py** - Email utility functions
   - `send_order_confirmation_email(order)` - Sends when order is placed
   - `send_order_completion_email(order)` - Sends when order status = 'delivered'

2. **shop/templates/emails/order_confirmation.html** - Order confirmation template
   - Customer details
   - Order items with prices
   - Total amount
   - Payment methods info

3. **shop/templates/emails/order_completed.html** - Order completion template
   - Order summary
   - Thank you message
   - Contact information for feedback

### Modified Files
1. **jewellery_site/settings.py** - Added email configuration
2. **shop/views.py** - Import and call `send_order_confirmation_email()` after checkout
3. **shop/models.py** - Modified `Order.save()` to detect status change to 'delivered'

## Email Flow

### Confirmation Email (On Order Placement)
```
Order Placement (Checkout)
    ↓
Order created in database
    ↓
send_order_confirmation_email(order) called
    ↓
Email sent to customer_email
    ↓
Customer receives: "Order Confirmation - Wyatt Collection #ORD-..."
```

### Completion Email (On Order Delivery)
```
Admin marks order as 'Delivered'
    ↓
Order.save() called
    ↓
Status changed from 'pending/confirmed/etc' to 'delivered'
    ↓
send_order_completion_email(order) called
    ↓
Email sent to customer_email
    ↓
Customer receives: "Order Delivered - Wyatt Collection #ORD-..."
```

## Testing

### Option 1: Using Django Shell
```bash
cd g:\Myshop
python manage.py shell

# Then paste:
from shop.models import Order
from shop.email_utils import send_order_confirmation_email

order = Order.objects.latest('created_at')
send_order_confirmation_email(order)
```

### Option 2: Using Test Script
```bash
cd g:\Myshop
python manage.py shell
exec(open('test_email.py').read())
```

### Option 3: Live Testing
1. Create a test account
2. Place an order via regular checkout (not WhatsApp)
3. Check test email inbox for confirmation
4. Go to admin panel: `/admin/shop/order/`
5. Select order and change status to "Delivered"
6. Save
7. Check test email inbox for completion email

## Troubleshooting

### Issue: "SMTPAuthenticationError"
**Solution**: Check that EMAIL_HOST_PASSWORD is correct in .env file

### Issue: "SMTPNotSupportedError"
**Solution**: Verify EMAIL_PORT is 465 and EMAIL_USE_SSL is True

### Issue: "Connection refused"
**Solution**: Verify EMAIL_HOST is correct: `mail.wyatt.co.ke`

### Issue: Email not sending but no errors
**Solution**: Check Django logs:
```bash
tail logs/myadmin.log | grep -i email
```

## Email Variables Available in Templates

### order_confirmation.html
- `customer_name` - Full name
- `order_number` - Order ID (e.g., ORD-20260817-0001)
- `order_date` - Created date
- `items` - List of order items with name, quantity, price, subtotal
- `total` - Total amount
- `address` - Delivery address
- `city` - City
- `phone` - Customer phone

### order_completed.html
- `customer_name` - Full name
- `order_number` - Order ID
- `completion_date` - Updated date
- `items` - List of order items
- `total` - Total amount

## Email Content

### Order Confirmation
- ✓ Order number and date
- ✓ Status badge (CONFIRMED)
- ✓ Itemized product list with prices
- ✓ Total amount
- ✓ Delivery address
- ✓ Payment methods (M-Pesa, Bank, COD)
- ✓ Contact information
- ✓ Branded header/footer

### Order Completion
- ✓ Order number and completion date
- ✓ Status badge (COMPLETED)
- ✓ Order summary
- ✓ Thank you message
- ✓ Request for feedback
- ✓ Contact information
- ✓ Branded header/footer

## Admin Panel Integration

### Sending Completion Email
1. Login to admin: `/admin/`
2. Navigate to Orders: `/admin/shop/order/`
3. Click on any order
4. Change Status dropdown to "Delivered"
5. Click "Save"
6. Completion email automatically sends to customer

## Security Notes

⚠️ **Important Security Reminders:**
- Never commit `.env` file to version control
- Keep EMAIL_HOST_PASSWORD secure
- Use environment variables for all sensitive data
- Verify SSL certificates when connecting to mail.wyatt.co.ke

## Monitoring

Monitor email sending in logs:
```bash
# View email-related logs
grep -i "email\|confirmation\|completion" logs/myadmin.log

# Watch logs in real-time
tail -f logs/myadmin.log | grep -i email
```

## Success Indicators

✓ Test email sends without errors
✓ Confirmation email received after checkout
✓ Email has proper formatting and branding
✓ Completion email sends when status changes
✓ All links and contact info are correct

## Next Steps

1. ✓ Configure .env with email credentials
2. ✓ Test SMTP connection
3. ✓ Place test order and verify confirmation email
4. ✓ Mark order as delivered and verify completion email
5. ✓ Monitor logs for any issues
6. ✓ Inform customers about email notifications

## Support

For issues:
1. Check Django logs in `logs/myadmin.log`
2. Verify cPanel email credentials
3. Test SMTP connection manually
4. Check firewall/network access to mail.wyatt.co.ke:465

---

**Last Updated**: August 17, 2026
**System**: Wyatt Collection Django E-Commerce
