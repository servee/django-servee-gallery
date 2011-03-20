from django.contrib import admin
from servee_image.models import Image


class ImageAdmin(admin.ModelAdmin):
    list_display = ('title',)
    
admin.site.register(Image, ImageAdmin)
