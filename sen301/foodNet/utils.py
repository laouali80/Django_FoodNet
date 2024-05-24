from .models import *
import json


def cookieCart(request):
    """Fetching cookies or setting the cookie dict to null"""
    
    # try to fetch if there are cookies if not set cart to empty dict
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    
    # print('cart: ', cart)
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0}
    cartItems = order['get_cart_items']

    for i in cart:

        try:
            cartItems += cart[i]['quantity']
            # cartItems += 1
            

            # product = Product.objects.get(id=0)
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'img':product.img,
                },
                'quantity':cart[i]['quantity'],
                'get_total':total,
            }
            items.append(item)
        except:
            items = []
            order = {'get_cart_total':0, 'get_cart_items':0}
            cartItems = order['get_cart_items']
            
            return ({
                'items': items,
                'order': order,
                'cartItems': cartItems,
                'error': True
            })

    return ({
                'items': items,
                'order': order,
                'cartItems': cartItems,
                'error': False
            })


def cartData(request):
    if request.user.is_authenticated:
        client = request.user
        order, created = Order.objects.get_or_create(client=client, complete=False)
        # items = order.orderitem_set.all() (if related name was not given)
        items = order.order_items.all()
        cartItems = order.get_cart_items
    else:
        # fetching the cookies
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cartItems = cookieData['cartItems']
        
        if(cookieData['error']):
            return ({
                'items': items,
                'order': order,
                'cartItems': cartItems,
                'error': True
            })
    
    return ({
                'items': items,
                'order': order,
                'cartItems': cartItems,
                'error': False
            })