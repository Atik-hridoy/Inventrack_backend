from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
  # if you have a home view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),  # ✅ Make sure this is added
    
]