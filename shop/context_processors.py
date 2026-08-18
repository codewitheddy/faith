from .models import Category


def store_globals(request):
    cart = request.session.get('cart', {})
    return {
        'categories': Category.objects.all(),
        'cart_count': sum(item['quantity'] for item in cart.values()),
    }
