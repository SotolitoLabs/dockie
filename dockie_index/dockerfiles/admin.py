from django.contrib import admin
from dockerfiles.models import Dockerfile
from dockerfiles.models import DockerfileResource

admin.site.register(Dockerfile)
admin.site.register(DockerfileResource)
