from django.db import models


class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    uemail = models.EmailField(max_length=50)

    phone = models.CharField(max_length=11, default='')
    address = models.CharField(max_length=150, default='')
    recipients = models.CharField(max_length=30, default='')

