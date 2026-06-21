from django.contrib import admin
from .models import CallLog, MessageLog

@admin.register(CallLog)
class CallLogAdmin(admin.ModelAdmin):  # <--- admin.site hata kar sirf admin.ModelAdmin kiya hai
    list_display = ('phone_number', 'status', 'country', 'timestamp')

@admin.register(MessageLog)
class MessageLogAdmin(admin.ModelAdmin):  # <--- Yahan bhi sirf admin.ModelAdmin hoga
    list_display = ('target_number', 'status', 'country', 'timestamp')