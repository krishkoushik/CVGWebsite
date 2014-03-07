from django.db import models
from cvg import settings
from ckeditor.fields import RichTextField
"""from django.contrib import admin
media = settings.MEDIA_URL
class FooAdmin(admin.ModelAdmin):
	class Media:
		js = ('http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js', media+'/js/wymeditor/jquery.wymeditor.js', media+'/js/editor.js')
# Create your models here."""
class Photo(models.Model):
	title=models.CharField(max_length=100,blank=True)
	image=models.ImageField(upload_to='blog')
	
	def __unicode__(self):
		return self.image.url
	
	
class Video(models.Model):
	name=models.CharField(max_length=100,blank=True)
	video=models.URLField()
	
	def __unicode__(self):
		return self.video
	
	

class Project(models.Model):
    title = models.CharField(max_length=100)
    brief = models.CharField(max_length=300)
    detail = RichTextField()
    main_imag=models.ForeignKey(Photo,related_name='main')
    imag=models.ManyToManyField(Photo,related_name='aux',blank=True,null=True)
    videos=models.ManyToManyField(Video,blank=True,null=True)
    date = models.DateField()

    def __unicode__(self):
        return self.title
	class meta:
		ordering=['date']




