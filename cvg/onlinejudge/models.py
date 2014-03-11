from django.db import models
from django import forms
from django.core.files import File
from django.contrib.auth.models import User
import subprocess,shlex
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
	arguements = models.CharField(max_length=300)
	time_limit = models.IntegerField()
	mem_limit = models.IntegerField()
	disk_limit = models.IntegerField()
	contest = models.ForeignKey(Contest)
	check_script = models.CharField(max_length=100)
	prob_dir = models.CharField(max_length=100)
	def __unicode__(self):
		return self.name
	def save(self, *args, **kwargs):
		self.prob_dir = "media/problems/"+str(self.id)+"/"
#Creating a Directory for this problem
		subprocess.call(shlex.split("mkdir -p media/problems/"+str(self.id)))
		self.check_script = self.prob_dir+"script.sh"
		super(Problem, self).save(*args, **kwargs)

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
#time_of_submission=models.IntegerField(null=True,blank=True)
	accepted=models.IntegerField(blank=True,null=True)
	language=models.IntegerField(blank=True,null=True)# 0 means C++ and 1 means C code
	"""def create_control_CodeToCompile(sender, usr,prob, created, **kwargs):
		if created:
			a = CodeToCompile()
			a.user = usr
			a.problemid=prob
			a.language=0
			a.accepted=0
	def __init__(self,usr,prob,lan=0,acc=0):
		self.language=lan
		self.accepted=acc
		self.user=usr
		self.problemid=prob"""

class UploadFileForm(forms.Form):
	fil_e  = RestrictedFileField(max_upload_size=2621440)

class RequestQueue(models.Model):
	codetocompile=models.OneToOneField(CodeToCompile)
