from django.db import models
from django import forms
from django.core.files import File
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
class Contest(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name

class CurrentContest(models.Model):
	contest = models.ForeignKey(Contest)
	def __str__(self):
		return self.contest.name

class Problem(models.Model):
	name = models.CharField(max_length=100)
	statement = RichTextField()
	compile_line = models.CharField(max_length=300)
	contest = models.ForeignKey(Contest)
	def __str__(self):
		return self.name

class CodeToCompile(models.Model):
	user = models.ForeignKey(User)
	fil_e = models.CharField(max_length=100)
	compileoutp = models.CharField(max_length=100)
	runtimeoutp = models.CharField(max_length=100)
	compilemessage = models.CharField(max_length = 100)
	runtimemessage = models.CharField(max_length = 100)
	problemid = models.ForeignKey(Problem)
	status = models.CharField(max_length=100)
	processed = models.CharField(max_length=1)

class UploadFileForm(forms.Form):
	fil_e  = forms.FileField()

class RequestQueue(models.Model):
	codetocompile=models.OneToOneField(CodeToCompile)
