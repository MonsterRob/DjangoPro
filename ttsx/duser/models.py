from django.db import models


class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    uemail = models.EmailField(max_length=50)

    phone = models.CharField(max_length=11, default='')
    address = models.CharField(max_length=150, default='')
    recipients = models.CharField(max_length=30, default='')


class AreaInfo(models.Model):
    atitle = models.CharField(max_length=30, verbose_name='标题')  # 名称
    aParent = models.ForeignKey('self', null=True, blank=True, verbose_name='父级')  # 父级

    def __str__(self):
        return self.atitle
