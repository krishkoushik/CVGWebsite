from django.contrib import admin
from models import Project, Photo, Video
# Example how to add rich editor capabilities to your models in admin.
 
from django.contrib.admin import site, ModelAdmin
 
import models
 
# we define our resources to add to admin pages
class CommonMedia:
  js = (
    'https://ajax.googleapis.com/ajax/libs/dojo/1.6.0/dojo/dojo.xd.js',
    '/appmedia/admin/js/editor.js',
  )
  css = {
    'all': ('/appmedia/admin/css/editor.css',),
  }
 
# let's add it to this model
site.register(models.Project,
  list_display  = ('detail',),
  search_fields = ['detail',],
  Media = CommonMedia,
)
 
# ... and so on


#admin.site.register(Project)
admin.site.register(Photo)
admin.site.register(Video)
