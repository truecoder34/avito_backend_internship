from django.urls import path
from WalletController import views


urlpatterns = [
    path('service/', views.ServiceView.as_view(), name='service'),
    path('service/<uuid:pk>', views.ServiceView.as_view(), name='service_details'),
]