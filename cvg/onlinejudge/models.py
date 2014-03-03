from django.db import models
from django import forms
from django.core.files import File
from django.contrib.auth.models import User

class Problem(models.Model):
	statement = models.CharField(max_length=2000)
	compile_line = models.CharField(max_length=300)



class CodeToCompile(models.Model):
	user = models.ForeignKey(User)
	fil_e = models.CharField(max_length=100)
	compileoutp = models.CharField(max_length=100)
	runtimeoutp = models.CharField(max_length=100)
	compilemessage = models.CharField(max_length = 100)
	runtimemessage = models.CharField(max_length = 100)
	problemid = models.ForeignKey(Problem)
	status = models.CharField(max_length=100)
	


class UploadFileForm(forms.Form):
	fil_e  = forms.FileField()
