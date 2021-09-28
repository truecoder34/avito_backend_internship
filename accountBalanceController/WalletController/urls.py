from django.urls import path
from WalletController import views


urlpatterns = [
    path('service/', views.ServiceView.as_view(), name='crud_service'),
]