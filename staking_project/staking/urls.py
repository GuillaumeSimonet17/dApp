from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('connect-wallet/<str:address>/', views.dashboard_address, name='connect_wallet'),
    path("stake/", views.stake_tokens, name="stake_tokens"),  # Nouvelle route
]
