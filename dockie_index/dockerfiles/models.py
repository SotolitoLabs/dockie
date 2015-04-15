from django.db import models
from django.contrib.auth.models import User



#TODO create namespaces for dockerfiles in the filesystem
# eg. resources/dockerfile_name/Dockerfile

#TODO check if there's a git file storage for django

class Dockerfile(models.Model):
    user     = models.ForeignKey(User)
    name     = models.CharField(max_length=200)
    uri      = models.CharField(max_length=200)
    created  = models.DateTimeField('Creation Date')
    updated  = models.DateTimeField('Updated Date')
    filename = models.FileField(upload_to='resources/%Y/%m/%d')
    
    def __unicode__(self):
        return self.name

class DockerfileResource(models.Model):

    def get_dockerfile_name(self):
        return self.dockerfile.name + "_" + self.dockerfile.id

    dockerfile = models.ForeignKey(Dockerfile)
    resource   = models.FileField(upload_to='resources/%Y/%m/%d')
