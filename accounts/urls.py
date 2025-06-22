# accounts/urls.py
from django.urls import path
from .views import RegisterView, LoginView, UserListView, UserProfileView, UserProfileEditHistoryView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('list/', UserListView.as_view(), name='user-list'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('history/', UserProfileEditHistoryView.as_view(), name='user-profile-history'),
]
