from django.http import HttpResponse
from django.core import serializers
from django.utils import simplejson
from django.shortcuts import render
from django.template import RequestContext, loader


from dockerfiles.models import Dockerfile

def index(request):
    dockerfiles = Dockerfile.objects.all().order_by('updated')[:5]
    template = loader.get_template('dockerfiles/index.html')
    context =  RequestContext(request, {
        'dockerfiles': dockerfiles,
    })
    return HttpResponse(template.render(context))

def showDockerFile(request, id):
    type = request.META.get('HTTP_ACCEPT').split(',')[0]
    dockerfile = Dockerfile.objects.filter(id = id)
    context = {'dockerfile': dockerfile[0]}
    if type == "text/html":
        return render(request, 'dockerfiles/show.html', context)
    else:
        json_dockerfile = serializers.serialize("json", dockerfile)
        json_dockerfile_resources = serializers.serialize("json",
            dockerfile[0].dockerfileresource_set.all())
        return HttpResponse('{ "dockerfile": %s , { "resources": %s } }' %
            ( json_dockerfile, json_dockerfile_resources ),
            content_type='application/json')
