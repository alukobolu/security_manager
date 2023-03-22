from django.db.models.query_utils import Q
from django.shortcuts import render, get_object_or_404,redirect
import random

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


from . import serializers
from .models import Account,SocialLogin,UserOtp

#For authentication
from django.contrib.auth import authenticate,logout

#For gmail login
from django.contrib.auth.decorators import login_required

#For email verification
from rest_framework.decorators import api_view, permission_classes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail import send_mail


def create_otp(email):
    otp = random.randint(1000, 9999)

    if UserOtp.objects.filter(email=email).exists():
        UserOtp.objects.get(email=email).delete()

    user_otp = UserOtp(email=email, code=otp)
    user_otp.save()
    return user_otp.code


def verify_otp(email, otp):
    if UserOtp.objects.filter(email=email).exists():
        user_otp = UserOtp.objects.get(email=email)
        if str(otp) == str(user_otp.code):
            user_otp.delete()
            return True
        else:
            return False
    else:
        return False

#The send email function
def send_email(request, account, mail_subject,message): 
    send_mail(
        mail_subject,
        message,
        'noreply@bauss.com',
        [account.email],
        fail_silently=False,
    )
    

class check_user(APIView):
    def get(self,request,user):
        data ={}
        try:
            if Account.objects.filter(email=user).exists() == True:
                account = Account.objects.get(email=user)
                result = True
                data["fullname"]     = account.fullname
                data['profile_image']  = str(account.profile_image.url)
            else:
                result = False
            data["result"]     = result
        except:
            data["Error"]     = "Sorry something when wrong"
        return Response(data=data)

# Create your views here.
class user_view(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = {}
        user =  get_object_or_404(Account, email=request.user.email)
        serializer = serializers.AccountSerializer(user)
        data = serializer.data
        data['email_verified'] = user.email_verified
        data['profile_image'] = data['profile_image']
        # if user.plan != None:
        #     data['plan'] = user.plan.space_size
        #     data['plan_desc'] = user.plan.desc
        #     data['amount'] = user.plan.amount
        # else:
        #     data['plan'] = None
        #     data['plan_desc'] = None
        #     data['amount'] = None
        return Response(data, status=status.HTTP_200_OK)

     #for Updating user 
    def put(self, request):
        data = {}
        user =  get_object_or_404(Account, email=request.user.email)

        serializer = serializers.AccountSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            data['email_verified'] = user.email_verified
            # if user.plan != None:
            #     data['plan'] = user.plan.space_size
            #     data['plan_desc'] = user.plan.desc
            #     data['amount'] = user.plan.amount
            # else:
            #     data['plan'] = None
            #     data['plan_desc'] = None
            #     data['amount'] = None
            data['profile_image'] = data['profile_image']
            data['success'] = "Success"

        else:
            data = serializer.errors   
        return Response(data,  status=status.HTTP_200_OK)

#Register users
class register_view(APIView):
    def post(self, request):
        data = {}   #This is all the data that is been passed to the api Eg. Contex variables
        # current_site = get_current_site(request)
        serializer = serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            otp = create_otp(account.email)
            data['success'] = "Successfully registered."
            data['email'] = account.email
        else:
            data = serializer.errors
        return Response(data)

#Login view for validation
class login_view(APIView):
    data = {}  
    def post(self, request):
        credentials = request.data['username']
        password = request.data['password']
        # Check if username or email exist 
        if Account.objects.filter(email=credentials).exists()==True:
            account_cred =  Account.objects.get(email=credentials) 	

        elif Account.objects.filter(username=credentials).exists()==True:
            account_cred =  Account.objects.get(username=credentials) 	

        else:
            account_cred = None
            self.data['error'] = "Username/Email not found"

        # If it does, it means the password doesnt match 
        if account_cred:
            # Check if username and passowrd match
            userAuth = authenticate(username=account_cred, password=password) 

            if userAuth is not None:					 		
                self.data['error'] = False
            else:
                self.data['error'] = "Incorrect password"

        return Response(self.data)

#Login view for validation
class verify_email(APIView):
    data = {}  
    def post(self, request):
        email = request.data['email']
        otp = request.data['otp']
        result = verify_otp(email,otp)
        if result == True:
            request.user.email_verified = True
            request.user.save()
            self.data['success'] = "Successfully Verified email"
        else:
            self.data['error'] = "OTP code is invalid"
        return Response(self.data)

# Login with google 

@api_view(['POST'])
def welcome_email_view(request):
    data = {}
    account =  get_object_or_404(Account, email=request.data['email'])
    if account.email_verified is not True:
        message = f"Hi,{account.fullname} you are welcome, ENJOY "
        send_email(request, account,"Welcome to BAUSS",message)
    else:
        data['verified'] = True
    data['success'] = "Success"
    return Response(data)


@api_view(['POST'])
def setting_password(request):
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']

    if password == confirm_password:
        user = request.user
        user.set_password(password)
        user.save()
        data ={}
        data['success'] = "Successfully set password"
        return Response(data=data)
    else:
        data ={}
        data['error'] = "Passwords do not match"
        return Response(data=data)

