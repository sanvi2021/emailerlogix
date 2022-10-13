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
import re
import secrets
import string
import time
from .models import *



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
            'unique_code': usr
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
  permission_classes = [IsAuthenticated] 
  def get(self,request,email=email,format=None):
    start = time.time()
    email = request.data['email']
    print(email,"----- Email of customer ------")
    conn = IMAP4_SSL('imap.gmail.com',993)
    list1=[{'seed': 'logixtest21@gmail.com', 'password': 'slbcotbyuqwchyis'}]
           #{'seed': 'arav24.it@gmail.com','password': 'uiakvpjyhgwoyuqo'},#
           #{'seed':'nishantkumar164@gmail.com', 'password': 'uzstwqeqfyswqthi'}]
    username= User.objects.get(email=email)
    tok = Rdmstr.objects.filter(user_id=username).last()
    var1 = str(tok)
    for i in range(len(list1)):
      a = list1[i]
      user = a.get('seed')
      password = a.get('password')
      try:
        conn.login(user,password)
      except Exception as e:
        print("Could not login", e)
      print("--- checking for user---", user)
      conn.list()[1]
      
         
      try:
          conn.select("INBOX")
          print("--- Testing begins with seed as---", user)
          typ, srch= conn.search(None,"ALL")
          for num in srch[0].split():
              typ, data = conn.fetch(num, '(RFC822)')
              mail = mailparser.parse_from_bytes(data[0][1])
              b = mail.message_as_string
              if var1 in b:
                print('found')
                header = mail.headers
                sndr_mail= mail.from_
                sender_email =sndr_mail[0]
                sender_mail = sender_email[1]
                auth_result = header.get('Authentication-Results')
                sndr_ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', auth_result )
                sender_ip= sndr_ip[0]
                if 'dkim=pass' in auth_result:
                    dkim_record = 'PASS'
                else:
                    dkim_record = 'FAIL'
                if 'spf=pass' in auth_result:
                    spf_record = 'PASS'
                else:
                    spf_record = 'FAIL'
                if 'dmarc=pass' in auth_result:
                    dmarc_record = 'PASS'
                else:
                    dmarc_record = 'FAIL'
                msgId = str(mail.message_id)
                rcode =var1
                customer_id = str(username)
                label = 'Inbox'  
                end = time.time()
                print("===execution time===", end-start)

                check_mdata = AppReport.objects.filter(rcode=rcode,customer_id=username)
                print(str(check_mdata))
                if len(check_mdata)>0:
                    print("----- object already exist with the same Rcode from same username---")
                else:
                    mdata = AppReport.objects.create(customer_id=username,msgID=msgId,sender_mail=sender_mail,spf_record=spf_record,
                                                     dkim_record=dkim_record,DMARC_record=dmarc_record,sender_ip=sender_ip,
                                                     rcode=rcode, label=label)
                return Response ({"success": "Pass", 
                                  "data":{"label":label,"username":customer_id,
                                          "sender email": sender_mail,"Message Id":msgId,
                                          "sender Ip": sender_ip, "spf":spf_record, 
                                          "dkim": dkim_record, "dmarc":dmarc_record
                                          }})
              else:
                pass             
          try:
              conn.select("[Gmail]/Spam")
              print("----- testing in spam block ----")
              typ, srch= conn.search(None,"ALL")
              for num in srch[0].split():
                  typ, data = conn.fetch(num, '(RFC822)')
                  mail = mailparser.parse_from_bytes(data[0][1])
                  b = mail.message_as_string
                  if var1 in b:
                      header = mail.headers
                      sndr_mail= mail.from_
                      sender_email =sndr_mail[0]
                      sender_mail = sender_email[1]
                      auth_result = header.get('Authentication-Results')
                      sndr_ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', auth_result )
                      sender_ip= sndr_ip[0]
                      msgId = mail.message_id
                      rcode =var1
                      customer_id = str(username)
                      label = 'Spam'
                      if 'dkim=pass' in auth_result:
                          dkim_record = 'PASS'
                      else:
                          dkim_record = 'FAIL'
                      if 'spf=pass' in auth_result:
                          spf_record = 'PASS'
                      else:
                          spf_record = 'FAIL'
                      if 'dmarc=pass' in auth_result:
                          dmarc_record = 'PASS'
                      else:
                          dmarc_record = 'FAIL'
                      
                      end = time.time()
                      print("===execution time===", end-start)
                      check_mdata = AppReport.objects.filter(rcode=rcode,customer_id=username)
                      print(str(check_mdata))
                      if len(check_mdata)>0:
                          print("----- object already exist with the same Rcode from same username---")
                      else:
                          mdata = AppReport.objects.create(customer_id=username,msgID=msgId,sender_mail=sender_mail,spf_record=spf_record,
                                                           dkim_record=dkim_record,DMARC_record=dmarc_record,sender_ip=sender_ip,
                                                           rcode=rcode, label=label)
                
                      return Response({
                          "success":"Pass","Message Id":msgId,"username":customer_id,
                          "label":label,"sender email": sender_mail, "sender Ip" : str(sender_ip),
                          "spf": spf_record, "dkim": dkim_record, "dmarc": dmarc_record
                          }) 
                  else:
                      pass  
          except Exception as e:
              print("Couldnt Parse Message",e)
      except Exception as e:
                  print("Couldnt Parse message:", e)
                  pass
    end = time.time()
    print("===execution time===", end-start)
    return Response({"success": "Fail", "message": 'Unique code is not found in the mail body. Please try again'})

   
    