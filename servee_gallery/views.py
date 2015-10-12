from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from servee_gallery.models import Gallery, Image

def index(request):
    project_list = Gallery.objects.all()

    return render_to_response("gallery/list.html",
        {"project_list": project_list},
        context_instance=RequestContext(request)
    )
