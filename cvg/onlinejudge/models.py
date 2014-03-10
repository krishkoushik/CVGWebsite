from django.db import models
from django import forms
from django.core.files import File
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from formatChecker import RestrictedFileField
class Contest(models.Model):
	name = models.CharField(max_length=100)
	time = models.IntegerField()
	start_time = models.IntegerField()
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
	time_of_submission=models.IntegerField(null=True,blank=True)
	#accepted=models.IntegerField()
	language=models.IntegerField()# 0 means C++ and 1 means C code
	def __init__(self):
		self.language=0
		self.accepted=0

class UploadFileForm(forms.Form):
	fil_e  = RestrictedFileField(max_upload_size=2621440)

class RequestQueue(models.Model):
	codetocompile=models.OneToOneField(CodeToCompile)
