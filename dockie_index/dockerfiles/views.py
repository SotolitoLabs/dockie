from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.utils import simplejson
from django.utils import timezone
from django.shortcuts import render
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from docker import Client

from dockerfiles.models import Dockerfile
from dockerfiles.utils import save_file

#TODO add language support

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

def showRegistry(request):
    type = request.META.get('HTTP_ACCEPT').split(',')[0]
    docker = Client(base_url='unix://var/run/docker.sock')
    images = docker.search('imcsk8')
    for image in images:
        print "---- IMAGE: %s " % image
    context = {'images': images }
    if type == "text/html":
        return render(request, 'dockerfiles/images.html', context)
    else:
        json_images = serializers.serialize("json", images)
        return HttpResponse('{ "images": %s , { "resources": %s } }' %
            ( json_images ),
            content_type='application/json')
   
@login_required()
def newDockerFile(request):
    template = loader.get_template('dockerfiles/edit.html')
    context =  RequestContext(request, {
        'title'  : "New",
        'action' : reverse('create'),
    })
    return HttpResponse(template.render(context))

# TODO create json response for asynchronous calls or command line
# client
@login_required()
def createDockerFile(request):
    try:
        dockerfile = Dockerfile(name = request.POST['name'],
            created = timezone.now(), updated = timezone.now(),
            user_id = request.user.id)
        if request.FILES.has_key('filename'):
            uploaded_file = request.FILES['filename']
            save_file(uploaded_file)
            dockerfile.filename = uploaded_file.name
        dockerfile.save()
    except Exception as e:
        template = loader.get_template('dockerfiles/edit.html')
        context =  RequestContext(request, {
            'title'  : "Create",
            'action' : reverse('create'),
            'error'  : "Error: %s " % (str(e)),
        })
        return HttpResponse(template.render(context))

    uri = reverse('show', args=[dockerfile.id])
    return HttpResponseRedirect(uri)

@login_required()
def editDockerFile(request, id):
    dockerfile = Dockerfile.objects.filter(id = id)
    context =  RequestContext(request, {
        'title'     : 'Edit',
        'action'    : reverse('update', args=[dockerfile[0].id]),
        'dockerfile': dockerfile[0],
    })
    template = loader.get_template('dockerfiles/edit.html')
    return HttpResponse(template.render(context))

@login_required()
def updateDockerFile(request, id):
    qs = Dockerfile.objects.filter(id = id)
    dockerfile = qs[0]
    try:
        if request.POST['name']:
            dockerfile.name = request.POST['name']

        if request.FILES.has_key('filename'):
            uploaded_file = request.FILES['filename']
            save_file(uploaded_file)
            dockefile.filename = uploaded_file.name

        if request.POST['name'] or request.FILES['filename']:
            dockerfile.updated = timezone.now()
            dockerfile.save() 
    except Exception as e:
        template = loader.get_template('dockerfiles/edit.html')
        context =  RequestContext(request, {
            'title'      : "Edit",
            'action'     : reverse('update', args=[dockerfile.id]),
            'dockerfile' : dockerfile,
            'error': "Error: %s " % (str(e)),
        })
        return HttpResponse(template.render(context))

    uri = reverse('show', args=[dockerfile.id])
    return HttpResponseRedirect(uri)
