from imaplib import IMAP4_SSL
import mailparser
import re
import secrets
import string
import time
from .models import *


def mailcheck(request,username,seed_email,seed_password,var1):
    try:
        conn= IMAP4_SSL('imap.gmail.com',993)
        conn.login(seed_email,seed_password)
        conn.list()[1]
        try:
            conn.select("INBOX")
            print("----Testing begins with ===",seed_email,var1)
            typ,srch=conn.search(None,"ALL")
            for num in srch[0].split():
                typ,data= conn.fetch(num,'(RFC822)')
                mail = mailparser.parse_from_bytes(data[0][1])
                b = mail.message_as_string 
                # if any(var1 in word for word in b):
                if var1 in b:
                    print('---Inbox- indentifier Found----')  
                    header = mail.headers
                    sndr_mail = mail.from_
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
                    # check_mdata = AppReport.objects.filter(rcode=rcode,customer_id=username)
                    # print(str(check_mdata))
                    # if len(check_mdata)>0:
                    #     print("----- object already exist with the same Rcode from same username---")
                    # else:
                    #     mdata = AppReport.objects.create(customer_id=username,msgID=msgId,sender_mail=sender_mail,spf_record=spf_record,
                    #                                     dkim_record=dkim_record,DMARC_record=dmarc_record,sender_ip=sender_ip,
                    #                                     rcode=rcode, label=label)
                    d = {"seed_email":seed_email,"label":label,"username":customer_id,"sender email": sender_mail,"Message Id":msgId,
                                                    "sender Ip": sender_ip, "spf":spf_record, 
                                                    "dkim": dkim_record, "dmarc":dmarc_record}
                    print(d,"===inbox blocl")
                    return d
                else:
                    print("====Else Block code-- Inbox search complete, not found====")
                  
                
        except Exception as e:
            print("Could not parse message/Inbox testing done", e)
        try:
            
                    conn.select("[Gmail]/Spam")
                    print("--checking in Spam --Testing begins with ===",seed_email)
                    typ,srch=conn.search(None,"ALL")
                    for num in srch[0].split():
                        typ,data= conn.fetch(num,'(RFC822)')
                        mail = mailparser.parse_from_bytes(data[0][1])
                        b = mail.message_as_string   
                        if var1 in b:
                            print('--Spam-- indentifier Found----')  
                            header = mail.headers
                            sndr_mail = mail.from_
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
                            label = 'Spam'
                            # check_mdata = AppReport.objects.filter(rcode=rcode,customer_id=username)
                            # print(str(check_mdata))
                            # if len(check_mdata)>0:
                            #     print("----- object already exist with the same Rcode from same username---")
                            # else:
                            #     mdata = AppReport.objects.create(customer_id=username,msgID=msgId,sender_mail=sender_mail,spf_record=spf_record,
                            #                                     dkim_record=dkim_record,DMARC_record=dmarc_record,sender_ip=sender_ip,
                            #                                     rcode=rcode, label=label)
                            d = {"seed_email":seed_email,"label":label,"username":customer_id,"sender email": sender_mail,"Message Id":msgId,
                                                            "sender Ip": sender_ip, "spf":spf_record, 
                                                            "dkim": dkim_record, "dmarc":dmarc_record}
                            print(d,"===spam blocl")
                            return d
                        else:
                            print("====Else Block code-- spam search complete, not found====")
        except Exception as e:
            print("Could not parse message", e)
                            
                                       
    except:
        print("+++ mailcheck Function first try block not executed")