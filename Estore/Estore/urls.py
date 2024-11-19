import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls
from products.views import ListProducts
from allauth_customs.views import CustomLogoutView

urlpatterns = [
    path("", ListProducts.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path("accounts/logout/", CustomLogoutView.as_view(), name="account_logout"),
    path('accounts/', include('allauth.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('profile/', include('user_profile.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    if os.getenv('ENVIRONMENT') == 'development':
        urlpatterns += debug_toolbar_urls()
