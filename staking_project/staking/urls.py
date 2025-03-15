from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.login_signup, name='login_signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login_signup'), name='logout'),
    # path('dashboard/<str:user_address>/', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('settings/', views.settings, name='settings'),
    path('update-wallet/', views.update_wallet_address, name='update_wallet_address'),

]
