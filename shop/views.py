from django.shortcuts import render, redirect
from .models import *
from .forms import SignUpForm, LogInForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def parse_session(request, template_data=None):
    if template_data is None:
        template_data = {}
    if request.session.has_key('alert_success'):
        template_data['alert_success'] = request.session.get('alert_success')
        del request.session['alert_success']
    if request.session.has_key('alert_danger'):
        template_data['alert_danger'] = request.session.get('alert_danger')
        del request.session['alert_danger']
    return template_data


def login_view(request):
    template_data = parse_session(request, {'form_button': "Login"})
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            login(request, user)
            if request.user.is_authenticated:
                messages.success(request, 'successfuly logged in')
                return redirect('store')
    else:
        form = LogInForm()
    template_data['form'] = form
    return render(request, 'shop/account/login.html', template_data)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'successfully logout')
    return redirect('store')


def signup_view(request):
    template_data = parse_session(request, {'form_button': "SignUp"})
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )

            messages.success(request, 'successfully SignUp')
            return redirect('store')
    else:
        form = SignUpForm()
    template_data['form'] = form
    return render(request, 'shop/account/signup.html', template_data)


def store(request):
    products = Product.objects.all()
    template_data = {'products': products}
    return render(request, 'shop/store.html', template_data)


def product(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        product = Product.objects.get(id=pk)
        try:
            customer = request.user.customer
        except:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        orderItem.quantity = request.POST['quantity']
        orderItem.save()
        return redirect('cart')
    context = {'product': product}
    return render(request, 'shop/product.html', context)


def cart(request):
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    context = {'order': order}
    return render(request, 'shop/cart.html', context)
