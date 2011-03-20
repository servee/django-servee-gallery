from django.db import models
from django.conf import settings
from servee_image.settings import DEFAULT_STORAGE, IMAGE_UPLOAD_TO
import datetime

class BaseImage(models.Model):
    """
    Image model, You may notice that there's no image here,
    That's because you could still use this app, and subclass
    BaseImage, and do something interesting with your own
    Image, like 
    
    """
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    uploaded = models.DateTimeField(blank=True)
    modified = models.DateTimeField(blank=True)

    def __unicode__(self):
        return '%s' % self.title
        
    def save(self, *args, **kwargs):
        self.modified = datetime.datetime.now()
        if not self.title:
            self.title = self.image.name
        if not self.uploaded:
            self.uploaded = datetime.datetime.now()
        super(BaseImage, self).save(*args, **kwargs) # Call the "real" save() method.
        
    def get_absolute_url(self):
        return '%s%s' % (settings.MEDIA_URL, self.image)

    class Meta:
        abstract = True
    
class Image(BaseImage):
    """
    """
    image = models.ImageField(
        upload_to=IMAGE_UPLOAD_TO,
        storage=DEFAULT_STORAGE()
    )
    
    class Meta:        
        verbose_name = "servee image"
        verbose_name_plural = "servee images"
        ordering = ['modified',]