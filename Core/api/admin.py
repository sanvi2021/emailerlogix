from django.contrib import admin
from .models import AppReport, Rdmstr


# Register your models here.
class ReportAppAdmin(admin.ModelAdmin):
    list_display = ('customer_id','sender_mail','spf_record','dkim_record','DMARC_record')
admin.site.register(AppReport,ReportAppAdmin)

class RdmstrAdmin(admin.ModelAdmin):
    list_display = ('user_id','created_on','Rcode')
admin.site.register(Rdmstr,RdmstrAdmin)

