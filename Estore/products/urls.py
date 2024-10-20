from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ListProducts.as_view(), name='products'),
    path('<slug>/', views.ProductDetail.as_view(), name='product_detail'),
]
