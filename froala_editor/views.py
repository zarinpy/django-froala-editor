import json
# from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import default_storage
import os
from django.utils.translation import ugettext_lazy as _


MEDIA_URL = getattr(settings, 'MEDIA_URL', '')


def image_upload(request):
    if 'file' in request.FILES:
        the_file = request.FILES['file']
        allowed_types = ['image/jpeg', 'image/jpg', 'image/pjpeg', 'image/x-png', 'image/png', 'image/gif']
        if not the_file.content_type in allowed_types:
            return HttpResponse(json.dumps({'error': _('You can only upload images.')}),
                                content_type="application/json")
        # Other data on the request.FILES dictionary:
        # filesize = len(file['content'])
        # filetype = file['content-type']
        upload_to = getattr(settings, 'FROALA_UPLOAD_PATH', 'uploads/froala_editor/images/')
        path = default_storage.save(os.path.join(upload_to, the_file.name), the_file)
        host = request.META['HTTP_ORIGIN']
        link = "%s%s%s" % (host, MEDIA_URL, the_file)
        # return JsonResponse({'link': link})
        return HttpResponse(json.dumps({'link': link}), content_type="application/json")


def file_upload(request):
    if 'file' in request.FILES:
        the_file = request.FILES['file']
        upload_to = getattr(settings, 'FROALA_UPLOAD_PATH', 'uploads/froala_editor/files/')
        path = default_storage.save(os.path.join(upload_to, the_file.name), the_file)
        host = request.META['HTTP_ORIGIN']
        link = "%s%s%s" % (host, MEDIA_URL, the_file)
        return HttpResponse(json.dumps({'link': link}), content_type="application/json")
