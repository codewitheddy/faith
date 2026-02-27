"""
Custom template tags for optimized image rendering
"""
from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import locale

register = template.Library()


@register.simple_tag
def optimized_img(image_url, alt_text="", width=None, height=None, css_class="", lazy=True):
    """
    Render an optimized image with lazy loading and responsive srcset
    
    Usage:
        {% load image_tags %}
        {% optimized_img product.get_image_url product.name width=800 css_class="product-image" %}
    """
    if not image_url:
        return ""
    
    # Build image attributes
    attrs = []
    
    # Lazy loading
    if lazy:
        attrs.append('loading="lazy"')
        attrs.append('decoding="async"')
    
    # Source
    attrs.append(f'src="{image_url}"')
    
    # Alt text
    attrs.append(f'alt="{alt_text}"')
    
    # Dimensions (helps prevent layout shift)
    if width:
        attrs.append(f'width="{width}"')
    if height:
        attrs.append(f'height="{height}"')
    
    # CSS class
    if css_class:
        attrs.append(f'class="{css_class}"')
    
    # Generate HTML
    html = f'<img {" ".join(attrs)}>'
    
    return mark_safe(html)


@register.filter
def cloudinary_optimize(url, params="w_800,q_auto,f_auto"):
    """
    Add Cloudinary optimization parameters to URL
    
    Usage:
        {{ product.image_url|cloudinary_optimize:"w_400,q_auto,f_webp" }}
    """
    if not url or 'cloudinary' not in url:
        return url
    
    return url.replace('/upload/', f'/upload/{params}/')


@register.filter
def responsive_srcset(url):
    """
    Generate responsive srcset for an image
    
    Usage:
        <img srcset="{{ product.image_url|responsive_srcset }}" ...>
    """
    if not url:
        return ""
    
    if 'cloudinary' in url:
        sizes = [400, 800, 1200, 1600]
        srcset_parts = []
        for size in sizes:
            transformed = url.replace('/upload/', f'/upload/w_{size},q_auto,f_auto/')
            srcset_parts.append(f"{transformed} {size}w")
        return ", ".join(srcset_parts)
    
    return f"{url} 1x"


@register.simple_tag
def picture_element(image_url, alt_text="", css_class="", lazy=True):
    """
    Generate a <picture> element with WebP and fallback
    
    Usage:
        {% picture_element product.get_image_url product.name css_class="product-img" %}
    """
    if not image_url:
        return ""
    
    lazy_attr = 'loading="lazy"' if lazy else ''
    
    if 'cloudinary' in image_url:
        webp_url = image_url.replace('/upload/', '/upload/f_webp,q_auto/')
        jpg_url = image_url.replace('/upload/', '/upload/f_jpg,q_auto/')
        
        html = f'''
        <picture>
            <source srcset="{webp_url}" type="image/webp">
            <source srcset="{jpg_url}" type="image/jpeg">
            <img src="{jpg_url}" alt="{alt_text}" class="{css_class}" {lazy_attr} decoding="async">
        </picture>
        '''
    else:
        html = f'<img src="{image_url}" alt="{alt_text}" class="{css_class}" {lazy_attr} decoding="async">'
    
    return mark_safe(html)


@register.filter
def thousand_separator(value):
    """
    Format a number with thousand separators (commas) and 2 decimal places
    
    Usage:
        {{ product.price|thousand_separator }}
        {{ order.total_amount|thousand_separator }}
    """
    if value is None:
        return ""
    try:
        # Handle Decimal values directly to avoid float precision issues
        if isinstance(value, Decimal):
            # Round to 2 decimal places using ROUND_HALF_UP
            value = value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            # Format with commas and 2 decimal places
            return f"{value:,}"
        else:
            # Convert to Decimal first, then format
            dec_value = Decimal(str(value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            return f"{dec_value:,}"
    except (ValueError, TypeError, InvalidOperation):
        return value
