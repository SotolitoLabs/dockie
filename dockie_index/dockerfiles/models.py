from django.db import models
from django.contrib.auth.models import User


class Dockerfile(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    uri = models.CharField(max_length=200)
    created = models.DateTimeField('Creation Date')
    updated = models.DateTimeField('Updated Date')
    
    def __unicode__(self):
        return self.name

class DockerfileResource(models.Model):

    def get_dockerfile_id(self):
        return self.dockerfile.id

    dockerfile = models.ForeignKey(Dockerfile)
    resource = models.FileField(upload_to='resources/%Y/%m/%d')
