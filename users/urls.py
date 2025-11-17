from django.urls import path, include
from .views import RegisterView, UpdateProfile, UserDetailView, LoginView, UserProfile, LogoutView
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('profile/', UserProfile.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfile.as_view(), name='profile'),
    path('profile/update/', UpdateProfile.as_view(), name='profile-update'),


]
