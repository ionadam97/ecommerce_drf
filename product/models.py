from io import BytesIO
from PIL import Image
from django.urls import reverse
from django.core.files import File
from django.db import models
from core.models import TimeStampedModel

def product_directory_path(instance, filename):
    
    return "uploads/products/{0}/{1}/{2}".format(instance.category, instance.title, filename)

class Category(TimeStampedModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return 'http://127.0.0.1:8000' + reverse("category_detail", kwargs={"category_slug": self.slug})


class Product(TimeStampedModel):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to=product_directory_path, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='', null=True, blank=True)
    delivery = models.BooleanField(default=True, null=True, blank=True)
    quantity = models.IntegerField(default=1,null=True, blank=True)
    is_deleted = models.BooleanField(default=False, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)


    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return 'http://127.0.0.1:8000' + reverse("product_detail", kwargs={"category_slug": self.category.slug,"product_slug": self.slug})

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail



