from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class User(models.Model):
    '''用户表'''
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.email


class Models(models.Model):
    '''模板表'''
    path = models.CharField(max_length=256)
    isPublic = models.BooleanField()
    creatorEmail = models.EmailField()
    useNum = models.IntegerField()

    class Meta:
        ordering = ['creatorEmail']

    def __str__(self):
        return self.path


# 上传图片的模型类
class Pictures(models.Model):
    pic = models.ImageField(upload_to='tmpImages/')
    ip = models.GenericIPAddressField(protocol='ipv4', default='0.0.0.0')
    uploaded_timeStamp = models.CharField(max_length=128, default='0000000000')

    def __str__(self):
        return self.pic
