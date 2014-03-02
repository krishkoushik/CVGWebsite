from django.db import models

# Create your models here.
class Photo(models.Model):
	title=models.CharField(max_length=100)
	image=models.ImageField(upload_to='media/projects')
	
	def __unicode__(self):
		return self.title
	
	
class Video(models.Model):
	name=models.CharField(max_length=100)
	video=models.URLField()
	
	def __unicode__(self):
		return self.name
	
	

class Project(models.Model):
    title = models.CharField(max_length=100)
    brief = models.CharField(max_length=300)
    detail = models.CharField(max_length=1000)
    main_imag=models.ForeignKey(Photo,related_name='main')
    imag=models.ManyToManyField(Photo,related_name='aux')
    videos=models.ManyToManyField(Video)
    date = models.DateField()

    def __unicode__(self):
        return self.title
	class meta:
		ordering=['date']




