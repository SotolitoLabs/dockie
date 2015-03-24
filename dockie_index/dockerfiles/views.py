from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from dockerfiles.models import Dockerfile

def index(request):
    dockerfiles = Dockerfile.objects.all().order_by('updated')[:5]
    template = loader.get_template('dockerfiles/index.html')
    context =  RequestContext(request, {
        'dockerfiles': dockerfiles,
    })
    return HttpResponse(template.render(context))
