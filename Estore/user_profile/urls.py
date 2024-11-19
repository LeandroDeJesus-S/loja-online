from django.urls import path
from . import views

urlpatterns = [
    path('me/', views.Profile.as_view(), name='user_profile'),
    path('edit/', views.EditProfile.as_view(), name='edit_profile'),
    path('disable/', views.DisableProfile.as_view(), name='disable_profile'),
]
