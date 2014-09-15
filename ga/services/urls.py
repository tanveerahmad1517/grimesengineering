from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^(?P<department_id>\d+)/(?P<department_slug>.+)/$', 'ga.services.views.services', name='department'),
)
