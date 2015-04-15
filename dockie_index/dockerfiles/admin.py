from django.contrib import admin
from dockerfiles.models import Dockerfile
from dockerfiles.models import DockerfileResource

class DockerfileResourceInline(admin.TabularInline):
    model = DockerfileResource

class DockerfileAdmin(admin.ModelAdmin):
    inlines = (DockerfileResourceInline, ) 

admin.site.register(Dockerfile, DockerfileAdmin)
