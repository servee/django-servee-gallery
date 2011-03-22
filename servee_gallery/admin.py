from django.contrib import admin
from servee_gallery.models import Gallery, Image

class ImageInline(admin.TabularInline):
    list_display = ("title",)
    model = Image

class GalleryAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [ImageInline,]
    
admin.site.register(Gallery, GalleryAdmin)
