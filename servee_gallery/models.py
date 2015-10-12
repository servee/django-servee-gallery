from django.db import models
from django.template.defaultfilters import slugify
from servee_gallery.settings import DEFAULT_STORAGE, IMAGE_UPLOAD_TO
import datetime

class BaseGallery(models.Model):
    """
    BaseGallery
    """
    title = models.CharField(max_length=256, blank=True, null=True)
    subtitle = models.CharField(max_length=256, blank=True, null=True)
    client = models.CharField(max_length=256, blank=True, null=True)
    location = models.CharField(max_length=256, blank=True, null=True)
    services = models.CharField(max_length=256, blank=True, null=True)
    feature_image = models.ImageField(upload_to="gallery_imgs", blank=True, null=True, help_text="This image will be resized to 470x420")
    slug = models.SlugField(max_length=128, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(blank=True)
    modified = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        self.modified = datetime.datetime.now()

        if not self.slug:
            self.slug = slugify(self.title)

        if not self.created:
            self.created = datetime.datetime.now()
        super(BaseGallery, self).save(*args, **kwargs) # Call the "real" save() method.

    class Meta:
        abstract = True
        ordering = ["order", "modified"]

    def __unicode__(self):
        if self.title:
            return self.title
        else:
            return u"Gallery #%s" % self.id

class Gallery(BaseGallery):
    """
    Non-Abstract Gallery Model
    """
    pass


class BaseGalleryItem(models.Model):
    """
    BaseGalleryItem
    """
    title = models.CharField(max_length=256, blank=True, null=True)
    gallery = models.ForeignKey(Gallery, related_name="items")
    order = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    uploaded = models.DateTimeField(blank=True)
    modified = models.DateTimeField(blank=True)

    def __unicode__(self):
        return "%s" % self.title

    def save(self, *args, **kwargs):
        self.modified = datetime.datetime.now()

        # update gallery modified time
        self.gallery.modified = datetime.datetime.now()
        self.gallery.save()

        if not self.uploaded:
            self.uploaded = datetime.datetime.now()
        super(BaseGalleryItem, self).save(*args, **kwargs) # Call the "real" save() method.

    def get_absolute_url(self):
        return self.item.url

    class Meta:
        abstract = True
        ordering = ("order", "gallery")

class Image(BaseGalleryItem):
    """
    """
    image = models.ImageField(
        upload_to=IMAGE_UPLOAD_TO,
        storage=DEFAULT_STORAGE(),
        help_text="This image will be resized to 800x600"
    )

    def save(self, *args, **kwargs):
        # create a title if the galleritem has a name
        if not self.title:
            self.title = self.image.name
        super(Image, self).save(*args, **kwargs) # Call the "real" save() method.

    class Meta:
        verbose_name = "servee gallery image"
        verbose_name_plural = "servee gallery images"
        ordering = ["order", "modified"]
