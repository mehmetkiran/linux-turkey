from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = UserModel
        fields = '__all__'


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = UserModel
        fields = '__all__'


class UserLoginForm(forms.Form):
    username_ = forms.CharField(max_length=250, label='Kullanıcı Adı')
    password_ = forms.CharField(max_length=250, label='Parola', widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username_')
        password = self.cleaned_data.get('password_')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Kullanıcı Adı veya parola hatalı')

        return super(UserLoginForm, self).clean()


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=250, label='Kullanıcı Adı')
    email = forms.CharField(max_length=250, label='E-Posta Adresi', widget=forms.EmailInput)
    password = forms.CharField(max_length=250, label='Parola', widget=forms.PasswordInput)
    confirmPassword = forms.CharField(max_length=250, label='Parola Onay', widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = [
            'username',
            'email',
            'password',
            'confirmPassword',
        ]

    def clean_confirmPassword(self):
        password = self.cleaned_data.get('password')
        confirmPassword = self.cleaned_data.get('confirmPassword')
        if password and confirmPassword and password != confirmPassword:
            raise forms.ValidationError('Parolalar eşleşmiyor!')
        return confirmPassword


class UserProfileChangeForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = [
            'email',
            'userCountry',
            'userFacebook',
            'userTwitter',
            'userLinkedin',
            'userWebsite',
            'userAbout',
            'profileImage',
        ]
