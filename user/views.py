from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .utils import generic_response, validate_field_not_request_body
from .models import UserProfile
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
# Create your views here.   


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        # token['username'] = user.username

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class =  MyTokenObtainPairSerializer


class RegisterAPI(APIView):
    def post(self, request):
        try:
            data = {
                'email': request.data.get('email'),
                'username': request.data.get('username'),
                'password': request.data.get('password'),
                'confirm_password':request.data.get('confirm_password')
            }

            is_error, response = validate_field_not_request_body(data)
            
            if is_error:
                return response

            email = data.get('email')
            password = data.get('password')
            confirm_password = data.get('confirm_password')

            if password != confirm_password:
                # logger.exception('New password and confirm password does not matched!')
                return generic_response(status.HTTP_400_BAD_REQUEST,
                                        'New password and confirm password does not matched!')

            if UserProfile.objects.filter(email=email):
                # logger.exception('Email is already registered!')
                return generic_response(status.HTTP_400_BAD_REQUEST, 'Email is already registered!')

            serializer = RegisterSerializer(data=data)

            if serializer.is_valid():
                serializer.save()

                user_profile = UserProfile.objects.filter(email=email).first()
                user = authenticate(email=email, password=password)

                return generic_response(status.HTTP_201_CREATED, 'Registered successfully.', {
                    'user_id': user.id, 'access_token': jwt_token
                    })
            else:
                return generic_response(status.HTTP_400_BAD_REQUEST, f'Error:{serializer.errors}')

        except Exception as ex:
            print('Error while registering your data: {}'.format(ex))
            return generic_response(status.HTTP_400_BAD_REQUEST,
                                    'Error while registering your data')


class LoginAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            email = data.get('email')
            password = data.get('password')

            user_profile = UserProfile.objects.filter(email=email).first()

            user = authenticate(email=email, password=password)
            if user is None:
                return generic_response(status.HTTP_400_BAD_REQUEST, message='Invalid user!')

            # Use the custom TokenObtainPairSerializer to get the token
            token_serializer = MyTokenObtainPairSerializer(data={
                'email': email,
                'password': password
            })
            if token_serializer.is_valid():
                
                token_data = token_serializer.validated_data
                access_token = token_data['access']
                refresh_token = token_data['refresh']

                return generic_response(status.HTTP_200_OK, data={
                    'user_id': user.id,
                    'access_token': access_token,
                    'refresh_token': refresh_token
                })
            else:
                return generic_response(status.HTTP_400_BAD_REQUEST,
                                        f'Error: {token_serializer.errors}')
        except Exception as ex:
            print(ex)
            return generic_response(status.HTTP_400_BAD_REQUEST,
                                    'Error while logging you in!')

