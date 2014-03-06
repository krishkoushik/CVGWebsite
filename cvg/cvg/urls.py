from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'website.views.home', name='home'),
    url(r'^about/$', 'website.views.about', name='about'),
    url(r'^projects/$', 'website.views.projects', name='projects'),
    url(r'^resources/$', 'website.views.resources', name='resources'),
    url(r'^blog/$', 'website.views.blog', name='blog'),
    url(r'^blog/blog-post$', 'website.views.blogpost', name='blogpost'),
    url(r'^contact/$', 'website.views.contact', name='contact'),
    url(r'^projects/projectinfo/(?P<project_id>\d+)$', 'website.views.projectinfo', name='projectinfo'),
    
   # url(r'^weblog/', include('zinnia.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
	#url(r'^blog/', include('blog.urls')),  
    
    #Url for online judge portal
    url(r'^onlinejudge/$', 'onlinejudge.views.home', name='onlinejudgehome'),
    url(r'^onlinejudge/login/$', 'onlinejudge.views.login', name='onlinejudgelogin'),
    url(r'^onlinejudge/logout/$', 'onlinejudge.views.logout', name='onlinejudgelogout'),
    url(r'^onlinejudge/editor/$', 'onlinejudge.views.editor', name='editor'),
    url(r'^onlinejudge/editor/submit/$', 'onlinejudge.views.handle_editor', name='handle_editor'),
    url(r'^onlinejudge/challenges/(?P<contest_id>\d+)/$', 'onlinejudge.views.challenges', name='challenges'),
    url(r'^onlinejudge/practice/$', 'onlinejudge.views.practice', name='practice'),
    url(r'^onlinejudge/submissionpage/(?P<problem_id>\d+)/$', 'onlinejudge.views.submissionpage', name='submissionpage'),
    url(r'^onlinejudge/upload_file/(?P<problem_id>\d+)/$', 'onlinejudge.views.upload_file', name='upload_file'),
    url(r'^onlinejudge/viewsubmission/(?P<obid>\d+)/$', 'onlinejudge.views.viewsubmission', name='viewsubmission'),
    url(r'^onlinejudge/contest/(?P<contest_id>\d+)/$', 'onlinejudge.views.contest', name='contest'),

   # url(r'^cvg/', include('cvg.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    
)

#urlpatterns += staticfiles_urlpatterns()
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
