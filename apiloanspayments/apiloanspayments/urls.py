from django.contrib import admin
from django.urls import include, path
from api import views
from rest_framework import routers

urlpatterns = [

    path('admin/', admin.site.urls), # url que permite la administracion django
    path('api/auth/', include('dj_rest_auth.urls')), # URL que permite realizar las acciones de autenticacion
    path('api/registration/', include('dj_rest_auth.registration.urls')), # URL que permite realizar el registro de usuarios
    path('api/v1/customer/', views.CustomerView.as_view()), # URL que permite realizar operaciones de con clientes
    path('api/v1/balance/', views.BalanceView.as_view()), # URL que permite obtener el balance de un cliente especifico
    path('api/v1/loan/', views.LoanView.as_view()), # URL que permite realizar operaciones con los prestamos
    path('api/v1/payment/', views.paymentView.as_view()), # URL que permite realizar operaciones con los pagos.
]