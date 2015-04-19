# General utilities
from django.conf import settings

def save_file(f):
    filename = "%s/%s" % (settings.MEDIA_ROOT, f.name)
    with open(filename, 'wb+') as dest:
        for part in f.chunks():
            dest.write(part)
