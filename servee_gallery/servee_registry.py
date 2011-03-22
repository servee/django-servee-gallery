from servee import frontendadmin
from servee.frontendadmin.insert import ModelInsert
from servee_gallery.models import Gallery
from servee_gallery.admin import GalleryAdmin

class GalleryFrontendAdmin(frontendadmin.ServeeModelAdmin, GalleryAdmin):
    exclude = ("created", "modified", "slug")
    pass

class GalleryInsert(ModelInsert):
    model = Gallery

frontendadmin.site.register_insert(GalleryInsert)
frontendadmin.site.register(Gallery, GalleryFrontendAdmin)
