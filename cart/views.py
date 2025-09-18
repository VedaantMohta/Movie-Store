from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from movies.models import Movie
from .models import Order, Item
from django.contrib.auth.decorators import login_required

from .utils import calculate_cart_total
def index(request):
    selected_cart = request.GET.get('cart', '1')
    all_carts = request.session.get('carts', {'1': {}, '2': {}, '3': {}})
    cart = all_carts.get(selected_cart, {})
    movie_ids = list(cart.keys())
    movies_in_cart = []
    cart_total = 0
    if movie_ids:
        movies_in_cart = Movie.objects.filter(id__in=movie_ids)
        cart_total = calculate_cart_total(cart, movies_in_cart)
    template_data = {}
    template_data['title'] = 'Cart'
    template_data['movies_in_cart'] = movies_in_cart
    template_data['cart_total'] = cart_total
    template_data['selected_cart'] = selected_cart
    return render(request, 'cart/index.html', {'template_data': template_data})

def add(request, id):
    get_object_or_404(Movie, id=id)
    selected_cart = request.POST.get('cart', '1')
    all_carts = request.session.get('carts', {'1': {}, '2': {}, '3': {}})
    cart = all_carts.get(selected_cart, {})
    cart[id] = request.POST['quantity']
    all_carts[selected_cart] = cart
    request.session['carts'] = all_carts
    return redirect(f'/cart/?cart={selected_cart}')

def clear(request):
    selected_cart = request.GET.get('cart', '1')
    all_carts = request.session.get('carts', {'1': {}, '2': {}, '3': {}})
    all_carts[selected_cart] = {}
    request.session['carts'] = all_carts
    return redirect(f'/cart/?cart={selected_cart}')

@login_required
def purchase(request):
    selected_cart = request.GET.get('cart', '1')
    all_carts = request.session.get('carts', {'1': {}, '2': {}, '3': {}})
    cart = all_carts.get(selected_cart, {})
    movie_ids = list(cart.keys())
    if not movie_ids:
        return redirect(f'/cart/?cart={selected_cart}')
    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)
    order = Order()
    order.user = request.user
    order.total = cart_total
    order.save()
    for movie in movies_in_cart:
        item = Item()
        item.movie = movie
        item.price = movie.price
        item.order = order
        item.quantity = cart[str(movie.id)]
        item.save()
    all_carts[selected_cart] = {}
    request.session['carts'] = all_carts
    template_data = {}
    template_data['title'] = 'Purchase confirmation'
    template_data['order_id'] = order.id
    return render(request, 'cart/purchase.html',{'template_data': template_data})