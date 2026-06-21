from django.db import models

class CallLog(models.Model):
    phone_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20) # 'Correct' or 'Wrong'
    country = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} - {self.status}"

class MessageLog(models.Model):
    target_number = models.CharField(max_length=20)
    message_payload = models.TextField()
    status = models.CharField(max_length=20) # 'Correct' or 'Wrong'
    country = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.target_number} - {self.status}"