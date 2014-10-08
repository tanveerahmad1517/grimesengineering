from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'ga.about.views.index', name='index'),
    url(r'^our_team/$', 'ga.about.views.team', name='team'),
    url(r'^licenses/$', 'ga.about.views.licenses', name='licenses'),
)
