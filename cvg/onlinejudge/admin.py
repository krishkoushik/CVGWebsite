from django.contrib import admin
from onlinejudge.models import CodeToCompile
from onlinejudge.models import RequestQueue
from onlinejudge.models import Problem
from onlinejudge.models import Contest
from onlinejudge.models import CurrentContest

admin.site.register(CurrentContest)
admin.site.register(CodeToCompile)
admin.site.register(RequestQueue)
admin.site.register(Problem)
admin.site.register(Contest)
