import imaplib
import getpass
import email
from imaplib import IMAP4, IMAP4_SSL
from urllib import request
import mailparser
from rest_framework.status import HTTP_200_OK,HTTP_404_NOT_FOUND
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView, View
from rest_framework.response import Response
from .serializer import UserSerializer,RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import authentication, permissions
from . import mailcheck
from .models import *
import time
import secrets
import string
from django.core.mail import EmailMultiAlternatives




#Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer


#class to get the token information & Login
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        # usr= time_stamp(user.email) # function created to get the current logged in user lastlogin details
        usr =random_string(user.email)
        user = User.objects.get(email=user.email)
        rcode = Rdmstr.objects.create(user_id= user, Rcode= usr)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'unique_code': usr,
            "seed_emails":['logixtest21@gmail.com','logixtest1992@gmail.com']
        })
# def time_stamp(email):
#   usr= User.objects.get(email=email).last_login
#   return usr

def random_string(email):
    N = 7
    res = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
              for i in range(N))
    return res


class appreport(APIView):
    authentication_classes =[authentication.BasicAuthentication]
    permission_classes = [IsAuthenticated] 
    def get(self,request,email=email,format=None):
        start = time.time()
        email = request.data['email']
        username= User.objects.get(email=email)
        tok = Rdmstr.objects.filter(user_id=username).last()
        var1 = str(tok)        
        print(email,"----- Email of customer ------")
        list1=[{'seed': 'logixtest21@gmail.com', 'password': 'slbcotbyuqwchyis'},{'seed':'logixtest1992@gmail.com', 'password': 'bbjzxfvbqpexbvrz'}]
        output = []
        for i in range(len(list1)):
            a = list1[i]
            seed_email = a.get('seed')
            seed_password = a.get('password')
            try:
                data = mailcheck.mailcheck(request,username,seed_email,seed_password,var1)
                output.append(data)
                
            except:
                print("--Couldnot called from views file----") 
                 
        end = time.time()
        print("===execution time===", end-start)
        print(output)
        # check_mdata = AppReport.objects.filter(rcode=rcode,customer_id=username)
        # print(str(check_mdata))
        # if len(check_mdata)>0:
        #     print("----- object already exist with the same Rcode from same username---")
        # else:
        #     mdata = AppReport.objects.create()
        return Response({"success": "Pass", "message": output})

