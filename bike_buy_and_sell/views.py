from datetime import timezone

from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect

from .cart import Cart
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from .models import *


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return render(request, 'logout.html')


def about_view(request):
    return render(request, 'about_us.html')


def contact_view(request):
    return render(request, 'contact_us.html')


def index(request):
    bike_buy_and_sell = BikeBuyAndSell.objects.filter(status="Approved").order_by('-id')
    banner = Banner.objects.all().order_by('-id')
    categories = Category.objects.all().order_by('-id')
    context = {
        'bike_buy_and_sell': bike_buy_and_sell,
        'banners': banner,
        'categories': categories,
    }
    return render(request, 'index.html', context=context)


def user_login(request):
    form = LoginForm()
    context = {'form': form}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username,password=password)
            print('user = ', user)
            if user:
                login(request, user)
                messages.success(request, 'Logged in successfully')
                return redirect('index')
            else:
                messages.error(request, 'Logged in Fail')
    return render(request, 'login.html', context)


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration.html"


@login_required(login_url='/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to maintain user's session
            messages.success(request, 'Your password was successfully updated!')
            return redirect('index')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})


@login_required(login_url='/login')
def profile(request):
    # Assuming you have a OneToOneField relationship between User and Profile models
    profile = request.user

    return render(request, 'profile.html', {'profile': profile})


@login_required(login_url='/login')
def update_profile(request):
    form = ProfileUpdateForm()
    context = {
        'user': request.user,
        'form': form
    }
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')

            user = User.objects.get(pk=request.user.id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            return redirect('profile')

    return render(request, 'update_profile.html', context)


@login_required(login_url='/login')
def booking_list(request):
    booking_list = Orders.objects.filter(user=request.user).order_by('-id')
    context = {
        "booking_list": booking_list
    }
    return render(request, 'booking_list.html', context)


def buy_list(request):
    bike_buy_and_sell = BikeBuyAndSell.objects.filter(status='Approved').order_by('-id')
    context = {
        'bike_buy_and_sell': bike_buy_and_sell
    }
    return render(request, 'buy_list.html', context)


@login_required(login_url='/login')
def sell_views(request):
    category = Category.objects.all()
    context = {
        'category': category
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        category = request.POST.get('category')
        category_obj = Category.objects.get(pk=category)
        user = request.user
        bike_buy_and_sell_create = BikeBuyAndSell.objects.create(
            name=name,
            price=price,
            quantity=quantity,
            description=description,
            category=category_obj,
            user=user
        )
        print('bike_buy_and_sell_create = ', bike_buy_and_sell_create)

        image_list = request.FILES.getlist('image')
        print("image_list = ", image_list)
        for image in image_list:
            print("image = ", image)
            BikeBuyAndSellImage.objects.create(
                bike_buy_and_sell=bike_buy_and_sell_create,
                image=image
            )
        return redirect('sell_list')

    return render(request, 'sell.html', context=context)


@login_required(login_url='/login')
def sell_list(request):
    user = request.user
    obj = BikeBuyAndSell.objects.filter(user=user).order_by('-id')
    context = {
        "bike_buy_and_sell": obj
    }
    return render(request, 'sell_list.html', context)


# any one can add product to cart, no need of signin
def add_to_cart_view(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(BikeBuyAndSell, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart_detail.html', {'cart': cart})


def cart_update(request, product_id):
    if request.method == "POST":
        cart = Cart(request)
        product = get_object_or_404(BikeBuyAndSell, id=product_id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print('cd = ', cd)
            cart.update(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
        return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(BikeBuyAndSell, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


@login_required(login_url='/login')
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.get(username=request.user)
            order = Orders.objects.create(
                user=user,
                email=cd['email'],
                mobile=cd['mobile'],
                address=cd['address'],
                total_price=cart.get_total_price()
            )

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    bike_buy_and_sell=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            return render(request, 'order_created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'checkout_create.html', {'form': form})


def search_view(request):
    # whatever user write in search box we get in query
    query = request.GET['query']
    products = BikeBuyAndSell.objects.all().filter(name__icontains=query)

    # word variable will be shown in html when user click on search button
    word = "Searched Result : {}".format(query)

    context = {
        'bike_buy_and_sell': products,
        'word': word,
    }

    return render(request, 'index.html', context)


def order_details(request, order_id):
    orders = Orders.objects.get(user=request.user, id=order_id)
    products = OrderItem.objects.filter(order__id=order_id)
    return render(request, 'order_details.html', {'order': orders, "products": products})


def product_detail(request, id):
    product = get_object_or_404(BikeBuyAndSell, id=id)
    cart_product_form = CartAddProductForm()
    context = {
        'product': product,
        'cart_product_form': cart_product_form,
    }
    return render(request, 'detail.html', context)


def category_based_bike(request, category_id):
    bike_buy_and_sell = BikeBuyAndSell.objects.filter(category__id=category_id)
    context = {
        'bike_buy_and_sell': bike_buy_and_sell,
    }
    return render(request, 'category_based_bike.html', context)
