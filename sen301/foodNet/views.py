from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Order, OrderItem, Product, Category, ShippingAddress
from .forms import RegisterForm, LoginForm
from django.shortcuts import redirect
from django.contrib import messages
from .templatetags.my_filter import naira
import datetime
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .utils import cookieCart, cartData

# Create your views here.

def home_page(request):
    cookieData = cookieCart(request)
    cartItems = cookieData['cartItems']
    if request.user.is_authenticated:
        return redirect('foodNet:market')
    return render(request, "foodnet/home_page.html", {
        'cartItems': cartItems
    })


def login_view(request):

    # redirect the user to market if he is login
    if request.user.is_authenticated:
        return redirect('foodNet:market')
    
    if request.method == "POST":

        # recuperation of the data first
        form = LoginForm(request.POST)

        if form.is_valid():
            # Attempt to sign user in
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            
            user = authenticate(request, username=username, password=password)

            
            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("foodNet:market"))
            else:
                    
                messages.info(request, 'Invalid Username/Password! Please Try again.')
                return render(request, "foodnet/login.html", {
                "form": form
            })
                
        else:

            messages.warning(request, 'Please fill the form to login!!')
            return render(request, "foodnet/login.html", {
            "form": form
        })
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        return render(request, "foodnet/login.html", {
            "form": LoginForm(),
            'cartItems': cartItems,
        })
    

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("foodNet:login"))


def register(request):

    #  redirect the user if he is login
    if request.user.is_authenticated:
        return redirect('foodNet:market')
    
    if request.method == "POST":
        
        first_name = request.POST.get("first_name", False)
        surname = request.POST.get("surname", False)
        middle_name = request.POST.get("middle_name", False)
        username = request.POST["username"]
        email = request.POST.get("email", False)
        
        password = request.POST.get("password", False)
        confirmation = request.POST.get("confirm_password", False)
        
        phone_number = request.POST.get("phone_number", False)
        address1 = request.POST.get("address1", False)
        address2 = request.POST.get("address2", False)        
        state = request.POST.get("state", False)
        city = request.POST.get("city", False)
        zipcode = request.POST.get("zip", False)


        if not(first_name) or not(surname) or not(username) or not(phone_number) or \
            not(address1) or not(city) or not(state):

            messages.warning(request, 'Please fill the form correctly.')
            return render(request, "foodnet/register.html")

        # Ensure password matches confirmation
        if password != confirmation:

            messages.warning(request, 'Passwords must match.')
            return render(request, "foodnet/register.html")

        # Attempt to create new user
        try:
            if not(address2):
                user = User.objects.create_user(first_name=first_name, last_name=surname, middle_name = middle_name, username=username
                                                , email=email, password=password, phone_number=phone_number, address1=address1)
            else:
                user = User.objects.create_user(first_name=first_name, last_name=surname, middle_name = middle_name, username=username
                                                , email=email, password=password, phone_number=phone_number, address1=address1, address2=address2
                                                , state=state, city=city, zipcode=zipcode)

            user.save()
        except IntegrityError:

            messages.info(request, 'Username already taken.')
            return render(request, "foodnet/register.html")
        

        login(request, user)
        messages.success(request, 'Welcome the FoodNet community !! Your account has been created.')
        return HttpResponseRedirect(reverse("foodNet:market"))
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        return render(request, "foodnet/register.html", {
            "form": RegisterForm(),
            'cartItems': cartItems
        })


def market(request):

    if request.user.is_authenticated:

        client = request.user

        products = Product.objects.all().exclude(vendor=client).order_by('product_timestamp')
        paginator = Paginator(products, 6)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        
        order, created = Order.objects.get_or_create(client=client,complete=False)
        cartItems = order.get_cart_items

        categories = Category.objects.all()

    else:

       # fetching the cookies
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        
        
        products = Product.objects.all().order_by('product_timestamp')
        paginator = Paginator(products, 6)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        categories = Category.objects.all()

        if(cookieData['error']):
            messages.info(request, 'Something wrong happen!! Please try again.')
            return render(request, "foodnet/market.html", {
                'products': page_obj,
                'cartItems': cartItems,
                'categories': categories,
                'paginator': paginator
            })

    return render(request, "foodnet/market.html", {
        'products': page_obj,
        'cartItems': cartItems,
        'categories': categories,
        'paginator': paginator 
    })


# @login_required(login_url="/foodNet/login/")
def cart(request):

    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    
    if(data['error']):
        messages.info(request, 'Something wrong happen!! Please try again.')
        return render(request, "foodnet/cart.html", {
            'items': items,
            'order': order,
            'cartItems': cartItems,
        })        

    return render(request, "foodnet/cart.html", {
            'items': items,
            'order': order,
            'cartItems': cartItems,
        })


# @login_required(login_url="foodNet/login")
def checkout(request):

    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    
    if(data['error']):
        messages.info(request, 'Something wrong happen!! Please try again.')
        return render(request, "foodnet/cart.html", {
            'items': items,
            'order': order,
            'cartItems': cartItems,
        })
    
    return render(request, "foodnet/checkout.html", {
        'items': items,
        'order': order,
        'cartItems': cartItems,
    })


def view_product(request, product_id):

    try:  
        product = Product.objects.get(pk=int(product_id))
    except UnboundLocalError or ValueError:
        messages.info(request, '404 Not Found!! Product not found.')
        return redirect('foodNet:market')
    except Product.DoesNotExist:
        messages.info(request, '404 Not Found!! Product not found.')
        return redirect('foodNet:market')
    
    if request.user.is_authenticated:
        client = request.user
        order, created = Order.objects.get_or_create(client=client, complete=False)
        cartItems = order.get_cart_items
          
    else:
        # fetching the cookies
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        
        if(cookieData['error']):
            messages.info(request, 'Something wrong happen!! Please try again.')
            return render(request, "foodnet/cart.html", {
                'product':product,
                'cartItems': cartItems,
            })

    return render(request, "foodnet/view_product.html",{
        'product':product,
        'cartItems': cartItems
    })


@login_required(login_url="/foodNet/login/")
def create_product(request):
    if request.method == "POST":
        
        name = request.POST.get("name", False)
        description = request.POST.get("description", False)
        price = request.POST.get("price", False)
        category = request.POST.get("category", False)
        image = request.FILES.get("image", False)

        
        if not(name) or not price.isdigit() or not category:
            messages.warning(request, 'Please fill the form correctly.')
            return render(request, "foodnet/create_product.html")
        
        try:
            # if the user provides the image
            if image:
                try:
                    if Category.objects.get(pk=int(category)):
                        product = Product.objects.create(name=name, description=description, price=price,
                                                        img=image, vendor=request.user, category=Category.objects.get(pk=int(category)))
                        product.save()
                except IntegrityError and ValueError:

                    messages.info(request, 'Sorry something went wrong!! Please try again.')
                    return render(request, "auctions/create_listing.html")
                
            # if the user does not provide the image
            else:
                try:
                    if Category.objects.get(pk=int(category)):
                        product = Product.objects.create(name=name, description=description, price=price,
                                                        vendor=request.user, category=Category.objects.get(pk=int(category)))
                        product.save()
                except IntegrityError and ValueError:

                    messages.info(request, 'Sorry something went wrong!! Please try again.')
                    return render(request, "auctions/create_listing.html")

        except IntegrityError or KeyError:

            messages.info(request, 'Sorry something went wrong!! Please try again.')
            return render(request, "auctions/create_listing.html")

        
        messages.success(request, f'Your product {name.title()} has been added to the market for {naira(int(price))}.')
        return HttpResponseRedirect(reverse("foodNet:market"))

    else:
        categories = Category.objects.all()

        client = request.user
        order, created = Order.objects.get_or_create(client=client, complete=False)
        cartItems = order.get_cart_items
        

        return render(request, "foodnet/create_product.html", {
            'categories': categories,
            'cartItems': cartItems,
        })


@login_required(login_url="/foodNet/login/")
def profile(request, prof_name, prof_id):
    try:  
        profile = User.objects.get(pk=int(prof_id))

        if profile.username != prof_name:
            return redirect('foodNet:market')
        
    except UnboundLocalError or ValueError:
        messages.info(request, '404 Not Found!! Profile not found.')
        return redirect('foodNet:market')
    except Product.DoesNotExist:
        messages.info(request, '404 Not Found!! Profile not found.')
        return redirect('foodNet:foodNet:market')
    
    
    order, created = Order.objects.get_or_create(client=profile, complete=False)
    cartItems = order.get_cart_items

    marketProducts = Product.objects.filter(vendor=profile).order_by('-product_timestamp')
    
    
    sells = []
    for product in marketProducts:
        orderItems = OrderItem.objects.filter(product=product).order_by('added_timestamp')
        for item in orderItems:
            if item.order.complete == True:
                
                sells.append(item)


    orders = Order.objects.filter(client=profile).exclude(complete=False).order_by('order_timestamp')
    
    return render(request, "foodnet/profile.html", {
        'profile': profile,
        'cartItems': cartItems,
        'marketProducts': marketProducts,
        'sells': sells,
        'orders': orders
    })


# @csrf_exempt
# @login_required(login_url="/foodNet/login/")
def updateItem(request):

    # parse the data receive to python object(dictionary)
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    client = request.user
    try:
        product = Product.objects.get(pk=productId)
    except UnboundLocalError or ValueError:
        messages.info(request, '400 Bad request!! Product not found.')
        return redirect('foodNet:foodNet:market')
    except Product.DoesNotExist:
        messages.info(request, '404 Not Found!! Product not found.')
        return redirect('foodNet:market')

    # query or create a new order
    order, created = Order.objects.get_or_create(client=client, complete=False)
    # query or create a new item order
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    # modify the item order quantity
    if action == 'add':
        orderItem.quantity = orderItem.quantity + 1
    elif action == 'remove':
        orderItem.quantity = orderItem.quantity - 1

    orderItem.save()

    # delete the item order if the quantity is less than 1
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


@login_required(login_url="/foodNet/login/")
def placeOrder(request):
    data = json.loads(request.body)

    client = request.user
    order, created = Order.objects.get_or_create(client=client, complete=False)
    
    shipping = data['shipping']

    # print(shipping["total"])

    transaction_id = datetime.datetime.now().timestamp()

    if shipping['total'] == order.get_cart_total or shipping['total'] == (order.get_cart_total + 500):
        if request.user.can_purchase(shipping['total']):
            order.complete = True
            order.transaction_id = transaction_id

            items = order.order_items.all()

            for item in items:
                credit = item.get_total
                item.product.vendor.budget = item.product.vendor.budget + credit
                item.product.vendor.save()

            client.budget = client.budget - shipping['total']
            client.save()
            order.save()
        else:
            return JsonResponse({
                'response': 'Fail'}, safe=False)
    else:
        return JsonResponse('Intruder', safe=False)
    
    ShippingAddress.objects.create(
        client=client,
        order=order,
        name=shipping['name'],
        phone_number=shipping['phone_number'],
        address=shipping['address'],
        state=shipping['state'],
        city=shipping['city'],
        zipcode=shipping['zipcode']
    )

    return JsonResponse({
        'response': 'Success'}, safe=False)
    

def search(request):
    if request.method == "GET":
        search = request.GET.get("category", False)
        
        if search:
            # checking if the request is digit or numeric
            if search.isnumeric() and search.isdigit():
               
                try:
                    # checking if the category exists.
                    Category.objects.get(pk=int(search))

                    if request.user.is_authenticated:
                        client = request.user
                        order, created = Order.objects.get_or_create(client=client, complete=False)
                        cartItems = order.get_cart_items

                        products = Product.objects.filter(category=Category.objects.get(pk=int(search))).exclude(vendor=request.user).order_by('product_timestamp')
                        paginator = Paginator(products, 6)
                        page_number = request.GET.get("page", 1)
                        page_obj = paginator.get_page(page_number)

                        return render(request, "foodnet/market.html", {
                            'products': page_obj,
                            'cartItems': cartItems,
                            'categories': Category.objects.all(),
                            'paginator': paginator
                        })
                    else:
                        cookieData = cookieCart(request)
                        cartItems = cookieData['cartItems']
                        products = Product.objects.filter(category=Category.objects.get(pk=int(search))).order_by('product_timestamp')
                        paginator = Paginator(products, 6)
                        page_number = request.GET.get("page", 1)
                        page_obj = paginator.get_page(page_number)
                        categories = Category.objects.all()

                        return render(request, "foodnet/market.html", {
                            'products': page_obj,
                            'categories': categories,
                            'cartItems': cartItems,
                            'paginator': paginator 
                        })
            
                except UnboundLocalError or ValueError:
                    messages.info(request, '400 Bad Request!! Category not found.')
                    return redirect('foodNet:market')
                except Category.DoesNotExist:
                    # if the category does not exist we throw a 404 (not found). error
                    messages.info(request, '404 Not Found!! Category not found.')
                    return redirect('foodNet:market')
            # checking if the user wants all the auctions (with no category).
            elif search == "all":
                
                return redirect("foodNet:market")
            else:
                # else if the user attempt something else we throw a 404 (not found) error.
                messages.warning(request, '403 Search Forbidden!! Category not found.')
                return redirect('foodNet:market')
        else:
            messages.info(request, '403 Search Forbidden!! Category not found.')
            return redirect('foodNet:market')
    else:
        
        # if the user attempt to access by a post request
        return redirect("index")


def processOrder(request):
    pass


def editProduct(request):
    pass


@login_required(login_url="/foodNet/login/")
def deleteProduct(request, product_id):
    
    try:  
        product = Product.objects.get(pk=int(product_id))
    except UnboundLocalError or ValueError:
        messages.warning(request, '404 Not Found!! Product not found.')
        return redirect('foodNet:profile', prof_name=request.user.username, prof_id=request.user.id)
    except Product.DoesNotExist:
        messages.warning(request, '404 Not Found!! Product not found.')
        return redirect('foodNet:profile', prof_name=request.user.username, prof_id=request.user.id)
    
    if request.user != product.vendor:
        messages.warning(request, '401 Unauthorized!! Unauthorized Request.')
        return redirect('foodNet:profile', prof_name=request.user.username, prof_id=request.user.id)
    
    
    product.delete()

    messages.success(request, 'The product has been removed from the market.')
    return redirect('foodNet:profile', prof_name=request.user.username, prof_id=request.user.id)



def editProfile(request):
    pass


@login_required(login_url="/foodNet/login/")
def view_own_product(request, product_id):

    try:  
        product = Product.objects.get(pk=int(product_id))
    except UnboundLocalError or ValueError:
        messages.info(request, '404 Not Found!! Product not found.')
        return redirect('foodNet:market')
    except Product.DoesNotExist:
        messages.info(request, '404 Not Found!! Product not found.')
        return redirect('foodNet:market')
    
    client = request.user
    order, created = Order.objects.get_or_create(client=client, complete=False)
    cartItems = order.get_cart_items
    
    
    return render(request, "foodnet/view_own_product.html",{
        'product':product,
        'cartItems': cartItems
    })
   

@login_required(login_url="/foodNet/login/")
def orders(request, user_name):
    
    return render(request, "foodnet/orders.html")
