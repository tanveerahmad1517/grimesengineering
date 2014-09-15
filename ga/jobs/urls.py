from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^(?P<job_id>\d+)/(?P<job_slug>.+)/$', 'ga.jobs.views.detail', name='detail'),
    url(r'^log_download/$', 'ga.jobs.views.log_download', name='log_download'),
)

