from django.contrib import admin
from onlinejudge.models import CodeToCompile
from onlinejudge.models import RequestQueue
from onlinejudge.models import Problem

admin.site.register(CodeToCompile)
admin.site.register(RequestQueue)
admin.site.register(Problem)

