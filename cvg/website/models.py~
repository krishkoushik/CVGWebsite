from django.db import models

# Create your models here.
class Photo(models.Model):
	title=models.CharField(max_length=100,blank=True)
	image=models.ImageField(upload_to='media/projects')
	
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
    detail = models.CharField(max_length=1000)
    main_imag=models.ForeignKey(Photo,related_name='main')
    imag=models.ManyToManyField(Photo,related_name='aux',blank=True,null=True)
    videos=models.ManyToManyField(Video,blank=True,null=True)
    date = models.DateField()

    def __unicode__(self):
        return self.title
	class meta:
		ordering=['date']




