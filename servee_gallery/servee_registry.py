from django.forms.models import modelform_factory
from django.contrib.admin.util import unquote
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import select_template
from django.shortcuts import render_to_response
from django.utils.functional import update_wrapper
from django.views.decorators.csrf import csrf_exempt

from servee import frontendadmin
from servee.frontendadmin.insert import ModelInsert
from servee.frontendadmin.forms import AddForm
from servee_gallery.models import Gallery, Image
from servee_gallery.admin import GalleryAdmin

class GalleryFrontendAdmin(frontendadmin.ServeeModelAdmin, GalleryAdmin):
    exclude = ("created", "modified", "slug")
    pass

class GalleryInsert(ModelInsert):
    model = Gallery
    
    
    def __init__(self, *args, **kwargs):
        self.item_add_image_template = [
            "servee/wysiwyg/insert/%s/%s/_add_image.html" % (self.model._meta.app_label, self.model._meta.module_name),
            "servee/wysiwyg/insert/%s/_add_image.html" % (self.model._meta.app_label),            
        ]
        
        if kwargs.get("add_image_form", None):
            self.add_image_form = kwargs.pop("add_image_form")
        else:
            self.add_image_form = AddForm
        
        super(GalleryInsert, self).__init__(*args, **kwargs)
    
    
    @csrf_exempt
    def reorder(self, request):
        idents_in_order = request.POST.getlist("itemid")
        for i, ident in enumerate(idents_in_order):
            img = Image.objects.get(pk=ident)
            img.order = i + 1
            img.save()
        return HttpResponse("")
            
    
    @csrf_exempt
    def add_image_view(self, request):
        """
        Uploadify doesn't properly pass the csrf_token.
        """
        instance_form = self.get_add_image_form()
        form = instance_form(request.POST, request.FILES)

        new_instance = None
        if form.is_valid():
            # Don't commit because we have other things to do below.
            new_instance = form.save(commit=False)
            
            # Set the gallery, order, and save
            gallery = Gallery.objects.get(pk=request.POST["gallery_id"])
            new_instance.gallery = gallery
            
            gallery_items = Image.objects.filter(gallery=gallery).order_by("-order").values_list("order", flat=True)
            if gallery_items:
                new_instance.order = gallery_items[0] + 1
            else:
                new_instance.order = 1
            
            new_instance.save()
            
            #render the new display to the page.
            template = select_template(self.item_add_image_template)
            context = RequestContext(request)
            context.update({
                    "insert": self,
                    "form": form,
                    "object": new_instance
                })
            response = HttpResponse(template.render(context))
            response.status_code = 201
            return response
        
        # return the errors
        response = HttpResponse(form.errors)
        response.status_code = 400
        return response

    def get_urls(self):
        """
        Returns urls to get the panel, get/filter list, add/upload, delete and get rendered output.
        """
        from django.conf.urls.defaults import patterns, url
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        return patterns("",
            url(r"^add_minimal_image/$",
                self.add_image_view,
                name="insert_servee_gallery_gallery_image_add"),
            url(r"^reorder/$",
                self.reorder,
                name="insert_servee_gallery_gallery_reorder"),
        ) + super(GalleryInsert, self).get_urls()
    
    
    def get_add_image_form(self):
        exclude_fields = ["order","gallery"]
        
        for field in Image._meta.fields:
            if field.blank:
                exclude_fields.append(field.name)
        
        return modelform_factory(Image, form=self.add_image_form,
            exclude=exclude_fields)
    
    def detail_view(self, request, object_id):
        obj = self.get_object(unquote(object_id))
        
        form = self.get_minimal_add_form()
        
        image_form = self.get_add_image_form()
        
        return render_to_response(self.item_detail_template, {
                "insert": self,
                "object": obj,
                "form": form(),
                "image_form": image_form()
            }, context_instance=RequestContext(request))

frontendadmin.site.register_insert(GalleryInsert)
frontendadmin.site.register(Gallery, GalleryFrontendAdmin)
