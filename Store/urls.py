"""
URL configuration for ColdStore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='Login.html'), name='Login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('Register', views.Register, name='Register'),
    path('Admin_Setting', views.admin_settings, name='Admin_Setting'),
    path('client_details', views.Details, name='Client Details'),
    path('Client', views.Client, name='Add_Client'),
    path('Inventory', views.Inventory, name='Inventory'),
    path('Inventory_Gate', views.Inventory_Gate, name='Inventory_Gate'),
    path('Store', views.Store, name='Store'),
    path('Setting', views.Setting, name='Setting'),
    path('Staff', views.Staff, name='Staff'),
    path('Chamber', views.Chamber, name='Chamber'),
    path('sidebar/', views.sidebar_view, name='sidebar'),
    path('Recipt', views.Recipts, name='Recipt'),
    

]
