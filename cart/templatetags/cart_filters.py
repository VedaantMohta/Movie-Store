from django import template
register = template.Library()

@register.filter(name='dict_get')
def dict_get(d, key):
    if isinstance(d, dict):
        return d.get(key, {})
    return {}

@register.filter(name='get_quantity')
def get_cart_quantity(cart, movie_id):
    # cart may be None, a string, or a dict
    try:
        if isinstance(cart, dict):
            return cart.get(str(movie_id), 0)
        return 0
    except Exception:
        return 0