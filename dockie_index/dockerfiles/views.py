from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.utils import simplejson
from django.utils import timezone
from django.shortcuts import render
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from dockerfiles.models import Dockerfile
from dockerfiles.utils import save_file

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

@login_required()
def newDockerFile(request):
    template = loader.get_template('dockerfiles/new.html')
    context =  RequestContext(request, {
        'content': "",
    })
    return HttpResponse(template.render(context))

# TODO create json response for asynchronous calls or command line
# client
@login_required()
def createDockerFile(request):
    try:
        uploaded_file = request.FILES['filename']
        save_file(uploaded_file)
        docker_file = Dockerfile(name = request.POST['name'],
            created = timezone.now(), updated = timezone.now(),
            filename = uploaded_file.name, user_id = request.user.id)
        docker_file.save()
    except Exception as e:
        template = loader.get_template('dockerfiles/new.html')
        context =  RequestContext(request, {
            'error': "Error: %s " % (str(e)),
        })
        return HttpResponse(template.render(context))

    uri = reverse('show', args=[docker_file.id])
    return HttpResponseRedirect(uri)
