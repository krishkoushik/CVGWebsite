from django.contrib import admin
from models import Post, Comment
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
site.register(models.Post,
  list_display  = ('text',),
  search_fields = ['text',],
  Media = CommonMedia,
)

#admin.site.register(Post)
admin.site.register(Comment)

