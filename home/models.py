from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.otp