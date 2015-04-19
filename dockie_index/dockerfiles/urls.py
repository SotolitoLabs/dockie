from django.conf.urls import patterns, include, url
from dockerfiles import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dockie_index.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='home'),
    url(r'^(\d+)/$', views.showDockerFile, name='show'),
    url(r'^(\d+)$', views.showDockerFile),
    url(r'^new$', views.newDockerFile, name='new'),
    url(r'^create$', views.createDockerFile, name='create'),
    url(r'^edit/(\d+)$', views.editDockerFile, name='edit'),
    url(r'^update/(\d+)$', views.updateDockerFile, name='update'),
)

