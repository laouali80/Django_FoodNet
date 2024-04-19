from django.test import TestCase, Client
from django.db.models import Max

from .models import User, Order, OrderItem, Product, Category, ShippingAddress

# Create your tests here.

class FoodNetTest(TestCase):

    def setUp(self):
        # create users
        test = User.objects.create_user(first_name='test', last_name='test', middle_name = 'test', username='test'
                                                , email='t@gmail.com', password='t1234', phone_number='12345', address1='s1', address2='s2'
                                                , state='a1', city='c1', zipcode='r1')
        test2 = User.objects.create_user(last_name='test2', middle_name = 'test2', username='test2'
                                                , email='t2@gmail.com', password='t1234', phone_number='12345', address1='s1', address2='s2'
                                                , state='a1', city='c1', zipcode='r1')
        test3 = User.objects.create_user(first_name='test3', middle_name = 'test3', username='test3'
                                                , email='t3@gmail.com', password='t1234', phone_number='12345', address1='s1', address2='s2'
                                                , state='a1', city='c1', zipcode='r1')
        test4 = User.objects.create_user(first_name='test4', last_name='test4', username='test4'
                                                , email='t4@gmail.com', password='t1234', phone_number='12345', address1='s1', address2='s2'
                                                , state='a1', city='c1', zipcode='r1')
        test5 = User.objects.create_user(first_name='test5', last_name='test5', middle_name = 'test5', username='test5'
                                                , email='t5@gmail.com', phone_number='12345', address1='s1', address2='s2'
                                                , state='a1', city='c1', zipcode='r1')
        test6 = User.objects.create_user(first_name='test6', last_name='test6', middle_name = 'test6', username='test6'
                                                , email='t6@gmail.com', password='t1234', address1='s1', address2='s2'
                                                , state='a1', city='c1', zipcode='r1')
        test7 = User.objects.create_user(first_name='test7', last_name='test7', middle_name = 'test7', username='test7'
                                                , email='t7@gmail.com', password='t1234', phone_number='12345', address2='s2'
                                                , state='a1', city='c1', zipcode='r1')
        test8 = User.objects.create_user(first_name='test8', last_name='test8', middle_name = 'test8', username='test8'
                                                , email='t8@gmail.com', password='t1234', phone_number='12345', address1='s1'
                                                , state='a1', city='c1', zipcode='r1')
        test9 = User.objects.create_user(first_name='test9', last_name='test9', middle_name = 'test9', username='test9'
                                                , email='t9@gmail.com', password='t1234', phone_number='12345', address1='s1', address2='s2'
                                                , city='c1', zipcode='r1')
        test10 = User.objects.create_user(first_name='test10', last_name='test10', middle_name = 'test10', username='test10'
                                                , email='t10@gmail.com', password='t1234', phone_number='12345', address1='s1', address2='s2'
                                                , state='a1', zipcode='r1')
        test11 = User.objects.create_user(first_name='test11', last_name='test11', middle_name = 'test11', username='test11'
                                                , email='t11@gmail.com', password='t1234', phone_number='12345', address1='s1', address2='s2'
                                                , state='a1', city='c1')
        test13 = User.objects.create_user(first_name='test13', last_name='test13', middle_name = 'test13', username='test13'
                                                , password='t1234', phone_number='12345', address1='s1', address2='s2'
                                                , state='a1', city='c1', zipcode='r1')

        # create category
        c1 = Category.objects.create(category="Food")
        c2 = Category.objects.create(category="Drink")
        c3 = Category.objects.create(category="Snack")

        # create products
        p1 = Product.objects.create(name='chips', description='description', price=100, category=c1, vendor=test) # correct
        p2 = Product.objects.create(description='description2', price=200, category=c2, vendor=test2)   # no name
        p3 = Product.objects.create(name='sweet', description='description3', price=-100, category=c3, vendor=test) # wrong price
        p4 = Product.objects.create(name='pizza', price=0, vendor=test2)    # no category and wrong price
        p5 = Product.objects.create(name='burger', description='description5', price=200, vendor=test2) # no category
        p11 = Product.objects.create(name='rice', description='good', price=50, category=c1, vendor=test11)

        # create orders
        o1 = Order.objects.create(client=test, transaction_id='15042024')
        o2 = Order.objects.create(client=test2, transaction_id='16042024')
        o11 = Order.objects.create(client=test11, transaction_id='17042024')
        o3 = Order.objects.create(client=test3, transaction_id='18042024')
        

        # create order Items
        oI1 = OrderItem.objects.create(product=p1, order=o1, quantity=3)
        oI2 = OrderItem.objects.create(product=p2, order=o1, quantity=2)
        oI3 = OrderItem.objects.create(product=p1, order=o2, quantity=1)
        oI4 = OrderItem.objects.create(product=p3, order=o1, quantity=-3)
        oI5 = OrderItem.objects.create(product=p4, order=o2, quantity=0)
        oI11 = OrderItem.objects.create(product=p1, order=o11, quantity=4)

        # create shipping
        s1 = ShippingAddress.objects.create(client=test11, order=o11, name=test11.first_name, phone_number=test11.phone_number, address=test11.address1, state=test11.state, city=test11.city)
        s2 = ShippingAddress.objects.create(client=test, order=o1, name=test.first_name ,phone_number=test.phone_number, address=test.address1, state=test.state, city=test.city)
        s3 = ShippingAddress.objects.create(client=test2, order=o2, name=test2.first_name ,phone_number=test2.phone_number, address=test2.address1, state=test2.state, city=test2.city)
        s4 = ShippingAddress.objects.create(client=test3, order=o11, phone_number=test3.phone_number, address=test3.address1, state=test3.state, city=test3.city)
        s5 = ShippingAddress.objects.create(client=test4, order=o1, name=test4.first_name, address=test4.address1, state=test4.state, city=test4.city)
        s6 = ShippingAddress.objects.create(client=test5, order=o2, name=test5.first_name, phone_number=test5.phone_number, state=test5.state, city=test5.city)
        s7 = ShippingAddress.objects.create(client=test6, order=o11, name=test6.first_name ,phone_number=test6.phone_number, address=test6.address1, city=test6.city)
        s8 = ShippingAddress.objects.create(client=test7, order=o1, name=test7.first_name ,phone_number=test7.phone_number, address=test7.address1, state=test7.state)
        


    # Tests on the models (User, Order, OrderItem, Product, Category, ShippingAddress)

    def test_valid_user(self):
        """Check valid users"""
        
        # User with all infomation
        u1 = User.objects.get(username='test')
        self.assertTrue(u1.valid_user())

        # User without middle name
        u4 = User.objects.get(username='test4')
        self.assertTrue(u4.valid_user())
        
        # User Without password
        u5 = User.objects.get(username='test5')
        self.assertTrue(u5.valid_user())

        # User Without address2
        u8 = User.objects.get(username='test8')
        self.assertTrue(u8.valid_user())

        # User without zip code
        u11 = User.objects.get(username='test11')
        self.assertTrue(u11.valid_user())

    def test_invalid_user(self):
        """Check the invalid users"""

        # User without firstname
        u2 = User.objects.get(username='test2')
        self.assertFalse(u2.valid_user())

    	# User Without
        u3 = User.objects.get(username='test3')
        self.assertFalse(u3.valid_user())
        
        # User Without phone number
        u6 = User.objects.get(username='test6')
        self.assertFalse(u6.valid_user())
        
        # User Without address1
        u7 = User.objects.get(username='test7')
        self.assertFalse(u7.valid_user())
        
        # User Without state
        u9 = User.objects.get(username='test9')
        self.assertFalse(u9.valid_user())
        
        # User Without city
        u10 = User.objects.get(username='test10')
        self.assertFalse(u10.valid_user())

        # User Without email
        u13 = User.objects.get(username='test13')
        self.assertFalse(u13.valid_user())

    def test_valid_product(self):
        """Check the valid product"""

        # A correct Product
        p1 = Product.objects.get(name='chips')
        self.assertTrue(p1.valid_product())

        # A correct Product
        p11 = Product.objects.get(name='rice')
        self.assertTrue(p11.valid_product())

    def test_invalid_product(self):
        """Check the invalid product"""

        # A product without name
        p2 = Product.objects.get(description='description2')
        self.assertFalse(p2.valid_product())

        # A product with -100 (negative price)
        p3 = Product.objects.get(name='sweet')
        self.assertFalse(p3.valid_product())

        # A product with 0 (zero price)
        p4 = Product.objects.get(name='pizza')
        self.assertFalse(p4.valid_product())

        # A product without category
        p5 = Product.objects.get(name='burger')
        self.assertFalse(p5.valid_product())

    def test_valid_order(self):
        """Check valid order creation"""

        # valid creation of order
        o1 = Order.objects.get(transaction_id='15042024')
        self.assertTrue(o1.valid_order())

        # valid creation of order
        o11 = Order.objects.get(transaction_id='17042024')
        self.assertTrue(o11.valid_order())

    def test_invalid_order(self):
        """Check the invalid order creation"""

        # invalid order because of the user invalidation
        o2 = Order.objects.get(transaction_id='16042024')
        self.assertFalse(o2.valid_order())

    def test_valid_orderItem(self):
        """Check the valid order Item"""

        # different vendor and client
        oI11 = OrderItem.objects.get(quantity=4)
        self.assertTrue(oI11.valid_orderItem())

    def test_invalid_orderItem(self):
        """Check the invalid Order Item"""

        # same vendor and order client
        oI1 = OrderItem.objects.get(quantity=3)
        self.assertFalse(oI1.valid_orderItem())

        # invalid product (name)
        oI2 = OrderItem.objects.get(quantity=2)
        self.assertFalse(oI2.valid_orderItem())

        # invalid order (client)
        oI3 = OrderItem.objects.get(quantity=1)
        self.assertFalse(oI3.valid_orderItem())

        # invalid quantity
        oI4 = OrderItem.objects.get(quantity=-3)
        self.assertFalse(oI4.valid_orderItem())

        # invalid quantity and product (name)
        oI5 = OrderItem.objects.get(quantity=0)
        self.assertFalse(oI5.valid_orderItem())

    def test_valid_shipping(self):
        """Check the valid shipping"""

        # correct shipping
        u11 = User.objects.get(username='test11')
        s1 = ShippingAddress.objects.get(client=u11)
        self.assertTrue(s1.valid_shipping())

        # valid shipping information
        u1 = User.objects.get(username='test')
        s2 = ShippingAddress.objects.get(client=u1)
        self.assertTrue(s2.valid_shipping())

    def test_invalid_shipping(self):
        """Check the invalid shipping"""

        # invalid user
        u2 = User.objects.get(username='test2')
        s3 = ShippingAddress.objects.get(client=u2)
        self.assertFalse(s3.valid_shipping())

        # missing name, invalid user and client diff from order client
        u3 = User.objects.get(username='test3')
        s4 = ShippingAddress.objects.get(client=u3)
        self.assertFalse(s4.valid_shipping())

        # missing phone number, invalid user and client diff from order client
        u4 = User.objects.get(username='test4')
        s5 = ShippingAddress.objects.get(client=u4)
        self.assertFalse(s5.valid_shipping())

        # missing address and client diff from order client
        u5 = User.objects.get(username='test5')
        s6 = ShippingAddress.objects.get(client=u5)
        self.assertFalse(s6.valid_shipping())

        # missing address and client diff from order client
        u6 = User.objects.get(username='test6')
        s7 = ShippingAddress.objects.get(client=u6)
        self.assertFalse(s7.valid_shipping())

        # missing address and client diff from order client
        u7 = User.objects.get(username='test7')
        s8 = ShippingAddress.objects.get(client=u7)
        self.assertFalse(s8.valid_shipping())

    def test_user_number_SellingProduct(self):
        """Check the total product of a user."""

        u1 = User.objects.get(username='test')
        self.assertEqual(u1.selling_products.count(), 2)

        u2 = User.objects.get(username="test2")
        self.assertEqual(u2.selling_products.count(), 3)

        u11 = User.objects.get(username="test11")
        self.assertEqual(u11.selling_products.count(), 1)

        u3 = User.objects.get(username="test3")
        self.assertEqual(u3.selling_products.count(), 0)

    def test_user_number_orders(self):
        """Check the number of orders of a user."""

        u1 = User.objects.get(username='test')
        self.assertEqual(u1.orders.count(), 1)

        u2 = User.objects.get(username="test2")
        self.assertEqual(u2.orders.count(), 1)

        u11 = User.objects.get(username="test11")
        self.assertEqual(u11.orders.count(), 1)

        u3 = User.objects.get(username="test3")
        self.assertEqual(u3.orders.count(), 1)

        u4 = User.objects.get(username="test4")
        self.assertEqual(u4.orders.count(), 0)

    def test_user_number_shipping(self):
        """Check the total orders shipping to a user."""

        u1 = User.objects.get(username='test')
        self.assertEqual(u1.user_shipping.count(), 1)

        u2 = User.objects.get(username="test2")
        self.assertEqual(u2.user_shipping.count(), 1)

        u11 = User.objects.get(username="test11")
        self.assertEqual(u11.user_shipping.count(), 1)

        u8 = User.objects.get(username="test8")
        self.assertEqual(u8.user_shipping.count(), 0)

    def test_total_order_product(self):
        """Check the total number products being order"""

        p1 = Product.objects.get(name='chips')
        self.assertEqual(p1.order_products.count(), 3)

        p2 = Product.objects.get(description='description2')
        self.assertEqual(p2.order_products.count(), 1)

        p3 = Product.objects.get(name='sweet')
        self.assertEqual(p3.order_products.count(), 1)

        p4 = Product.objects.get(name='pizza')
        self.assertEqual(p4.order_products.count(), 1)

        p5 = Product.objects.get(name='burger')
        self.assertEqual(p5.order_products.count(), 0)

        p11 = Product.objects.get(name='rice')
        self.assertEqual(p11.order_products.count(), 0)

    def test_total_num_items_in_order(self):
        """Check the total number of items in an order."""

        o1 = Order.objects.get(transaction_id='15042024')
        self.assertEqual(o1.order_items.count(), 3)

        o2 = Order.objects.get(transaction_id='16042024')
        self.assertEqual(o2.order_items.count(), 2)

        o11 = Order.objects.get(transaction_id='17042024')
        self.assertEqual(o11.order_items.count(), 1)

        o3 = Order.objects.get(transaction_id='18042024')
        self.assertEqual(o3.order_items.count(), 0)

    def test_order_number_shipping(self):
        """Check the total number of shipping of an order."""

        o1 = Order.objects.get(transaction_id='15042024')
        self.assertEqual(o1.order_shipping.count(), 3)

        o2 = Order.objects.get(transaction_id='16042024')
        self.assertEqual(o2.order_shipping.count(), 2)

        o11 = Order.objects.get(transaction_id='17042024')
        self.assertEqual(o11.order_shipping.count(), 3)

        o3 = Order.objects.get(transaction_id='18042024')
        self.assertEqual(o3.order_shipping.count(), 0)


    # Tests on the routes(views)

    def test_home_page(self):
        """"check the response of the index route(view) with its context"""
        c = Client()
        c.login(username='test', password='t1234')
        response = c.get("/foodNet/home/")

        self.assertEqual(response.status_code, 302)
        c.logout()

        response = c.get("/foodNet/home/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("foodnet/home_page.html", [template.name for template in response.templates ])

    def test_login(self):
        """"""
        pass

    def test_register(self):
        pass
        
        