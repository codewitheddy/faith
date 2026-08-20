"""Email utilities for sending order notifications"""
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def _fmt(value):
    """Format a number with comma thousands separator, no decimals."""
    try:
        return f"{float(value):,.0f}"
    except (TypeError, ValueError):
        return str(value)


def send_order_confirmation_email(order):
    """
    Send order confirmation email to customer
    
    Args:
        order: Order instance
    """
    try:
        # Prepare order items for template
        items = []
        total_savings = 0
        for order_item in order.items.all():
            product_name = order_item.product.name if order_item.product else "[Deleted Product]"
            current_price = float(order_item.price)
            original_price = float(order_item.product.price) if order_item.product else current_price
            
            # Check if product is on sale
            is_on_sale = order_item.product.on_sale if order_item.product else False
            discount_percent = order_item.product.discount_percent if order_item.product and is_on_sale else 0
            
            # Calculate savings
            savings = 0
            if is_on_sale and discount_percent > 0:
                savings = (original_price - current_price) * order_item.quantity
                total_savings += savings
            
            subtotal = float(order_item.price * order_item.quantity)
            items.append({
                'name': product_name,
                'quantity': order_item.quantity,
                'price': current_price,
                'price_fmt': _fmt(current_price),
                'original_price': original_price,
                'original_price_fmt': _fmt(original_price),
                'is_on_sale': is_on_sale,
                'discount_percent': discount_percent,
                'subtotal': subtotal,
                'subtotal_fmt': _fmt(subtotal),
                'savings': savings,
            })
        
        context = {
            'customer_name': order.customer_name,
            'order_number': order.order_number,
            'order_date': order.created_at.strftime('%d %B %Y'),
            'items': items,
            'total': float(order.total_amount),
            'total_fmt': _fmt(order.total_amount),
            'total_savings': total_savings,
            'total_savings_fmt': _fmt(total_savings),
            'address': order.customer_address,
            'city': order.city if hasattr(order, 'city') else 'N/A',
            'phone': order.customer_phone,
        }
        
        # Render HTML template
        html_content = render_to_string('emails/order_confirmation.html', context)
        text_content = strip_tags(html_content)
        
        # Create email
        subject = f'Order Confirmation - Wyatt Collection #{order.order_number}'
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.customer_email],
        )
        email.attach_alternative(html_content, "text/html")
        
        # Send email
        email.send(fail_silently=False)
        
        logger.info(f"Order confirmation email sent to {order.customer_email} for order #{order.order_number}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send order confirmation email for order #{order.order_number}: {str(e)}")
        return False


def send_order_completion_email(order):
    """
    Send order completion email to customer
    
    Args:
        order: Order instance
    """
    try:
        # Prepare order items for template
        items = []
        total_savings = 0
        for order_item in order.items.all():
            product_name = order_item.product.name if order_item.product else "[Deleted Product]"
            current_price = float(order_item.price)
            original_price = float(order_item.product.price) if order_item.product else current_price
            
            # Check if product is on sale
            is_on_sale = order_item.product.on_sale if order_item.product else False
            discount_percent = order_item.product.discount_percent if order_item.product and is_on_sale else 0
            
            # Calculate savings
            savings = 0
            if is_on_sale and discount_percent > 0:
                savings = (original_price - current_price) * order_item.quantity
                total_savings += savings
            
            subtotal = float(order_item.price * order_item.quantity)
            items.append({
                'name': product_name,
                'quantity': order_item.quantity,
                'price': current_price,
                'price_fmt': _fmt(current_price),
                'original_price': original_price,
                'original_price_fmt': _fmt(original_price),
                'is_on_sale': is_on_sale,
                'discount_percent': discount_percent,
                'subtotal': subtotal,
                'subtotal_fmt': _fmt(subtotal),
                'savings': savings,
            })
        
        context = {
            'customer_name': order.customer_name,
            'order_number': order.order_number,
            'completion_date': order.updated_at.strftime('%d %B %Y') if order.updated_at else 'Today',
            'items': items,
            'total': float(order.total_amount),
            'total_fmt': _fmt(order.total_amount),
            'total_savings': total_savings,
            'total_savings_fmt': _fmt(total_savings),
        }
        
        # Render HTML template
        html_content = render_to_string('emails/order_completed.html', context)
        text_content = strip_tags(html_content)
        
        # Create email
        subject = f'Order Delivered - Wyatt Collection #{order.order_number}'
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.customer_email],
        )
        email.attach_alternative(html_content, "text/html")
        
        # Send email
        email.send(fail_silently=False)
        
        logger.info(f"Order completion email sent to {order.customer_email} for order #{order.order_number}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send order completion email for order #{order.order_number}: {str(e)}")
        return False
