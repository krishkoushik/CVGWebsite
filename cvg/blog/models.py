from django.db import models
from django.template.defaultfilters import slugify

from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
# Create your models here.
"""class Photo(models.Model):
	title=models.CharField(max_length=100,blank=True)
	image=models.ImageField(upload_to='blog', null=True)
	
	def __unicode__(self):
		return self.image.url"""

class Post(models.Model):
    title = models.CharField(max_length=100)
    #image=models.ForeignKey(Photo,blank=True,null=True)
    slug = models.SlugField(unique=True)
    text = RichTextField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    #comments =models.ManyToManyField(Comment,blank=True,null=True)
    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('blog_post_detail', (), 
                {
                    'slug' :self.slug,
                })

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

class Comment(models.Model):
    name = models.CharField(max_length=42)
    email = models.EmailField(max_length=75)
    website = models.URLField(max_length=200, null=True, blank=True)
    text = models.TextField()
    post = models.ForeignKey(Post)
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.text
