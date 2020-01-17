from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(verbose_name='用户名',max_length=15,unique=True)
    password = models.CharField(verbose_name='密码',max_length=32)
    email = models.EmailField()
    phone = models.CharField(verbose_name='手机',max_length=11)
    isactive = models.BooleanField(verbose_name='是否激活',default=False)
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='最后活跃时间',auto_now=True)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return 'id:%s username:%s' % (self.id, self.username)

class Address(models.Model):
    receiver = models.CharField(verbose_name='收件人',max_length=20)
    address = models.CharField(verbose_name='收件地址',max_length=50)
    receiver_phone = models.CharField(verbose_name='收件人电话',max_length=11)
    isdefault = models.BooleanField(verbose_name='是否为默认地址',default=False)
    postcode = models.CharField(verbose_name='邮编',max_length=6)
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    uid = models.ForeignKey(User)

    class Meta:
        db_table = 'address'
