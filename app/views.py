from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import get_user_model,authenticate,login,logout
from .models import CustomUser, Product, Cart, CartItem, Category
from django.contrib.auth.decorators import login_required

User = get_user_model()

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2 and email and username and contact_number:
            if User.objects.filter(email = email).exists():
                messages.info(request, "Email already taken")
                return redirect('register')
            elif CustomUser.objects.filter(contact_number = contact_number).exists():
                messages.info(request, "Contact Number already taken")
                return redirect('register')
            elif User.objects.filter(username = username).exists():
                messages.info(request, "Username already taken")
                return redirect('register')
            else:
                user = User.objects.create_user(username = username,email = email, password = password1)
                user.save()
                user_model = User.objects.get(email = email)
                custom_user = CustomUser.objects.create(user = user_model, contact_number = contact_number)
                custom_user.save()
        else:
            messages.info(request,"Fill all details !")
            return redirect('register')
        return redirect('login')
    else:
        return render(request, 'users/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if "@" in username:
            if User.objects.filter(email=username).exists():
                user_model = User.objects.get(email=username)
                user = authenticate(username = user_model.username, password = password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, "Invalid credentials!")
                    return redirect('/users/login')
            else:
                messages.error(request, "Invalid credentials!")
                return redirect('/users/login')
        else:
            if CustomUser.objects.filter(contact_number=username).exists():
                user = CustomUser.objects.get(contact_number=username)
                user_model = User.objects.get(username=user.user)
                user = authenticate(username = user_model.username, password = password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, "Invalid credentials!")
                    return redirect('/users/login')
            else:
                messages.error(request, "Invalid credentials!")
                return redirect('/users/login')
    else:
        return render(request, 'users/login.html')
    
@login_required(login_url='/users/login')
def user_logout(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/users/login')
def edit_profile(request):
    user = User.objects.filter(username = request.user.username).first()
    custom_user = user.customuser_set.all().first()
    if request.method == "POST":
        if request.FILES.get('image') == None:
            pass
        else:
            custom_user.image = request.FILES.get('image')
        custom_user.contact_number = request.POST.get('phone')
        user.username = request.POST.get('name')
        user.email = request.POST.get('email')
        custom_user.address = request.POST.get('address')
        if request.POST.get('password') == request.POST.get('confirm_password'):
            user.password = request.POST.get('password')
        else:
            messages.info(request,"Passwords don't match !")
            return redirect('/users/edit_profile')
        custom_user.save()
        user.save()
        return redirect(f'/users/edit_profile')
    else:
        return render(request, 'users/editprofile.html',{'custom_user': custom_user})
    

def help_support(request):
    user = User.objects.filter(username = request.user).first()
    if user:
        custom_user = user.customuser_set.all().first()
        return render(request, 'users/helpsupport.html',{'custom_user': custom_user})
    return render(request,'users/helpsupport.html')

def about(request):
    user = User.objects.filter(username = request.user).first()
    if user:
        custom_user = user.customuser_set.all().first()
        return render(request, 'users/about.html',{'custom_user': custom_user})
    return render(request,'users/about.html')

def contact(request):
    user = User.objects.filter(username = request.user).first()
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        email_message = EmailMessage(
            subject=subject,
            body=f"Message from {name} ({email}):\n\n{message}",
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.EMAIL_HOST_USER],
            headers={'Reply-To': email},  
        )

        email_message.send(fail_silently=False)
        messages.info(request,"Your message has been sent !")
        return redirect('/users/contact')
    else:
        if user:
            custom_user = user.customuser_set.all().first()
            return render(request, 'users/contact.html',{'custom_user': custom_user})
        return render(request,'users/contact.html')

def home(request):
    user = User.objects.filter(username = request.user).first()
    categories = Category.objects.all()
    if user:
        custom_user = user.customuser_set.all().first()
        return render(request, 'users/home.html',{'custom_user': custom_user,'categories':categories})
    else:
        return render(request,'users/home.html',{'categories':categories})

def products(request):
    products = Product.objects.all()
    user = User.objects.filter(username = request.user).first()
    categories = Category.objects.all()
    if user:
        custom_user = user.customuser_set.all().first()
        return render(request, 'products/products.html',{'custom_user': custom_user, 'products': products,'categories':categories})
    else:
        return render(request,'products/products.html',{ 'products' : products })

def product(request,id):
    product = Product.objects.get(id=id)
    return render(request,'products/product.html',{'product':product})

@login_required(login_url='/users/login')
def cart(request):
    cart,created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    return render(request,'products/cart.html',{'cart':cart,'cart_items':cart_items})

@login_required(login_url='/users/login')
def add_to_cart(request,id):
    product = Product.objects.get(id=id)
    cart,created = Cart.objects.get_or_create(user = request.user)
    cart_item,created = CartItem.objects.get_or_create(cart = cart,product = product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return JsonResponse({
        'success': True,
        'message': f"{product.name} added to Cart Successfully"
    })

@login_required(login_url='/users/login')
def add_item(request,id):
    product = Product.objects.get(id=id)
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(cart=cart,product=product)
    cart_item.add_item()
    print(cart_item.quantity)
    return JsonResponse({
        'success': True,
        'quantity': cart_item.quantity,
        'total_price': cart.cart_price
    })

@login_required(login_url='/users/login')
def remove_item(request,id):
    product = Product.objects.get(id=id)
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(cart=cart,product=product)
    if cart_item.remove_item():
        quantity = cart_item.quantity
    else:
        quantity = 0
    return JsonResponse({
        'success': True,
        'quantity': quantity,
        'total_price': cart.cart_price
    })

def search_products(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    price_range = request.GET.get('price_range')

    products = Product.objects.all()

    # Filter by search query
    if query:
        products = products.filter(name__icontains=query)

    # Filter by category
    if category_id:
        products = products.filter(categories__icontains=category_id)

    # Filter by price range
    if price_range:
        price_min, price_max = map(int, price_range.split('-'))
        products = products.filter(price__gte=price_min, price__lte=price_max)

    categories = Category.objects.all()
    
    return render(request, 'products/products.html', {
        'products': products,
        'categories': categories,
        'request': request
    })

def buy_now(request):
    return render(request,'/products/buynow.html',{})