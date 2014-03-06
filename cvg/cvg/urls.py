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
    url(r'^contact/$', 'website.views.contact', name='contact'),
    url(r'^projects/projectinfo/(?P<project_id>\d+)$', 'website.views.projectinfo', name='projectinfo'),
    
    #url(r'^weblog/', include('zinnia.urls')),
    #url(r'^comments/', include('django.contrib.comments.urls')),
    #url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
	#url(r'^admin/', include(admin.site.urls)),
	url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
	#url(r'^blog/', include('blog.urls')), 
	
	url(r'^blog/$', 'blog.views.blog', name='blog'),
    url(r'^blog/blogpost/^(?P<slug>[-\w\d]+)/$', 'blog.views.blogpost', name='blogpost'),
    url(r'^blog/blogpost/(?P<slug>[-\w]+)$', 'blog.views.blogpost', name='blogpost'), 
    
    
    #Url for online judge portal
    url(r'^onlinejudge/$', 'onlinejudge.views.home', name='onlinejudgehome'),
    url(r'^onlinejudge/login/$', 'onlinejudge.views.login', name='onlinejudgelogin'),
    url(r'^onlinejudge/logout/$', 'onlinejudge.views.logout', name='onlinejudgelogout'),
    url(r'^onlinejudge/submissionpage/$', 'onlinejudge.views.submissionpage', name='submissionpage'),
    url(r'^onlinejudge/upload_file/$', 'onlinejudge.views.upload_file', name='upload_file'),
    url(r'^onlinejudge/submissionpage/(?P<obid>\d+)/$', 'onlinejudge.views.viewsubmission', name='viewsubmission'),
    # url(r'^cvg/', include('cvg.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    
)

#urlpatterns += staticfiles_urlpatterns()
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
