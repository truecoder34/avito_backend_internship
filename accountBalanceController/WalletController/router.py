from WalletController.views import ServiceView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'service', ServiceView, basename='services')

urlpatterns = [] + router.urls