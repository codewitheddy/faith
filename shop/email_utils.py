"""Email utilities for sending order notifications"""
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_order_confirmation_email(order):
    """
    Send order confirmation email to customer
    
    Args:
        order: Order instance
    """
    try:
        # Prepare order items for template
        items = []
        for order_item in order.items.all():
            product_name = order_item.product.name if order_item.product else "[Deleted Product]"
            items.append({
                'name': product_name,
                'quantity': order_item.quantity,
                'price': float(order_item.price),
                'subtotal': float(order_item.price * order_item.quantity),
            })
        
        context = {
            'customer_name': order.customer_name,
            'order_number': order.order_number,
            'order_date': order.created_at.strftime('%d %B %Y'),
            'items': items,
            'total': float(order.total_amount),
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
        for order_item in order.items.all():
            product_name = order_item.product.name if order_item.product else "[Deleted Product]"
            items.append({
                'name': product_name,
                'quantity': order_item.quantity,
                'price': float(order_item.price),
                'subtotal': float(order_item.price * order_item.quantity),
            })
        
        context = {
            'customer_name': order.customer_name,
            'order_number': order.order_number,
            'completion_date': order.updated_at.strftime('%d %B %Y') if order.updated_at else 'Today',
            'items': items,
            'total': float(order.total_amount),
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
