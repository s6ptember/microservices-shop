from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('refresh/', views.refresh_token, name='refresh'),
]
