import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from linuxturkey import settings
from question.models import QuestionModel


class UserModel(AbstractUser):
    email = models.EmailField(verbose_name='E-Posta Adresi', unique=True)
    userAbout = models.TextField(verbose_name='Hakkında', null=True, blank=True)
    profileImage = models.ImageField(verbose_name='Profil Resmi', null=True, blank=True, upload_to='user/',
                                     default='user/NewTux.svg')
    userCountry = models.CharField(verbose_name='Ulke', null=True, blank=True, max_length=200)
    userFacebook = models.CharField(verbose_name='Facebook Adresi', null=True, blank=True, max_length=200)
    userTwitter = models.CharField(verbose_name='Twitter Adresi', null=True, blank=True, max_length=200)
    userLinkedin = models.CharField(verbose_name='Linkedin Adresi', null=True, blank=True, max_length=200)
    userWebsite = models.CharField(verbose_name='Kişisel Sitesi', null=True, blank=True, max_length=200)
    isVerified = models.BooleanField(verbose_name='Onaylanmis Kullanici', default=0)

    def __int__(self):
        return self.id


class UserVerifyModel(models.Model):
    verifyID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    publicKey = models.UUIDField(default=uuid.uuid4)
    privateKey = models.UUIDField(default=uuid.uuid4, editable=False)


class UserLoginHistory(models.Model):
    loginID = models.AutoField(verbose_name='Giris ID', primary_key=True)
    userID = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    loginDate = models.DateTimeField(verbose_name='Giris Tarihi', auto_now_add=True)
    ipAddress = models.GenericIPAddressField(verbose_name='IP Adres', null=True)
    location = models.TextField(verbose_name='Konum', null=True)
    userAgent = models.CharField(verbose_name='User-Agent', max_length=250, null=True)
    browser = models.CharField(verbose_name='Tarayıcı', max_length=250, null=True)
    status = models.BooleanField(verbose_name='Durum', default=False)


class QuestionHistory(models.Model):
    id = models.AutoField(verbose_name='Geçmiş ID', primary_key=True)
    userID = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, null=True, blank=True)
    questionID = models.ForeignKey(QuestionModel, models.CASCADE)
    historyDate = models.DateTimeField(verbose_name='Tarih', auto_now_add=True)
    ipAddress = models.GenericIPAddressField(null=True)


class ForgotPasswordModel(models.Model):
    forgotPassword = models.AutoField(verbose_name='ID', primary_key=True)
    userID = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    publicKey = models.UUIDField(default=uuid.uuid4)
    privateKey = models.UUIDField(default=uuid.uuid4, editable=False)
