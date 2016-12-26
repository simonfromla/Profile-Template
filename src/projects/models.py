from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils.safestring import mark_safe
from django.utils.text import slugify


# Create your models here.

def upload_location(instance, filename):
    ImageModel = instance.__class__
    new_id = ImageModel.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object,
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" %(new_id, filename)


#Abstract Base Classes/models are not bound to a DB table. You can use them to abstract common methods/attributes
class BaseModel(object):
    """ Base class for other model classes """

    def get_thumbnail(self, is_project=False, is_website=False):
        """
        Returns the URL to the thumbnail associated with this object.
        """
        if is_project:
            DEFAULT_THUMBNAIL = "python_logo.png"
        elif is_website:
            DEFAULT_THUMBNAIL = "stock_thumb.svg"
        else:
            DEFAULT_THUMBNAIL = "default_thumbnail.png"

        if self.thumbnail:
            return self.thumbnail.get_thumbnail()
        else:
            return settings.STATIC_URL + "images/defaults/" + DEFAULT_THUMBNAIL  # Default thumbnail



class Image(models.Model):
    """ Image model """

    def __str__(self):
        return self.name

    def image_preview(self):
        return mark_safe('<img src="%s" alt="Image" width="100px" height="100px" />' % self.image.url)

    def get_thumbnail(self):
        return self.image.url

    name = models.CharField(max_length=50, help_text='Name of the image.')
    image = models.FileField(help_text='The image.')
    # image = models.ImageField(upload_to=upload_location, help_text='The image.')


class Skill(BaseModel, models.Model):
    name = models.CharField(max_length=50)
    thumbnail = models.ForeignKey(Image, null=True, blank=True, help_text='Thumbnail for the skill.')

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_thumbnail(self):
        return super(Skill, self).get_thumbnail()



class Website(BaseModel, models.Model):
    """ Website model. """

    def __str__(self):
        return self.url

    def get_thumbnail(self):
        return super(Website, self).get_thumbnail(is_website=True)

    name = models.CharField(max_length=50, help_text='Website name.')
    url = models.URLField(help_text='Website url.')
    thumbnail = models.ForeignKey(Image, null=True, blank=True, help_text='Website thumbnail.')


#n number of projects will have ONE image while ONE image can belong to many projects
class Project(BaseModel, models.Model):
    is_project = True

    #These are class level/local variables, compared to a variable if it were under the get_absolute_url function
    # A variable denoted without 'self.', under g_a_u would be a free variable.
    # All instance level vars, 'self.', have access to other vars in this class (regardless of scope?).
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, null=True)
    related_links = models.ManyToManyField(Website, help_text='Github or project site.')
    pull_quote = models.CharField(max_length=200)
    description = models.TextField()
    skills = models.ManyToManyField(Skill, blank=True, help_text='The skills your project is based on.')
    thumbnail = models.ForeignKey(Image, null=True, blank=True, help_text='Thumbnail for the project.')
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("projects:detail", kwargs={"slug": self.slug})

    def get_thumbnail(self):
        return super(Project, self).get_thumbnail(is_project=True)


# def create_slug(instance, new_slug=None):
#     slug = slugify(instance.title)
#     if new_slug is not None:
#         slug = new_slug
#     qs = Project.objects.filter(slug=slug).order_by("-id")
#     exists = qs.exists()
#     if exists:
#         new_slug = "%s-%s" %(slug, qs.first().id)
#         return create_slug(instance, new_slug=new_slug)
#     return slug

#
# def pre_save_project_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = create_slug(instance)
#
# pre_save.connect(pre_save_project_receiver, sender=Project)