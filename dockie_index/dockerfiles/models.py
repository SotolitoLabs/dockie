from django.db import models

Class Dockerfile(models.Model):
    name = models.CharField(max_length=200)
    uri = models.CharField(max_length=200)
    created = models.DateTimeField('Creation Date')
    updated = models.DateTimeField('Updated Date')

