from ast import Delete
from datetime import datetime
from email.policy import default
from enum import unique
from tkinter import CASCADE
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        token = Token.objects.create(user=instance)
        print(token)
        
# class Report(models.Model):
#          timestamp = models.DateTimeField(auto_now_add=True)
#          customer_id = models.ForeignKey(User, on_delete = models.CASCADE)
#          data = JSONField()
     
        
class AppReport(models.Model):
    customer_id = models.ForeignKey(User, on_delete = models.CASCADE)
    msgID = models.CharField(max_length = 50)
    sender_mail = models.CharField(max_length=50)
    spf_record = models.CharField(max_length= 10, default='Pass')
    dkim_record = models.CharField(max_length= 10, default='Pass')
    DMARC_record = models.CharField(max_length= 10, default='Pass')
    sender_ip = models.CharField(max_length=20)
    record_time = models.DateTimeField(default=datetime.now())
    rcode = models.CharField(max_length=20)
    label = models.CharField(max_length = 20,default ='Inbox')
    
    
    # def __str__(self):
    #      return self.label

class Rdmstr(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    created_on = models.DateTimeField(auto_now_add = True)
    Rcode = models.CharField(max_length= 20)
    # email = models.TextField(max_length=3000,default='nothing')
    
    
    def __str__(self):
        return self.Rcode

    
    