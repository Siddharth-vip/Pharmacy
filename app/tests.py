from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from app.models import CustomUser, Product, Cart, CartItem, Order, OrderItem
from decimal import Decimal

User = get_user_model()

class MedicoMartWorkflowTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create User A
        self.user_a = User.objects.create_user(username='usera', email='usera@example.com', password='password123')
        self.custom_user_a = CustomUser.objects.create(
            user=self.user_a,
            contact_number='9876543210',
            address='123 Green Valley Road, City A @ 456 Palm Grove, City A'
        )

        # Create User B
        self.user_b = User.objects.create_user(username='userb', email='userb@example.com', password='password123')
        self.custom_user_b = CustomUser.objects.create(
            user=self.user_b,
            contact_number='9876543211',
            address='789 River Side, City B'
        )

        # Create Products
        self.prod_a = Product.objects.create(
            name='Product A - Vitamin C 1000mg',
            price=Decimal('250.00'),
            stock=50,
            is_available=True,
            weight=100,
            categories='vitamins,immunity'
        )
        self.prod_b = Product.objects.create(
            name='Product B - Ashwagandha Pure Extract',
            price=Decimal('450.00'),
            stock=30,
            is_available=True,
            weight=150,
            categories='ayurveda,wellness'
        )
        self.prod_c = Product.objects.create(
            name='Product C - Omega 3 Fish Oil',
            price=Decimal('600.00'),
            stock=20,
            is_available=True,
            weight=200,
            categories='supplements'
        )

    # TEST 1 & 6: Cart Checkout with COD
    def test_cart_checkout_cod_success(self):
        self.client.login(username='usera', password='password123')
        
        # Add Prod A and Prod B to cart
        self.client.post(f'/add_to_cart/{self.prod_a.id}/')
        self.client.post(f'/add_to_cart/{self.prod_b.id}/')
        
        cart = Cart.objects.get(user=self.user_a)
        self.assertEqual(cart.cartitem_set.count(), 2)

        # Proceed to place order with COD
        address = self.custom_user_a.get_addresses()[0]
        response = self.client.post('/place_order/', {
            'checkout_mode': 'cart',
            'delivery_address': address,
            'payment_method': 'Cash on Delivery'
        })
        
        # Should redirect to order success
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/order_success/' in response.url)

        # Verify Order was created
        order = Order.objects.filter(user=self.user_a).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.total_amount, Decimal('700.00'))
        self.assertEqual(order.payment_method, 'Cash on Delivery')
        self.assertEqual(order.payment_status, 'PENDING')
        self.assertEqual(order.order_status, 'CONFIRMED')
        self.assertEqual(order.items.count(), 2)

        # Cart should be empty
        self.assertEqual(cart.cartitem_set.count(), 0)

        # My Orders page should contain this order and products
        orders_resp = self.client.get('/orders/')
        self.assertEqual(orders_resp.status_code, 200)
        self.assertContains(orders_resp, 'Product A - Vitamin C 1000mg')
        self.assertContains(orders_resp, 'Product B - Ashwagandha Pure Extract')
        self.assertContains(orders_resp, order.order_id)

    # TEST 2: Address Required Validation
    def test_address_required_validation(self):
        self.client.login(username='usera', password='password123')
        self.client.post(f'/add_to_cart/{self.prod_a.id}/')

        # Submit without delivery address
        response = self.client.post('/place_order/', {
            'checkout_mode': 'cart',
            'delivery_address': '',
            'payment_method': 'Cash on Delivery'
        })
        
        self.assertEqual(response.status_code, 302)
        # Order should NOT be created
        self.assertEqual(Order.objects.count(), 0)

    # TEST 3: Payment Method Required Validation
    def test_payment_method_required_validation(self):
        self.client.login(username='usera', password='password123')
        self.client.post(f'/add_to_cart/{self.prod_a.id}/')

        address = self.custom_user_a.get_addresses()[0]
        # Submit without payment method
        response = self.client.post('/place_order/', {
            'checkout_mode': 'cart',
            'delivery_address': address,
            'payment_method': ''
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 0)

    # TEST 4: UPI Payment Unavailable Validation
    def test_upi_payment_unavailable(self):
        self.client.login(username='usera', password='password123')
        self.client.post(f'/add_to_cart/{self.prod_a.id}/')

        address = self.custom_user_a.get_addresses()[0]
        response = self.client.post('/place_order/', {
            'checkout_mode': 'cart',
            'delivery_address': address,
            'payment_method': 'UPI'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 0)

    # TEST 5: Card Payment Unavailable Validation
    def test_card_payment_unavailable(self):
        self.client.login(username='usera', password='password123')
        self.client.post(f'/add_to_cart/{self.prod_a.id}/')

        address = self.custom_user_a.get_addresses()[0]
        response = self.client.post('/place_order/', {
            'checkout_mode': 'cart',
            'delivery_address': address,
            'payment_method': 'Card'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 0)

    # TEST 7 & 8: User Isolation in Orders
    def test_user_orders_isolation(self):
        # Create order for User A
        order_a = Order.objects.create(
            order_id='ORD-10001',
            user=self.user_a,
            total_amount=Decimal('250.00'),
            delivery_address='User A Address',
            payment_method='Cash on Delivery',
            payment_status='PENDING',
            order_status='CONFIRMED'
        )
        OrderItem.objects.create(
            order=order_a,
            product=self.prod_a,
            product_name=self.prod_a.name,
            quantity=1,
            unit_price=self.prod_a.price,
            subtotal=self.prod_a.price
        )

        # Create order for User B
        order_b = Order.objects.create(
            order_id='ORD-10002',
            user=self.user_b,
            total_amount=Decimal('600.00'),
            delivery_address='User B Address',
            payment_method='Cash on Delivery',
            payment_status='PENDING',
            order_status='CONFIRMED'
        )
        OrderItem.objects.create(
            order=order_b,
            product=self.prod_c,
            product_name=self.prod_c.name,
            quantity=1,
            unit_price=self.prod_c.price,
            subtotal=self.prod_c.price
        )

        # Login as User A
        self.client.login(username='usera', password='password123')
        resp = self.client.get('/orders/')
        self.assertContains(resp, 'ORD-10001')
        self.assertContains(resp, 'Product A - Vitamin C 1000mg')
        self.assertNotContains(resp, 'ORD-10002')
        self.assertNotContains(resp, 'Product C - Omega 3 Fish Oil')

        # User A attempting to view User B's order detail should get 404
        detail_resp = self.client.get(f'/orders/{order_b.order_id}/')
        self.assertEqual(detail_resp.status_code, 404)

        # Login as User B
        self.client.login(username='userb', password='password123')
        resp_b = self.client.get('/orders/')
        self.assertContains(resp_b, 'ORD-10002')
        self.assertContains(resp_b, 'Product C - Omega 3 Fish Oil')
        self.assertNotContains(resp_b, 'ORD-10001')
        self.assertNotContains(resp_b, 'Product A - Vitamin C 1000mg')

    # TEST 9, 11, 12, 13: Buy Now Flow (Independent of Cart)
    def test_buy_now_flow_does_not_modify_cart(self):
        self.client.login(username='usera', password='password123')

        # Cart contains Prod B and Prod C
        self.client.post(f'/add_to_cart/{self.prod_b.id}/')
        self.client.post(f'/add_to_cart/{self.prod_c.id}/')
        cart = Cart.objects.get(user=self.user_a)
        self.assertEqual(cart.cartitem_set.count(), 2)

        # Buy Now on Prod A with quantity 3
        checkout_resp = self.client.get(f'/checkout/?mode=buy_now&product_id={self.prod_a.id}&quantity=3')
        self.assertEqual(checkout_resp.status_code, 200)
        self.assertContains(checkout_resp, 'Product A - Vitamin C 1000mg')
        self.assertNotContains(checkout_resp, 'Product B - Ashwagandha')
        self.assertNotContains(checkout_resp, 'Product C - Omega 3')

        # Place COD order for Buy Now
        address = self.custom_user_a.get_addresses()[0]
        place_resp = self.client.post('/place_order/', {
            'checkout_mode': 'buy_now',
            'product_id': str(self.prod_a.id),
            'quantity': '3',
            'delivery_address': address,
            'payment_method': 'Cash on Delivery'
        })
        self.assertEqual(place_resp.status_code, 302)

        # Order created with Product A, qty 3, total 750
        order = Order.objects.filter(user=self.user_a, checkout_mode='buy_now').first()
        self.assertIsNotNone(order)
        self.assertEqual(order.total_amount, Decimal('750.00'))
        self.assertEqual(order.items.count(), 1)
        item = order.items.first()
        self.assertEqual(item.product_name, self.prod_a.name)
        self.assertEqual(item.quantity, 3)

        # Cart MUST still contain Product B and Product C!
        cart.refresh_from_db()
        self.assertEqual(cart.cartitem_set.count(), 2)
        cart_product_names = [ci.product.name for ci in cart.cartitem_set.all()]
        self.assertIn(self.prod_b.name, cart_product_names)
        self.assertIn(self.prod_c.name, cart_product_names)

        # My Orders shows the Buy Now order
        orders_resp = self.client.get('/orders/')
        self.assertContains(orders_resp, order.order_id)
        self.assertContains(orders_resp, 'Product A - Vitamin C 1000mg')

    # TEST 10: Buy Now when Logged Out (Redirect to login, then continue to Buy Now)
    def test_buy_now_logged_out_redirects_and_continues(self):
        # User is logged out
        self.client.logout()

        # Access Buy Now checkout while logged out
        target_checkout_url = f'/checkout/?mode=buy_now&product_id={self.prod_a.id}&quantity=2'
        resp = self.client.get(target_checkout_url)
        # Should redirect to login with next
        self.assertEqual(resp.status_code, 302)
        self.assertTrue('/users/login/' in resp.url)

        # Login with next parameter
        login_resp = self.client.post('/users/login/', {
            'username': 'usera',
            'password': 'password123',
            'next': target_checkout_url
        })
        
        # Should redirect directly to target Buy Now checkout, NOT /cart!
        self.assertEqual(login_resp.status_code, 302)
        self.assertEqual(login_resp.url, target_checkout_url)

        # Following redirect renders Buy Now checkout with Product A and quantity 2
        follow_resp = self.client.get(target_checkout_url)
        self.assertEqual(follow_resp.status_code, 200)
        self.assertContains(follow_resp, 'Product A - Vitamin C 1000mg')
        self.assertContains(follow_resp, 'Quantity: <strong class="text-brand-dark font-semibold">2</strong>')
