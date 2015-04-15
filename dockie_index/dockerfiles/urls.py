from django.conf.urls import patterns, include, url
from dockerfiles import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dockie_index.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index),
    url(r'^(\d+)/$', views.showDockerFile),
    url(r'^(\d+)$', views.showDockerFile),
)

