from django.db import models
from django import forms
from django.core.files import File
from django.contrib.auth.models import User


class CodeToCompile(models.Model):
	user = models.OneToOneField(User)
	fil_e = models.CharField(max_length=100)
	compileoutp = models.CharField(max_length=100)
	runtimeoutp = models.CharField(max_length=100)
	compilemessage = models.CharField(max_length = 100)
	runtimemessage = models.CharField(max_length = 100)
	processed=models.CharField(max_length=1)

class UploadFileForm(forms.Form):
	fil_e  = forms.FileField()


class RequestQueue(models.Model):
	codetocompile=models.OneToOneField(CodeToCompile)
