from django.contrib import admin
from onlinejudge.models import CodeToCompile
from onlinejudge.models import RequestQueue
from onlinejudge.models import Problem
from onlinejudge.models import Contest
from onlinejudge.models import CurrentContest

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
site.register(models.Problem,
  list_display  = ('statement',),
  search_fields = ['statement',],
  Media = CommonMedia,
)

admin.site.register(CurrentContest)
admin.site.register(CodeToCompile)
admin.site.register(RequestQueue)
#admin.site.register(Problem)
admin.site.register(Contest)
