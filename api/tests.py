from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Category, Product, Order, OrderItem


class CategoryModelTests(TestCase):
    def test_create_category(self):
        category = Category.objects.create(
            name="Electronics",
            description="Electronic devices and gadgets"
        )
        self.assertEqual(category.name, "Electronics")
        self.assertEqual(str(category), "Electronics")

    def test_category_str_representation(self):
        category = Category.objects.create(name="Books")
        self.assertEqual(str(category), "Books")


class ProductModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")

    def test_create_product(self):
        product = Product.objects.create(
            name="Laptop",
            description="A powerful laptop",
            price=999.99,
            stock=10,
            category=self.category
        )
        self.assertEqual(product.name, "Laptop")
        self.assertEqual(product.price, 999.99)
        self.assertTrue(product.is_active)

    def test_product_str_representation(self):
        product = Product.objects.create(
            name="Phone",
            description="Smartphone",
            price=599.99,
            stock=5,
            category=self.category
        )
        self.assertEqual(str(product), "Phone")


class OrderModelTests(TestCase):
    def test_create_order(self):
        order = Order.objects.create(
            customer_name="John Doe",
            customer_email="john@example.com",
            status="pending",
            total_amount=100.00
        )
        self.assertEqual(order.customer_name, "John Doe")
        self.assertEqual(order.status, "pending")

    def test_order_str_representation(self):
        order = Order.objects.create(
            customer_name="Jane Doe",
            customer_email="jane@example.com"
        )
        self.assertIn("Jane Doe", str(order))


class OrderItemModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Mouse",
            description="Wireless mouse",
            price=29.99,
            stock=50,
            category=self.category
        )
        self.order = Order.objects.create(
            customer_name="Test User",
            customer_email="test@example.com"
        )

    def test_create_order_item(self):
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=29.99
        )
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.product.name, "Mouse")


class CategoryAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(
            name="Test Category",
            description="Test Description"
        )

    def test_list_categories(self):
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_category(self):
        url = reverse('category-list')
        data = {
            'name': 'New Category',
            'description': 'New Description'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    def test_retrieve_category(self):
        url = reverse('category-detail', kwargs={'pk': self.category.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Category')

    def test_update_category(self):
        url = reverse('category-detail', kwargs={'pk': self.category.pk})
        data = {
            'name': 'Updated Category',
            'description': 'Updated Description'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Updated Category')

    def test_delete_category(self):
        url = reverse('category-detail', kwargs={'pk': self.category.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)


class ProductAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=99.99,
            stock=10,
            category=self.category
        )

    def test_list_products(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_product(self):
        url = reverse('product-list')
        data = {
            'name': 'New Product',
            'description': 'New Description',
            'price': 49.99,
            'stock': 5,
            'category': self.category.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_retrieve_product(self):
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product')

    def test_update_product(self):
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        data = {
            'name': 'Updated Product',
            'description': 'Updated Description',
            'price': 149.99,
            'stock': 20,
            'category': self.category.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')

    def test_delete_product(self):
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)


class OrderAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.order = Order.objects.create(
            customer_name="Test Customer",
            customer_email="customer@example.com",
            status="pending",
            total_amount=100.00
        )

    def test_list_orders(self):
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_order(self):
        url = reverse('order-list')
        data = {
            'customer_name': 'New Customer',
            'customer_email': 'new@example.com',
            'status': 'pending',
            'total_amount': 50.00
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)

    def test_retrieve_order(self):
        url = reverse('order-detail', kwargs={'pk': self.order.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer_name'], 'Test Customer')

    def test_update_order(self):
        url = reverse('order-detail', kwargs={'pk': self.order.pk})
        data = {
            'customer_name': 'Updated Customer',
            'customer_email': 'updated@example.com',
            'status': 'processing',
            'total_amount': 150.00
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.customer_name, 'Updated Customer')

    def test_delete_order(self):
        url = reverse('order-detail', kwargs={'pk': self.order.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)


class OrderItemAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Keyboard",
            description="Mechanical keyboard",
            price=79.99,
            stock=20,
            category=self.category
        )
        self.order = Order.objects.create(
            customer_name="Test User",
            customer_email="user@example.com"
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=79.99
        )

    def test_list_order_items(self):
        url = reverse('orderitem-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_order_item(self):
        new_product = Product.objects.create(
            name="Mouse",
            description="Wireless mouse",
            price=29.99,
            stock=30,
            category=self.category
        )
        url = reverse('orderitem-list')
        data = {
            'order': self.order.id,
            'product': new_product.id,
            'quantity': 1,
            'price': 29.99
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrderItem.objects.count(), 2)

    def test_retrieve_order_item(self):
        url = reverse('orderitem-detail', kwargs={'pk': self.order_item.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 2)

    def test_update_order_item(self):
        url = reverse('orderitem-detail', kwargs={'pk': self.order_item.pk})
        data = {
            'order': self.order.id,
            'product': self.product.id,
            'quantity': 5,
            'price': 79.99
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order_item.refresh_from_db()
        self.assertEqual(self.order_item.quantity, 5)

    def test_delete_order_item(self):
        url = reverse('orderitem-detail', kwargs={'pk': self.order_item.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(OrderItem.objects.count(), 0)


class HomeViewTests(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_contains_cicd_info(self):
        response = self.client.get('/')
        self.assertContains(response, 'CI/CD')
        self.assertContains(response, 'Server Information')

    def test_home_page_contains_api_endpoints(self):
        response = self.client.get('/')
        self.assertContains(response, '/api/categories/')
        self.assertContains(response, '/api/products/')


class APIRootTests(APITestCase):
    def test_api_root(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Welcome to Django CICD API')
        self.assertIn('categories', response.data['endpoints'])
