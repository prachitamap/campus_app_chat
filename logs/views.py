import hashlib
import random
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .models import CUser
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from knox.models import AuthToken
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

# Create your views here.

# signup
@api_view(["POST"])
def add_user(request):
    data = request.data
    user_model = get_user_model()

    try:
        if user_model.objects.filter(username = data["username"]).exists():  
            return Response({"message":"username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        if user_model.objects.filter(email = data["email"]).exists(): 
            return Response({"message":"email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = user_model.objects.create(
            username = data["username"],
            first_name = data["first_name"],
            last_name = data["last_name"],
            email = data["email"],
            branch = data["branch"],
            mobile = data["mobile"],
            year = data["year"],
        )
        user.set_password(data["password"])
        user.save()

        subject = "Welcome to Campus-App"
        message = f"Hello {user.first_name},\n\nWelcome to Campus-App, the ultimate destination for campus resale! We are thrilled to have you join our vibrant community of student shoppers.\n\nBrowse, buy, and connect with ease, knowing that exciting adventures and incredible finds await you. So, without any further ado, it's time to dive in and explore all that Campus-App has to offer! \n\nThanks for choosing Campus-App\nBest Regards\nCampus-App\nGoa College of Engineering"
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return Response({"message":"user created"}, status=status.HTTP_201_CREATED)

    except ObjectDoesNotExist:
        return Response({"message":"An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# signin
@api_view(["POST"])
def validate_user(request):
    data = request.data
    user_model = get_user_model()

    try:
        user = user_model.objects.get(username = data["username"])
        serializer = UserSerializer(user)

    except ObjectDoesNotExist:
        return Response({"message":"Invalid username"}, status=status.HTTP_404_NOT_FOUND)

    if user.check_password(data["password"]):
        token = AuthToken.objects.create(user, expiry=timedelta(days=3))[1]
        user.is_active = True
        user.save()
        resp = {
            "user": serializer.data,
            "token": str(token)
        }
        return Response(resp, status=status.HTTP_200_OK)

    return Response({"message":"Invalid password"}, status=status.HTTP_400_BAD_REQUEST)


# deactivating user
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    user.delete()
    return Response({"message":"User deleted successfully"}, status=status.HTTP_200_OK)


# editing user info
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_info(request):
    user = request.user
    serializer = UserSerializer(user, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    return Response({"message":"invalid data"}, status=status.HTTP_404_NOT_FOUND)


# generate otp
@api_view(["POST"])
def generate_otp(request):
    data = request.data
    user_model = get_user_model()

    try:
        user = user_model.objects.get(email = data["email"])

    except ObjectDoesNotExist:
        return Response({"message":"Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    otp = random.randint(100000 , 999999)  # generating a random 6 digit otp
    user.expiry_time = timezone.now() + timedelta(minutes=2)  # Setting the desired validity duration to 2 minutes
    user.secret_key = hashlib.sha256(str(otp).encode()).hexdigest()  # hashing the otp to secret_key
    user.save()

    subject = "Reset Password request"
    message = f"Hello {user.first_name},\n\nWe have received a request to reset your password for your Campus-App account.To proceed with the password reset, please enter the One-Time Password (OTP) provided below.\n\nOTP:{otp}\n\nPlease note that the OTP is valid for 2 minutes from the time of OTP generation.\nIf you did not request this password reset or believe this email was sent to you in error, please ignore it.\n\nThank you for using Campus-App\nBest Regards\nCampus-App\nGoa College of Engineering"
    from_email = settings.EMAIL_HOST_USER
    to_list = [user.email]
    send_mail(subject, message, from_email, to_list, fail_silently=True)

    return Response({"message":"otp generated"}, status=status.HTTP_201_CREATED)


# verify otp
@api_view(["POST"])
def verify_otp(request):
    data = request.data
    user_model = get_user_model()

    try:
        user = user_model.objects.get(email = data["email"])

    except ObjectDoesNotExist:
        return Response({"message":"invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    if user.expiry_time and user.expiry_time < timezone.now():
        return Response({"message":"OTP has expired"}, status=status.HTTP_406_NOT_ACCEPTABLE)

    hashed_otp = hashlib.sha256(str(data["otp"]).encode()).hexdigest()  # hashing the entered otp

    if "otp" in data and user.secret_key == hashed_otp:  # checking if there's any otp in db & then checking secret_key with hashed_otp
        user.save()
        return Response({"message":"OTP verified"}, status=status.HTTP_200_OK)
    else:
        return Response({"message":"Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)


# reset password
@api_view(["POST"])
def reset_password(request):
    data = request.data
    user_model = get_user_model()

    try:
        user = user_model.objects.get(email = data["email"])

    except ObjectDoesNotExist:
        return Response({"message":"Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    password = data["password"]
    user.set_password(password)
    user.save()
    return Response({"message":"password reset successful"}, status=status.HTTP_200_OK)


# generating otp using pyotp TOTP
# @api_view(['POST'])
# def generate_otp(request):
#     data = request.data
#     user_model = get_user_model()
#     try:
#         user = user_model.objects.get(email=data['email'])
#         secret_key = random_base32()
#         user.secret_key = secret_key
#         user.save()
#         otp = TOTP(secret_key).now()
#         print('otp is', otp)
#         return Response({'message':'otp generated'}, status=status.HTTP_200_OK)
#     except ObjectDoesNotExist:
# return Response({'message':'otp generation failed'},
# status=status.HTTP_404_NOT_FOUND)


# verifying using pyotp .verify()
# @api_view(['POST'])
# def verify_otp(request):
#     data = request.data
#     user_model = get_user_model()
#     user = user_model.objects.get(email=data['email'])
#     otp = data['otp']
#     print('provided otp is', otp)
#     secret_key = user.secret_key
#     otp_verified = TOTP(secret_key).verify(otp)
#     print(otp_verified)
#     if otp_verified:
#         return Response({'message': 'OTP verification successful'})
#     else:
#         return Response({'message': 'OTP verification failed'})


# resetting & confirming password
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def reset_password(request):
#     data = request.data
#     user = request.user
#     password = data.get('password')
#     confirm_password = data.get('confirm_password')
#     if password == confirm_password:
#         user.set_password(password)
#         user.save()
#         return Response({'message':'password reset successful'}, status=status.HTTP_200_OK)
#     else:
# return Response({"message":"passwords don't match"},
# status=status.HTTP_404_NOT_FOUND)


# getting a single user
# @api_view(['GET'])
# def get_user(request):
#     data = request.data
#     user_model= get_user_model()
#     try:
#         user= user_model.objects.get(username=data["username"])
#         serializers = UserSerializer(user)
#         resp={
#             "userInfo": serializers.data
#         }
#     except ObjectDoesNotExist:
#         return Response({"message":"user not found"}, status= status.HTTP_404_NOT_FOUND)
#     return Response(resp, status= status.HTTP_302_FOUND)


# updating by deleting previous tokens
# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def update_info(request):
#     user = request.user
#     serializer = UserSerializer(user, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         AuthToken.objects.filter(user=user).delete()
#         return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# list of all users
# def get_user_list(request):
#     users_model = get_user_model().objects.all()
#     serializer = UserSerializer(users_model, many=True)
#     resp = {
#         "listOfUsers": serializer.data
#     }
#     return JsonResponse(resp, status=status.HTTP_200_OK)


# reset password url generator
# @api_view(['POST'])
# def reset_password(request):
#     data = request.data
#     user_model = get_user_model()
#     try:
#         user = user_model.objects.get(email=data['email'])
#         token = AuthToken.objects.create(user, expiry=timedelta(days=1))[1]
#         reset_url = f"http://frontend-url.com/reset-password/?token={token}"
#         subject = "Reset password request"
#         message = f"Hello {user.first_name},\n\nFollowing is your reset password link:\n{reset_url} \n\nRegards\nGoa College of Engineering"
#         from_email = settings.EMAIL_HOST_USER
#         to_list = [user.email]
#         send_mail(subject, message, from_email, to_list, fail_silently=True)
#         return Response({'message': 'Password reset link sent successfully'}, status=status.HTTP_200_OK)
#     except ObjectDoesNotExist:
# return Response({'message':'invalid email'},
# status=status.HTTP_404_NOT_FOUND)


# signup without filters
# @api_view(['POST'])
# def add_user(request):
#     data = request.data
#     user_model= get_user_model()
#     try:
#         user= user_model.objects.get(username=data["username"])
#         return Response({"message":"user already present"}, status= status.HTTP_302_FOUND)
#     except ObjectDoesNotExist:
#         user= user_model.objects.create(username=data["username"], first_name=data["first_name"], last_name=data["last_name"], email=data["email"], branch=data["branch"], mobile=data["mobile"], year=data["year"])
#         user.set_password(data["password"])
#         user.save()
#         subject = "Welcome to Campus-App"
#         message = f"Hello {user.first_name},\n\nWelcome to Campus-App, the ultimate destination for campus resale! We are thrilled to have you join our vibrant community of student shoppers.\n\nBrowse, buy, and connect with ease, knowing that exciting adventures and incredible finds await you. So, without any further ado, it's time to dive in and explore all that Campus-App has to offer! \n\nThanks for choosing Campus-App\n\nBest Regards\nCampus-App\nGoa College of Engineering"
#         from_email = settings.EMAIL_HOST_USER
#         to_list = [user.email]
#         send_mail(subject, message, from_email, to_list, fail_silently=True)
# return Response({"message":"user created"}, status=
# status.HTTP_201_CREATED)
