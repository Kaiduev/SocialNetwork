from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import VerifyEmail, RegisterAPIView, TokenAPIView

urlpatterns = [
    path('registration/', RegisterAPIView.as_view(), name='registration'),
    path('token/', TokenAPIView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify')
]
