# from captcha.fields import ReCaptchaField
from django import forms
from .models import *


class ContacUsForm(forms.ModelForm):
    # captcha = ReCaptchaField()

    class Meta:
        model = ContacUsModel
        fields = [
            'name',
            'email',
            'website',
            'message',
        ]


