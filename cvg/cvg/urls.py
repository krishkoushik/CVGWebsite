from django.conf.urls import patterns, include, url

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
    url(r'^contact/$', 'website.views.contact', name='contact'),
    # url(r'^cvg/', include('cvg.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
