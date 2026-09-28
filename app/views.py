from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
import uuid
from .models import CustomUser, Product, Cart, CartItem, Category, Order, OrderItem

User = get_user_model()

def register(request):
    next_url = request.GET.get('next') or request.POST.get('next') or ''
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2 and email and username and contact_number:
            if User.objects.filter(email = email).exists():
                messages.info(request, "Email already taken")
                return render(request, 'users/register.html', {'next': next_url})
            elif CustomUser.objects.filter(contact_number = contact_number).exists():
                messages.info(request, "Contact Number already taken")
                return render(request, 'users/register.html', {'next': next_url})
            elif User.objects.filter(username = username).exists():
                messages.info(request, "Username already taken")
                return render(request, 'users/register.html', {'next': next_url})
            else:
                user = User.objects.create_user(username = username, email = email, password = password1)
                user.save()
                custom_user = CustomUser.objects.create(user = user, contact_number = contact_number)
                custom_user.save()
                messages.success(request, "Registration successful! Please sign in.")
                if next_url:
                    return redirect(f"/users/login/?next={next_url}")
                return redirect('login')
        else:
            messages.info(request,"Fill all details correctly and ensure passwords match!")
            return render(request, 'users/register.html', {'next': next_url})
    else:
        return render(request, 'users/register.html', {'next': next_url})

def user_login(request):
    next_url = request.POST.get('next') or request.GET.get('next') or ''
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = None

        if "@" in username:
            user_model = User.objects.filter(email=username).first()
            if user_model:
                user = authenticate(username=user_model.username, password=password)
        else:
            custom_user = CustomUser.objects.filter(contact_number=username).first()
            if custom_user:
                user = authenticate(username=custom_user.user.username, password=password)
            elif User.objects.filter(username=username).exists():
                user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials!")
            return render(request, 'users/login.html', {'next': next_url})
    else:
        return render(request, 'users/login.html', {'next': next_url})
    
@login_required(login_url='/users/login/')
def user_logout(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/users/login/')
def edit_profile(request):
    user = request.user
    custom_user = CustomUser.objects.filter(user=user).first()
    if request.method == "POST":
        if request.FILES.get('image'):
            custom_user.profile_image = request.FILES.get('image')
        custom_user.contact_number = request.POST.get('phone', custom_user.contact_number)
        user.username = request.POST.get('name', user.username)
        user.email = request.POST.get('email', user.email)
        custom_user.address = request.POST.get('address', '')
        
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if new_password or confirm_password:
            if new_password == confirm_password:
                user.set_password(new_password)
            else:
                messages.info(request, "Passwords don't match!")
                return redirect('edit_profile')
        custom_user.save()
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('edit_profile')
    else:
        return render(request, 'users/editprofile.html', {'custom_user': custom_user})

def help_support(request):
    custom_user = None
    if request.user.is_authenticated:
        custom_user = CustomUser.objects.filter(user=request.user).first()
    return render(request, 'users/helpsupport.html', {'custom_user': custom_user})

def wellness(request):
    custom_user = None
    if request.user.is_authenticated:
        custom_user = CustomUser.objects.filter(user=request.user).first()
    return render(request, 'users/wellness.html', {'custom_user': custom_user})

def about(request):
    custom_user = None
    if request.user.is_authenticated:
        custom_user = CustomUser.objects.filter(user=request.user).first()
    return render(request, 'users/about.html', {'custom_user': custom_user})

def contact(request):
    custom_user = None
    if request.user.is_authenticated:
        custom_user = CustomUser.objects.filter(user=request.user).first()
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
        try:
            email_message.send(fail_silently=False)
            messages.info(request,"Your message has been sent!")
        except Exception:
            messages.info(request,"Message received! We will get back to you shortly.")
        return redirect('contact')
    else:
        return render(request, 'users/contact.html', {'custom_user': custom_user})

def home(request):
    custom_user = None
    if request.user.is_authenticated:
        custom_user = CustomUser.objects.filter(user=request.user).first()
    categories = Category.objects.all()
    featured_products = Product.objects.all()[:8]
    return render(request, 'users/home.html', {
        'custom_user': custom_user,
        'categories': categories,
        'featured_products': featured_products,
        'products': featured_products
    })

def products(request):
    products = Product.objects.all()
    custom_user = None
    if request.user.is_authenticated:
        custom_user = CustomUser.objects.filter(user=request.user).first()
    categories = Category.objects.all()
    return render(request, 'products/products.html', {
        'custom_user': custom_user,
        'products': products,
        'categories': categories
    })

def product(request, id):
    product = get_object_or_404(Product, id=id)
    custom_user = None
    if request.user.is_authenticated:
        custom_user = CustomUser.objects.filter(user=request.user).first()
    related_products = Product.objects.exclude(id=id)[:6]
    return render(request, 'products/product.html', {
        'product': product,
        'custom_user': custom_user,
        'related_products': related_products
    })

@login_required(login_url='/users/login/')
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    custom_user = CustomUser.objects.filter(user=request.user).first()
    return render(request, 'products/cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        'custom_user': custom_user
    })

@login_required(login_url='/users/login/')
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return JsonResponse({
        'success': True,
        'message': f"{product.name} added to Cart Successfully"
    })

@login_required(login_url='/users/login/')
def add_item(request, id):
    product = get_object_or_404(Product, id=id)
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.add_item()
    return JsonResponse({
        'success': True,
        'quantity': cart_item.quantity,
        'total_price': cart.cart_price
    })

@login_required(login_url='/users/login/')
def remove_item(request, id):
    product = get_object_or_404(Product, id=id)
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(cart=cart, product=product)
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

    if query:
        products = products.filter(name__icontains=query)

    if category_id:
        products = products.filter(categories__icontains=category_id)

    if price_range:
        parts = price_range.split('-')
        if len(parts) == 2:
            price_min, price_max = map(int, parts)
            products = products.filter(price__gte=price_min, price__lte=price_max)
        elif price_range.endswith('+') or price_range == '10000+':
            products = products.filter(price__gte=10000)

    categories = Category.objects.all()
    custom_user = None
    if request.user.is_authenticated:
        custom_user = CustomUser.objects.filter(user=request.user).first()
    
    return render(request, 'products/products.html', {
        'products': products,
        'categories': categories,
        'custom_user': custom_user,
        'request': request
    })

@login_required(login_url='/users/login/')
def checkout(request):
    mode = request.GET.get('mode', 'cart')
    product_id = request.GET.get('product_id')
    custom_user = CustomUser.objects.filter(user=request.user).first()
    addresses = custom_user.get_addresses() if custom_user else []

    checkout_items = []
    total_price = 0
    quantity = 1

    if mode == 'buy_now' and product_id:
        product = get_object_or_404(Product, id=product_id)
        if not product.is_available:
            messages.error(request, f"{product.name} is currently out of stock.")
            return redirect('products')
        try:
            quantity = max(1, int(request.GET.get('quantity', 1)))
        except (ValueError, TypeError):
            quantity = 1
        subtotal = product.price * quantity
        checkout_items.append({
            'product': product,
            'quantity': quantity,
            'unit_price': product.price,
            'subtotal': subtotal,
        })
        total_price = subtotal
    else:
        mode = 'cart'
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.cartitem_set.all()
        if not cart_items.exists():
            messages.info(request, "Your cart is empty. Add products to proceed with checkout.")
            return redirect('cart')
        for item in cart_items:
            checkout_items.append({
                'product': item.product,
                'quantity': item.quantity,
                'unit_price': item.product.price,
                'subtotal': item.total_price,
            })
        total_price = cart.cart_price

    return render(request, 'products/checkout.html', {
        'custom_user': custom_user,
        'addresses': addresses,
        'checkout_items': checkout_items,
        'total_price': total_price,
        'checkout_mode': mode,
        'product_id': product_id or '',
        'quantity': quantity,
    })

@login_required(login_url='/users/login/')
def buy_now(request):
    product_id = request.GET.get('product_id')
    quantity = request.GET.get('quantity', 1)
    if product_id:
        return redirect(f"/checkout/?mode=buy_now&product_id={product_id}&quantity={quantity}")
    return redirect('checkout')

@login_required(login_url='/users/login/')
def place_order(request):
    if request.method != 'POST':
        return redirect('checkout')

    checkout_mode = request.POST.get('checkout_mode', 'cart')
    product_id = request.POST.get('product_id')
    quantity_str = request.POST.get('quantity', '1')
    delivery_address = request.POST.get('delivery_address', '').strip()
    payment_method = request.POST.get('payment_method', '').strip()

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json'

    # Validation: Delivery Address
    if not delivery_address:
        msg = "Please select a delivery address to continue."
        if is_ajax:
            return JsonResponse({'success': False, 'message': msg}, status=400)
        messages.error(request, msg)
        redirect_url = f"/checkout/?mode={checkout_mode}"
        if checkout_mode == 'buy_now' and product_id:
            redirect_url += f"&product_id={product_id}&quantity={quantity_str}"
        return redirect(redirect_url)

    # Validation: Payment Method
    if not payment_method:
        msg = "Please select a payment method to continue."
        if is_ajax:
            return JsonResponse({'success': False, 'message': msg}, status=400)
        messages.error(request, msg)
        redirect_url = f"/checkout/?mode={checkout_mode}"
        if checkout_mode == 'buy_now' and product_id:
            redirect_url += f"&product_id={product_id}&quantity={quantity_str}"
        return redirect(redirect_url)

    if payment_method.upper() == 'UPI':
        msg = "UPI payments are currently unavailable. Please select Cash on Delivery."
        if is_ajax:
            return JsonResponse({'success': False, 'message': msg}, status=400)
        messages.error(request, msg)
        redirect_url = f"/checkout/?mode={checkout_mode}"
        if checkout_mode == 'buy_now' and product_id:
            redirect_url += f"&product_id={product_id}&quantity={quantity_str}"
        return redirect(redirect_url)

    if payment_method.upper() in ['CARD', 'CREDIT / DEBIT / ATM CARD', 'CREDIT_CARD']:
        msg = "Card payments are currently unavailable. Please select Cash on Delivery."
        if is_ajax:
            return JsonResponse({'success': False, 'message': msg}, status=400)
        messages.error(request, msg)
        redirect_url = f"/checkout/?mode={checkout_mode}"
        if checkout_mode == 'buy_now' and product_id:
            redirect_url += f"&product_id={product_id}&quantity={quantity_str}"
        return redirect(redirect_url)

    if payment_method.upper() not in ['COD', 'CASH ON DELIVERY']:
        msg = "Unsupported payment method. Please select Cash on Delivery."
        if is_ajax:
            return JsonResponse({'success': False, 'message': msg}, status=400)
        messages.error(request, msg)
        return redirect('checkout')

    # Prepare and validate order items from DB
    items_to_create = []
    total_amount = 0

    if checkout_mode == 'buy_now':
        if not product_id:
            msg = "Product not specified for Buy Now."
            if is_ajax:
                return JsonResponse({'success': False, 'message': msg}, status=400)
            messages.error(request, msg)
            return redirect('products')
        product = Product.objects.filter(id=product_id).first()
        if not product or not product.is_available:
            msg = "Selected product is currently unavailable."
            if is_ajax:
                return JsonResponse({'success': False, 'message': msg}, status=400)
            messages.error(request, msg)
            return redirect('products')
        try:
            qty = max(1, int(quantity_str))
        except (ValueError, TypeError):
            qty = 1
        subtotal = product.price * qty
        total_amount = subtotal
        items_to_create.append((product, qty, product.price, subtotal))
    else:
        # Cart mode
        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.cartitem_set.exists():
            msg = "Your cart is empty."
            if is_ajax:
                return JsonResponse({'success': False, 'message': msg}, status=400)
            messages.error(request, msg)
            return redirect('cart')
        
        for item in cart.cartitem_set.select_related('product').all():
            prod = item.product
            subtotal = prod.price * item.quantity
            total_amount += subtotal
            items_to_create.append((prod, item.quantity, prod.price, subtotal))

    # Transactional order creation
    try:
        with transaction.atomic():
            count = Order.objects.count() + 1
            order_id = f"ORD-{10000 + count}"
            while Order.objects.filter(order_id=order_id).exists():
                order_id = f"ORD-{uuid.uuid4().hex[:6].upper()}"

            custom_user = CustomUser.objects.filter(user=request.user).first()
            contact_number = custom_user.contact_number if custom_user else ''

            order = Order.objects.create(
                order_id=order_id,
                user=request.user,
                total_amount=total_amount,
                delivery_address=delivery_address,
                contact_number=contact_number,
                payment_method='Cash on Delivery',
                payment_status='PENDING',
                order_status='CONFIRMED',
                checkout_mode=checkout_mode
            )

            for prod, qty, unit_pr, sub_pr in items_to_create:
                OrderItem.objects.create(
                    order=order,
                    product=prod,
                    product_name=prod.name,
                    product_image=prod.image if prod else None,
                    product_image_url=prod.image.url if prod and prod.image else '',
                    category=prod.categories if prod else '',
                    quantity=qty,
                    unit_price=unit_pr,
                    subtotal=sub_pr
                )

            # Clear cart ONLY if checking out from cart
            if checkout_mode == 'cart':
                cart = Cart.objects.filter(user=request.user).first()
                if cart:
                    cart.cartitem_set.all().delete()

        if is_ajax:
            return JsonResponse({
                'success': True,
                'order_id': order.order_id,
                'redirect_url': f'/order_success/{order.order_id}/'
            })
        return redirect('order_success', order_id=order.order_id)

    except Exception as e:
        msg = "An error occurred while placing your order. Please try again."
        if is_ajax:
            return JsonResponse({'success': False, 'message': msg, 'error': str(e)}, status=500)
        messages.error(request, msg)
        return redirect('checkout')

@login_required(login_url='/users/login/')
def order_success(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    custom_user = CustomUser.objects.filter(user=request.user).first()
    return render(request, 'products/ordersuccess.html', {
        'order': order,
        'custom_user': custom_user
    })

@login_required(login_url='/users/login/')
def orders(request):
    user_orders = Order.objects.filter(user=request.user).prefetch_related('items')
    custom_user = CustomUser.objects.filter(user=request.user).first()
    return render(request, 'products/orders.html', {
        'orders': user_orders,
        'custom_user': custom_user
    })

@login_required(login_url='/users/login/')
def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    custom_user = CustomUser.objects.filter(user=request.user).first()
    return render(request, 'products/orderdetail.html', {
        'order': order,
        'custom_user': custom_user
    })