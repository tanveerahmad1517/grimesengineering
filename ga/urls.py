from django.conf.urls import patterns, include, url

from django.contrib import admin
from ga.views import Contact
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'ga.views.index', name='index'),
    url(r'^clients$', 'ga.views.clientlist', name='clients'),
    url(r'^contact$', view=Contact.as_view(), name='contact'),

    url(r'^about/', include('ga.about.urls', namespace='about')),

    url(r'^job/', include('ga.jobs.urls', namespace='job')),
    url(r'^services/', include('ga.services.urls', namespace='services')),

    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
