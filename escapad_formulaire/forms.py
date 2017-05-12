#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import logging

from django import forms
from django.utils.translation import ugettext as _

from .models import User
from .models import Cours, Profil


logger = logging.getLogger(__name__)

class CreateNew(forms.Form):
    nom = forms.CharField(max_length=100)

class SearchUser(forms.Form):
    user = forms.CharField(max_length=100)

    def clean_user(self): # check if username dos not exist before
        try:
            User.objects.get(username=self.cleaned_data['user']) #get user from user model
        except User.DoesNotExist :
            raise forms.ValidationError("l'utilisateur n'existe pas!")
            return
        return self.cleaned_data['user']

class MediaForm(forms.Form):
    url_media = forms.CharField(max_length=100)

class UploadForm(forms.Form):
    nom_cours = forms.CharField(max_length=100)
    logo = forms.ImageField(required=False)
    home = forms.FileField()

class ModuleForm(forms.Form):
    module_1 = forms.FileField()
    media_1 = forms.FileField(required=False)

class UploadFormLight(forms.Form):
    archive=forms.FileField()

class UploadFormEth(forms.Form):
    nom_cours = forms.CharField(max_length=100)
    logo = forms.ImageField(required=False)

class ModuleFormEth(forms.Form):
    media_1 = forms.FileField(required=False)

class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

class CreateUserForm(forms.Form):
    username = forms.CharField(max_length=30)
    first_name = forms.CharField()
    last_name = forms.CharField()
    password1=forms.CharField(max_length=30,widget=forms.PasswordInput()) #render_value=False
    password2=forms.CharField(max_length=30,widget=forms.PasswordInput())
    email=forms.EmailField(required=False)
    #title = forms.ChoiceField(choices=["blabla","bbb"])

    def clean_username(self): # check if username dos not exist before
        try:
            User.objects.get(username=self.cleaned_data['username']) #get user from user model
        except User.DoesNotExist :
            return self.cleaned_data['username']

        raise forms.ValidationError("this user exist already")

    def clean_email(self): # check if username dos not exist before
        try:
            User.objects.get(email=self.cleaned_data['email']) #get user from user model
        except User.DoesNotExist :
            return self.cleaned_data['email']

        raise forms.ValidationError("this email is already associated with an account")



    def clean(self): # check if password 1 and password2 match each other
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:#check if both pass first validation
            if self.cleaned_data['password1'] != self.cleaned_data['password2']: # check if they match each other
                raise forms.ValidationError("passwords dont match each other")

        return self.cleaned_data


    def save(self): # create new user
        print "blablabla"
        new_profil=Profil()
        new_user=User.objects.create_user(self.cleaned_data['username'],
                                  self.cleaned_data['email'],
                                  self.cleaned_data['password1'])
        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_profil.user=new_user;

        new_user.save()
        new_profil.save()

        return new_profil