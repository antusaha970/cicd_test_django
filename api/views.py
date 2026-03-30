import platform
import sys
import django
from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from .models import Category, Product, Order, OrderItem
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    OrderSerializer,
    OrderCreateSerializer,
    OrderItemSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


@api_view(['GET'])
def api_root(request):
    return Response({
        'message': 'Welcome to Django CICD API',
        'version': '1.0.0',
        'endpoints': {
            'categories': '/api/categories/',
            'products': '/api/products/',
            'orders': '/api/orders/',
            'order_items': '/api/order-items/',
        }
    })


def home(request):
    server_info = {
        'python_version': sys.version,
        'django_version': django.get_version(),
        'platform': platform.platform(),
        'processor': platform.processor(),
        'hostname': platform.node(),
        'server_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

    cicd_info = {
        'title': 'CI/CD Pipeline Overview',
        'description': 'Continuous Integration and Continuous Deployment (CI/CD) is a method to frequently deliver apps to customers by introducing automation into the stages of app development.',
        'stages': [
            {
                'name': 'Source',
                'description': 'Code is committed to a version control repository (e.g., Git)',
                'tools': ['Git', 'GitHub', 'GitLab', 'Bitbucket']
            },
            {
                'name': 'Build',
                'description': 'Code is compiled and packaged into artifacts',
                'tools': ['Docker', 'Maven', 'Gradle', 'npm']
            },
            {
                'name': 'Test',
                'description': 'Automated tests are run to verify code quality',
                'tools': ['Pytest', 'JUnit', 'Selenium', 'Jest']
            },
            {
                'name': 'Deploy',
                'description': 'Application is deployed to staging or production',
                'tools': ['Jenkins', 'GitHub Actions', 'GitLab CI', 'AWS CodePipeline']
            }
        ],
        'benefits': [
            'Faster time to market',
            'Reduced manual errors',
            'Improved collaboration',
            'Early bug detection',
            'Consistent deployment process'
        ]
    }

    context = {
        'server_info': server_info,
        'cicd_info': cicd_info,
        'page_title': 'Django CI/CD Demo'
    }
    return render(request, 'home.html', context)
