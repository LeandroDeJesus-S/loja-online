from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path('', views.show_cart, name='show_cart'),
    path('manage/<option_pk>/', views.manage_cart, name='manage'),
]
