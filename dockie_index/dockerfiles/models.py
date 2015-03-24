from django.db import models

class Dockerfile(models.Model):
    name = models.CharField(max_length=200)
    uri = models.CharField(max_length=200)
    created = models.DateTimeField('Creation Date')
    updated = models.DateTimeField('Updated Date')
    
    def __unicode__(self):
        return self.name
