from django.db import models


class ContacUsModel(models.Model):
    contacID = models.AutoField(verbose_name='Sorun ID', primary_key=True)
    name = models.CharField(verbose_name='Isim', max_length=250)
    email = models.EmailField(verbose_name='E-mail', max_length=250)
    website = models.CharField(verbose_name='Web Site', max_length=250, blank=True)
    message = models.TextField(verbose_name='Mesaj'
                               )
