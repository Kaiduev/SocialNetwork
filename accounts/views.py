import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterUserSerializer, TokenSerializer
from .utils import Util

User = get_user_model()


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user=user).access_token
        current_site = get_current_site(request=request).domain
        relative_link = reverse('email-verify')
        absolute_url = current_site + relative_link + "?token=" + str(token)
        email_body = 'Hi ' + user.first_name + ' Use link below to verify your email\n' + absolute_url
        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your email'}
        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'message': 'Email successfully activated', 'code': 200}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'message': 'Activation Expired', 'code': 400}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'message': 'Invalid token', 'code': 400}, status=status.HTTP_400_BAD_REQUEST)


class TokenAPIView(TokenObtainPairView):
    serializer_class = TokenSerializer
    permission_classes = (permissions.AllowAny, )
