
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken import views
from . import views as v2


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', v2.RegisterUserAPIView.as_view(), name = 'Register'),
    # path('user/', v2.UserDetailAPI.as_view(), name='user_details'),
    path('login/', v2.CustomAuthToken.as_view(), name = 'login_check'),
    path('report/', v2.appreport.as_view(), name = "report"),
    
    
    
]
