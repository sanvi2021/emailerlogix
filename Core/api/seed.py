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


def seedmail(email,seed_mail,seed_password):
        start = time.time()
        user=seed_mail
        password=seed_password
        conn = IMAP4_SSL('imap.gmail.com',993)
        username= User.objects.get(email=email)
        tok = Rdmstr.objects.filter(user_id=username).last()
        var1 = str(tok)
        try:
            conn.login(user,password)
        except Exception as e:
            print("Could not login", e)     
        conn.list()[1]   
        try:
            conn.select("INBOX")
            print("--- Testing begins with seed as---", user)
            typ, srch= conn.search(None,"ALL")
            for num in srch[0].split():
                typ, data = conn.fetch(num, '(RFC822)')
                mail = mailparser.parse_from_bytes(data[0][1])
                b = mail.message_as_string
                print(var1,"inbox----")
                if var1 == None:
                    data={"success": "Fail", "message": "The indentifier is missing"}
                else:
                    print(var1,"====inbox=====")
                    if var1 in b:
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
                            mdata = AppReport.objects.create(customer_id=username,msgID=msgId,sender_mail=sender_mail,spf_record=spf_record,dkim_record=dkim_record,DMARC_record=dmarc_record,sender_ip=sender_ip,rcode=rcode, label=label)
                        data= {"code": var1,"seed_email": seed_mail,"label":label,"username":customer_id,"sender email": sender_mail,"Message Id":msgId,"sender Ip": sender_ip, "spf":spf_record, "dkim": dkim_record, "dmarc":dmarc_record}
                        return data
                    else:
                        print("value not matching")
                    try:
                        conn.select("[Gmail]/Spam")
                        print("----- testing in spam block ----")
                        typ, srch= conn.search(None,"ALL")
                        for num in srch[0].split():
                            typ, data = conn.fetch(num, '(RFC822)')
                            mail = mailparser.parse_from_bytes(data[0][1])
                            b = mail.message_as_string
                            print(var1,"-----spam")
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
                                check_mdata = AppReport.objects.filter(rcode=rcode,customer_id=username)
                                print(str(check_mdata))
                                if len(check_mdata)>0:
                                    print("----- object already exist with the same Rcode from same username---")
                                else:
                                    mdata = AppReport.objects.create(customer_id=username,msgID=msgId,sender_mail=sender_mail,spf_record=spf_record,dkim_record=dkim_record,DMARC_record=dmarc_record,sender_ip=sender_ip,rcode=rcode, label=label)
                        
                                data={"seed_email": seed_mail,"Message Id":msgId,"username":customer_id,"label":label,"sender email": sender_mail, "sender Ip" : str(sender_ip),"spf": spf_record, "dkim": dkim_record, "dmarc": dmarc_record}
                                return data
                            else:
                                print("=====value not matching=====")
                    except Exception as e:
                        print("Couldnt Parse Message",e)
        except Exception as e:
            print("Couldnt Parse message:", e)
        end = time.time()
        print("===execution time===", end-start)
        