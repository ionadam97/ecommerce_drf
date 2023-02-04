import random
from django.utils.text import slugify
from .models import Product, Category
from django.db.models.signals import pre_save, post_save

def slugify_instance_name(instance, save=False, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():

        rand_int = random.randint(0, 100)
        slug = f"{slug}-{rand_int}"
        return slugify_instance_name(instance, save=save, new_slug=slug)
    instance.slug = slug
    if save:
        instance.save()
    return instance


def slugify_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance_name(instance, save=False)


def slugify_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance_name(instance, save=True)


pre_save.connect(slugify_pre_save, sender=Product)
post_save.connect(slugify_post_save, sender=Product)

pre_save.connect(slugify_pre_save, sender=Category)
post_save.connect(slugify_post_save, sender=Category)