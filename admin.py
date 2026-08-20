from django.contrib import admin
from .models import CallLog, MessageLog

@admin.register(CallLog)
class CallLogAdmin(admin.ModelAdmin): 
    list_display = ('phone_number', 'status', 'country', 'timestamp')

@admin.register(MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
    list_display = ('target_number', 'status', 'country', 'timestamp')