from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('phone_list', views.phone_list, name='phone_list'),
    path('create_invoice', views.create_invoice, name='create_invoice'),
    path('invoice_list', views.invoice_list, name='invoice_list'),
    path('stock-data/', views.stock_data, name='stock_data'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
]