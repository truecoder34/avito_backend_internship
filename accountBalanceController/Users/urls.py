from Users.views import CustomUserCreate, ObtainTokenPairWithPhoneView
from django.urls import path
from rest_framework_simplejwt import views as jwt_views


# urlpatterns = [
#     path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),  # override sjwt stock token
#     path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),  
# ]

urlpatterns = [
    path('user/create/',    CustomUserCreate.as_view(),     name="create_user"),
    path('token/obtain/',   ObtainTokenPairWithPhoneView.as_view(),  name='token_create'),
    path('token/refresh/',  jwt_views.TokenRefreshView.as_view(),   name='token_refresh'),
]