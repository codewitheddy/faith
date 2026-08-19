from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F
from .models import Category, Product, ProductVariant, Order, OrderItem, UserProfile, Wishlist, HeroSlide
from .email_utils import send_order_confirmation_email
from decimal import Decimal
import json
from urllib.parse import quote

def _get_cart_count(request):
    cart = request.session.get('cart', {})
    return sum(item['quantity'] for item in cart.values())

def _get_wishlist_ids(request):
    if request.user.is_authenticated:
        return set(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))
    return set()

def home(request):
    categories = Category.objects.all()
    new_arrivals = Product.objects.filter(is_available=True).select_related('category').order_by('-created_at')[:8]
    featured_products = Product.objects.filter(is_available=True).select_related('category')[:8]
    sale_products = Product.objects.filter(
        is_available=True, sale_price__isnull=False
    ).filter(sale_price__lt=F('price')).select_related('category')[:8]
    hero_slides = HeroSlide.objects.filter(is_active=True).order_by('order')
    context = {
        'categories': categories,
        'new_arrivals': new_arrivals,
        'featured_products': featured_products,
        'sale_products': sale_products,
        'cart_count': _get_cart_count(request),
        'wishlist_ids': _get_wishlist_ids(request),
        'hero_slides': hero_slides,
    }
    return render(request, 'home_new.html', context)

def shop(request):
    categories = Category.objects.all()
    category_slug = request.GET.get('category', 'all')
    sale_filter = request.GET.get('filter', '')
    search_query = request.GET.get('q', '').strip()
    products_list = Product.objects.filter(is_available=True).select_related('category')
    if category_slug and category_slug != 'all':
        try:
            selected_category = Category.objects.get(slug=category_slug)
            products_list = products_list.filter(category=selected_category)
        except Category.DoesNotExist:
            pass
    if sale_filter == 'sale':
        products_list = products_list.filter(sale_price__isnull=False).filter(sale_price__lt=F('price'))
    if search_query:
        from django.db.models import Q
        products_list = products_list.filter(
            Q(name__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        ).distinct()
    paginator = Paginator(products_list, 16)
    products = paginator.get_page(request.GET.get('page', 1))
    context = {
        'categories': categories,
        'products': products,
        'cart_count': _get_cart_count(request),
        'selected_category': category_slug,
        'sale_filter': sale_filter,
        'search_query': search_query,
        'wishlist_ids': _get_wishlist_ids(request),
    }
    return render(request, 'shop.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    # Track view count (use F() to avoid race conditions)
    Product.objects.filter(pk=product.pk).update(view_count=F('view_count') + 1)
    related_products = Product.objects.filter(
        category=product.category, is_available=True
    ).exclude(id=product.id)[:4]
    in_wishlist = request.user.is_authenticated and Wishlist.objects.filter(user=request.user, product=product).exists()
    variants = product.variants.filter(is_available=True)
    context = {
        'product': product,
        'variants': variants,
        'related_products': related_products,
        'cart_count': _get_cart_count(request),
        'in_wishlist': in_wishlist,
    }
    return render(request, 'product_detail.html', context)

def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    cart_total = 0
    cart_total_savings = 0
    for product_id, item in cart.items():
        subtotal = float(item['price']) * item['quantity']
        cart_total += subtotal
        
        # Fetch product to get original price for display
        try:
            product = Product.objects.get(id=product_id)
            current_price = float(item['price'])
            
            # Get base price (original price)
            base_price = float(product.price)
            
            # Check if product is on sale
            is_on_sale = product.on_sale  # Uses the @property that checks sale_price < price
            
            # Get discount info
            discount_percent = product.discount_percent if is_on_sale else 0
            
            # Calculate savings
            if is_on_sale and discount_percent > 0:
                savings_per_item = (base_price - current_price) * item['quantity']
                cart_total_savings += savings_per_item
            
        except Product.DoesNotExist:
            base_price = float(item['price'])
            current_price = float(item['price'])
            is_on_sale = False
            discount_percent = 0
        
        cart_items.append({
            'id': product_id,
            'name': item['name'],
            'price': current_price,  # Actual price customer pays
            'original_price': base_price,  # Original/list price
            'is_on_sale': is_on_sale,
            'discount_percent': discount_percent,
            'quantity': item['quantity'],
            'subtotal': float(subtotal),
            'image': item.get('image', ''),
        })
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_total_savings': cart_total_savings,
        'cart_count': _get_cart_count(request),
    }
    return render(request, 'cart.html', context)

def about(request):
    context = {'cart_count': _get_cart_count(request)}
    return render(request, 'about.html', context)

def contact(request):
    context = {'cart_count': _get_cart_count(request)}
    return render(request, 'contact.html', context)

def filter_products(request):
    """AJAX endpoint for filtering products by category"""
    import logging
    logger = logging.getLogger(__name__)

    try:
        category_slug = request.GET.get('category', 'all')
        page_number = request.GET.get('page', 1)
        sale_filter = request.GET.get('filter', '')
        search_query = request.GET.get('q', '').strip()

        logger.info(f"Filter request - Category: {category_slug}, Page: {page_number}, Sale: {sale_filter}, Q: {search_query}")

        # Get products
        products_list = Product.objects.filter(is_available=True).select_related('category')

        # Filter by category
        selected_category = None
        if category_slug and category_slug != 'all':
            try:
                selected_category = Category.objects.get(slug=category_slug)
                products_list = products_list.filter(category=selected_category)
                logger.info(f"Filtered by category: {selected_category.name}")
            except Category.DoesNotExist:
                logger.warning(f"Category not found: {category_slug}")
                pass

        if sale_filter == 'sale':
            products_list = products_list.filter(sale_price__isnull=False).filter(sale_price__lt=F('price'))

        if search_query:
            from django.db.models import Q
            products_list = products_list.filter(
                Q(name__icontains=search_query) |
                Q(short_description__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(category__name__icontains=search_query)
            ).distinct()

        # Pagination
        paginator = Paginator(products_list, 16)
        products = paginator.get_page(page_number)

        logger.info(f"Found {paginator.count} products, showing page {products.number} of {paginator.num_pages}")

        # Get cart for quantity selectors
        cart = request.session.get('cart', {})

        # Build products HTML
        products_html = render_to_string('partials/products_grid.html', {
            'products': products,
            'cart': cart,
            'wishlist_ids': _get_wishlist_ids(request),
        }, request=request)

        # Build pagination HTML
        pagination_html = render_to_string('partials/pagination.html', {
            'products': products,
            'category': category_slug,
        }, request=request)

        response_data = {
            'success': True,
            'products_html': products_html,
            'pagination_html': pagination_html,
            'total_count': paginator.count,
            'page_count': paginator.num_pages,
            'current_page': products.number,
            'category': category_slug,
            'debug_info': {
                'products_found': paginator.count,
                'cart_items': len(cart),
                'category_slug': category_slug,
                'page': products.number
            }
        }

        logger.info(f"Returning response with {len(products_html)} chars of HTML")
        return JsonResponse(response_data)

    except Exception as e:
        logger.error(f"Error in filter_products: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': str(e),
            'debug_info': {
                'category': request.GET.get('category', 'unknown'),
                'page': request.GET.get('page', 'unknown')
            }
        }, status=500)


def search_suggest(request):
    """AJAX endpoint for live search suggestions (navbar dropdown)"""
    from django.db.models import Q

    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse({'results': [], 'total_count': 0})

    products = (
        Product.objects.filter(is_available=True)
        .filter(
            Q(name__icontains=query) |
            Q(short_description__icontains=query) |
            Q(category__name__icontains=query)
        )
        .select_related('category')[:6]
    )
    total = (
        Product.objects.filter(is_available=True)
        .filter(
            Q(name__icontains=query) |
            Q(short_description__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        ).count()
    )
    results = [{
        'name': p.name,
        'slug': p.slug,
        'price': float(p.effective_price),
        'on_sale': bool(p.on_sale),
        'category': p.category.name if p.category else '',
        'image': p.get_image_url() or '',
    } for p in products]
    return JsonResponse({'results': results, 'total_count': total})


@require_POST
def add_to_cart(request):
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        # Handle both JSON and form data
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = int(data.get('quantity', 1))
            price_override = data.get('price_override')
        else:
            product_id = request.POST.get('product_id')
            quantity = int(request.POST.get('quantity', 1))
            price_override = request.POST.get('price_override')
        
        logger.info(f"Adding product {product_id} x{quantity} to cart")
        product = get_object_or_404(Product, id=product_id)

        # Check if product is out of stock
        if product.is_out_of_stock:
            return JsonResponse({'success': False, 'error': 'This product is out of stock.'}, status=400)
        
        # Check if requested quantity exceeds available stock
        cart = request.session.get('cart', {})
        current_cart_qty = cart.get(str(product_id), {}).get('quantity', 0)
        total_qty_after_add = current_cart_qty + quantity
        
        if not product.can_order(total_qty_after_add):
            available = product.stock_quantity
            return JsonResponse(
                {'success': False, 'error': f'Only {available} unit(s) available in stock.'},
                status=400
            )

        # Use price_override (variant price) if provided and valid, else effective_price
        from decimal import Decimal, InvalidOperation
        try:
            price = Decimal(str(price_override)) if price_override else product.effective_price
        except InvalidOperation:
            price = product.effective_price
        
        logger.info(f"Current cart before add: {cart}")
        
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += quantity
        else:
            cart[str(product_id)] = {
                'name': product.name,
                'price': str(price),
                'quantity': quantity,
                'image': product.get_image_url() or ''
            }
        
        request.session['cart'] = cart
        request.session.modified = True
        
        cart_count = sum(item['quantity'] for item in cart.values())
        logger.info(f"Cart after add: {cart}, Count: {cart_count}")
        
        return JsonResponse({'success': True, 'cart_count': cart_count})
    except Exception as e:
        logger.error(f"Error adding to cart: {e}", exc_info=True)
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@require_POST
def update_cart(request):
    data = json.loads(request.body)
    product_id = data.get('product_id')
    action = data.get('action')
    
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        product = get_object_or_404(Product, id=product_id)
        
        if action == 'increase':
            # Check if increasing quantity is allowed by stock
            new_qty = cart[str(product_id)]['quantity'] + 1
            if not product.can_order(new_qty):
                available = product.stock_quantity
                return JsonResponse({
                    'success': False,
                    'error': f'Only {available} unit(s) available in stock.'
                }, status=400)
            cart[str(product_id)]['quantity'] = new_qty
        elif action == 'decrease':
            if cart[str(product_id)]['quantity'] > 1:
                cart[str(product_id)]['quantity'] -= 1
            else:
                del cart[str(product_id)]
        elif action == 'remove':
            del cart[str(product_id)]
    
    request.session['cart'] = cart
    request.session.modified = True  # Explicitly mark session as modified
    cart_count = sum(item['quantity'] for item in cart.values())
    cart_total = sum(float(item['price']) * item['quantity'] for item in cart.values())
    
    # Build cart_items array for frontend sync
    cart_items = []
    for pid, item in cart.items():
        subtotal = float(item['price']) * item['quantity']
        cart_items.append({
            'id': pid,
            'name': item['name'],
            'price': float(item['price']),
            'quantity': item['quantity'],
            'subtotal': subtotal,
            'image': item.get('image', '')
        })
    
    return JsonResponse({
        'success': True,
        'cart_count': cart_count,
        'cart_total': cart_total,
        'cart_items': cart_items
    })

def get_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    cart_total = 0
    
    for product_id, item in cart.items():
        subtotal = float(item['price']) * item['quantity']
        cart_total += subtotal
        cart_items.append({
            'id': product_id,
            'name': item['name'],
            'price': float(item['price']),
            'quantity': item['quantity'],
            'subtotal': subtotal,
            'image': item.get('image', '')
        })
    
    return JsonResponse({
        'success': True,
        'cart': cart,  # Return raw cart for easier sync
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_count': sum(item['quantity'] for item in cart.values())
    })


def product_stock_api(request, product_id):
    """API endpoint to get product stock status"""
    try:
        product = get_object_or_404(Product, id=product_id)
        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'stock_quantity': product.stock_quantity,
            'reorder_level': product.reorder_level,
            'is_low_stock': product.is_low_stock,
            'is_out_of_stock': product.is_out_of_stock,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def checkout(request):
    cart = request.session.get('cart', {})

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        # Fallback: build from split fields if hidden name field is empty
        if not name:
            fn = request.POST.get('first_name', '').strip()
            ln = request.POST.get('last_name', '').strip()
            name = (fn + ' ' + ln).strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address_line = request.POST.get('address', '').strip()
        apartment = request.POST.get('apartment', '').strip()
        city = request.POST.get('city', '').strip()
        postal_code = request.POST.get('postal_code', '').strip()
        shipping_method = request.POST.get('shipping_method', 'nairobi')
        shipping_fee = request.POST.get('shipping_fee', '0')
        discount_code = request.POST.get('discount_code', '').strip()
        discount_amount = request.POST.get('discount_amount', '0')
        notes = request.POST.get('notes', '')

        # Build full address string
        full_address = address_line
        if apartment:
            full_address += f', {apartment}'
        if city:
            full_address += f', {city}'
        if postal_code:
            full_address += f' {postal_code}'

        if not cart:
            messages.error(request, 'Your cart is empty.')
            return redirect('shop:shop')

        try:
            shipping_fee = Decimal(str(shipping_fee))
        except Exception:
            shipping_fee = Decimal('0')
        try:
            discount_amount = Decimal(str(discount_amount))
        except Exception:
            discount_amount = Decimal('0')

        subtotal = sum(float(item['price']) * item['quantity'] for item in cart.values())
        total = Decimal(str(subtotal)) + shipping_fee - discount_amount
        if total < 0:
            total = Decimal('0')

        # Create Order in database
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            customer_name=name,
            customer_email=email,
            customer_phone=phone,
            customer_address=full_address,
            notes=notes,
            total_amount=total,
            status='pending'
        )

        # Create OrderItems
        for product_id, item in cart.items():
            try:
                product = Product.objects.get(id=product_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=Decimal(item['price'])
                )
            except Product.DoesNotExist:
                pass

        # Send order confirmation email to customer
        send_order_confirmation_email(order)

        # Build WhatsApp message with pricing info
        shipping_labels = {
            'nairobi': 'Nairobi Delivery',
            'outside_nairobi': 'Outside Nairobi',
            'pickup': 'Pickup (Nairobi CBD)',
        }
        message = "*NEW ORDER - ThePopShopKe*\n"
        message += f"Order #: {order.order_number}\n\n"
        message += "*ORDER ITEMS*\n"
        item_count = 0
        total_savings = 0
        
        for i, (product_id, item) in enumerate(cart.items(), 1):
            item_count += item['quantity']
            sub = float(item['price']) * item['quantity']
            
            # Fetch product to get original price and discount info
            try:
                product = Product.objects.get(id=product_id)
                original_price = float(product.price)
                current_price = float(item['price'])
                is_on_sale = product.on_sale
                discount_percent = product.discount_percent if is_on_sale else 0
                
                # Calculate savings
                if is_on_sale and discount_percent > 0:
                    savings = (original_price - current_price) * item['quantity']
                    total_savings += savings
                
                message += f"{i}. {item['name']}\n"
                if is_on_sale and discount_percent > 0:
                    message += f"   Original: ~~Ksh {original_price:,.2f}~~\n"
                    message += f"   Discounted: Ksh {current_price:,.2f} ({discount_percent}% OFF)\n"
                    message += f"   Qty: {item['quantity']} x Ksh {current_price:,.2f}\n"
                else:
                    message += f"   Qty: {item['quantity']} x Ksh {current_price:,.2f}\n"
                message += f"   Subtotal: Ksh {sub:,.2f}\n\n"
            except Product.DoesNotExist:
                message += f"{i}. {item['name']}\n"
                message += f"   Qty: {item['quantity']} x Ksh {float(item['price']):,.2f}\n"
                message += f"   Subtotal: Ksh {sub:,.2f}\n\n"

        message += "*ORDER SUMMARY*\n"
        message += f"Total Items: {item_count}\n"
        message += f"Subtotal: Ksh {subtotal:,.2f}\n"
        if total_savings > 0:
            message += f"💰 Total Savings: Ksh {total_savings:,.2f}\n"
        message += f"Shipping ({shipping_labels.get(shipping_method, shipping_method)}): Ksh {float(shipping_fee):,.2f}\n"
        if discount_amount > 0:
            message += f"Discount ({discount_code}): -Ksh {float(discount_amount):,.2f}\n"
        message += f"*Total: Ksh {float(total):,.2f}*\n\n"
        message += "*CUSTOMER DETAILS*\n"
        message += f"Name: {name}\n"
        message += f"Phone: {phone}\n"
        if email:
            message += f"Email: {email}\n"
        message += f"Address: {full_address}\n"
        if notes:
            message += f"\n*NOTES*\n{notes}\n"
        message += "\nWe'll send you M-Pesa payment details shortly.\n"
        message += "Thank you for shopping with ThePopShopKe!\n"

        encoded_message = quote(message)
        whatsapp_url = f"https://wa.me/254717147007?text={encoded_message}"

        # Clear cart
        request.session['cart'] = {}
        request.session.modified = True

        # Check if user wants to send via WhatsApp
        send_via_whatsapp = request.POST.get('send_via_whatsapp', '').lower() in ('on', 'true', '1', 'yes')
        
        if send_via_whatsapp:
            return redirect(whatsapp_url)
        else:
            # Regular checkout - show order confirmation
            messages.success(request, f'Order #{order.order_number} created successfully! We\'ll contact you shortly.')
            return redirect('shop:account_orders')

    # GET — render checkout page
    if not cart:
        # Clear any stale messages and redirect
        storage = messages.get_messages(request)
        storage.used = True  # Mark all existing messages as used/cleared
        messages.info(request, 'Your cart is empty. Add some items first.')
        return redirect('shop:shop')

    cart_items = []
    cart_total = 0
    cart_total_savings = 0
    for product_id, item in cart.items():
        subtotal = float(item['price']) * item['quantity']
        cart_total += subtotal
        
        # Fetch product to get original price for display
        try:
            product = Product.objects.get(id=product_id)
            current_price = float(item['price'])
            base_price = float(product.price)
            
            # Check if product is on sale
            is_on_sale = product.on_sale  # Uses the @property that checks sale_price < price
            
            # Get discount info
            discount_percent = product.discount_percent if is_on_sale else 0
            
            # Calculate savings
            if is_on_sale and discount_percent > 0:
                savings_per_item = (base_price - current_price) * item['quantity']
                cart_total_savings += savings_per_item
            
        except Product.DoesNotExist:
            base_price = float(item['price'])
            current_price = float(item['price'])
            is_on_sale = False
            discount_percent = 0
        
        cart_items.append({
            'id': product_id,
            'name': item['name'],
            'price': current_price,  # Actual price customer pays
            'original_price': base_price,  # Original/list price
            'is_on_sale': is_on_sale,
            'discount_percent': discount_percent,
            'quantity': item['quantity'],
            'subtotal': float(subtotal),
            'image': item.get('image', ''),
        })

    # Pre-fill from profile if authenticated
    prefill = {}
    if request.user.is_authenticated:
        prefill['first_name'] = request.user.first_name or ''
        prefill['last_name'] = request.user.last_name or ''
        prefill['email'] = request.user.email or ''
        prefill['phone'] = ''
        prefill['address'] = ''
        prefill['city'] = ''
        prefill['apartment'] = ''
        prefill['postal_code'] = ''
        try:
            profile = request.user.userprofile
            prefill['phone'] = profile.phone or ''
            prefill['address'] = profile.address or ''
            prefill['city'] = profile.city or ''
        except Exception:
            pass

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'cart_items_json': json.dumps(cart_items),
        'cart_total': cart_total,
        'cart_total_savings': cart_total_savings,
        'cart_count': _get_cart_count(request),
        'prefill': prefill,
    })



def clear_cart(request):
    """Clear cart - for testing/debugging only"""
    request.session['cart'] = {}
    request.session.modified = True
    
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Cart cleared for session: {request.session.session_key}")
    
    return JsonResponse({
        'success': True,
        'message': 'Cart cleared',
        'cart_count': 0
    })


# ─── Account Views ────────────────────────────────────────────────────────────

def register(request):
    if request.user.is_authenticated:
        return redirect('shop:account_dashboard')
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        email      = request.POST.get('email', '').strip()
        phone      = request.POST.get('phone', '').strip()
        password   = request.POST.get('password', '')
        password2  = request.POST.get('password2', '')
        if password != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
        else:
            username = email  # use email as username
            user = User.objects.create_user(username=username, email=email,
                                            password=password,
                                            first_name=first_name, last_name=last_name)
            UserProfile.objects.create(user=user, phone=phone)
            login(request, user)
            messages.success(request, f'Welcome, {first_name}! Your account has been created.')
            return redirect('shop:account_dashboard')
    return render(request, 'account/register.html', {'cart_count': _get_cart_count(request)})


def account_login(request):
    if request.user.is_authenticated:
        return redirect('shop:account_dashboard')
    if request.method == 'POST':
        email    = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next', 'shop:account_dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'account/login.html', {'cart_count': _get_cart_count(request)})


def account_logout(request):
    logout(request)
    return redirect('shop:home')


@login_required(login_url='/login/')
def account_dashboard(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-created_at')
    wishlist = Wishlist.objects.filter(user=request.user).select_related('product')
    context = {
        'orders': orders,
        'wishlist': wishlist,
        'cart_count': _get_cart_count(request),
    }
    return render(request, 'account/dashboard.html', context)


@login_required(login_url='/login/')
def account_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-created_at')
    return render(request, 'account/orders.html', {
        'orders': orders,
        'cart_count': _get_cart_count(request),
    })


@login_required(login_url='/login/')
def account_order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'account/order_detail.html', {
        'order': order,
        'cart_count': _get_cart_count(request),
    })


@login_required(login_url='/login/')
def account_wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user).select_related('product__category')
    return render(request, 'account/wishlist.html', {
        'wishlist': wishlist,
        'cart_count': _get_cart_count(request),
    })


@login_required(login_url='/login/')
def account_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name  = request.POST.get('last_name', '').strip()
        user.save()
        profile.phone   = request.POST.get('phone', '').strip()
        profile.address = request.POST.get('address', '').strip()
        profile.city    = request.POST.get('city', '').strip()
        profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('shop:account_profile')
    return render(request, 'account/profile.html', {
        'profile': profile,
        'cart_count': _get_cart_count(request),
    })


@require_POST
@login_required(login_url='/login/')
def toggle_wishlist(request):
    product_id = request.POST.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    obj, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        obj.delete()
    # AJAX request — return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'in_wishlist': created})
    # Regular form POST (e.g. from wishlist page) — redirect back
    return redirect('shop:account_wishlist')
