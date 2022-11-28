from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate as authenticate

from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from authen.serializers import UserSerializer, UserLoginSerializer

def check_password_standardized(password):
    if len(password) < 8:
        return False

    count_upper = 0
    count_lower = 0
    count_alpha = 0

    for c in password:
        if c >= 'a' and c <= 'z':
            count_lower += 1
        elif c >= 'A' and c <= 'Z':
            count_upper += 1
        else:
            count_alpha += 1

    if count_upper > 0 and count_lower > 0 and count_alpha > 0:
        return True
    else:
        return False

class CustomIsAdminUser(IsAdminUser):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin)

# Create your views here.
class UserRegister(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            if serializer.validated_data['password'] == request.data['re_password']:
                if check_password_standardized(serializer.validated_data['password']) == True:
                    serializer.validated_data['password'] = make_password(serializer.validated_data['password'])

                    serializer.save()

                    return JsonResponse({
                        'message': 'Create an user successfully!'
                    }, status = status.HTTP_201_CREATED)
                else:
                    return JsonResponse({
                        'message': 'Your password must have length of 8 at least, and mixs with lowercase, uppercase and number/special characters'
                    }, status = status.HTTP_200_OK)
            else:
                return JsonResponse({
                    'messeage': 'Password is incorrect!'
                }, status = status.HTTP_200_OK)

        return JsonResponse({
            'message': 'This email already existed!'
        }, status = status.HTTP_200_OK)

class UserLogin(APIView):
    def get(self, request):
        return JsonResponse({
            'full_name': request.user.full_name,
            'is_admin': request.user.is_admin
        }, status = status.HTTP_200_OK)

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )

            if user:
                refresh = TokenObtainPairSerializer.get_token(user)

                return JsonResponse({
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                }, status = status.HTTP_200_OK)

        return JsonResponse({
            'message': 'Wrong email or password!'
        }, status = status.HTTP_401_UNAUTHORIZED)

class UserLogout(APIView):
    # logout by re-create new token
    def get(self, request):
        if request.user != None:
            refresh = TokenObtainPairSerializer.get_token(request.user)

        return JsonResponse({
            'message': 'Logout!' 
        }, status = status.HTTP_200_OK)
    # https://stackoverflow.com/questions/52431850/logout-django-rest-framework-jwt

#@permission_classes([IsAuthenticated])
class TestView(APIView):
    permission_classes = [IsAuthenticated, CustomIsAdminUser]
    #IsAdminUser is customized

    def get(self, request):
        return JsonResponse({
            'message': 'this is a test msg'
        }, status = status.HTTP_200_OK)
