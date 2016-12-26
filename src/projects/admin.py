from django.contrib import admin
from .customfields.imagefields import SVGAndImageFormField

from django import forms
# Register your models here.

from .models import *

class BaseAdmin(admin.ModelAdmin):
    """ Base class for other model admin classes """

    def get_thumbnail(self, obj):
        return mark_safe('<img src="' + obj.get_thumbnail() + '" alt="Thumbnail" width="100px" height="100px"')

    get_thumbnail.short_description = "Thumbnail"


# manytomanys not supported
class WebsiteAdmin(BaseAdmin):
    list_display = ('name', 'url', 'get_thumbnail')


# Model Forms
#
# class ImageModelForm(forms.ModelForm):
#     class Meta:
#         exclude = []
#         field_classes = {
#             'image': SVGAndImageFormField,
#         }


class ImageAdmin(admin.ModelAdmin):
    # form = ImageModelForm
    fields = ('image_preview', 'name', 'image')
    list_display = ('name', 'image_preview',)
    readonly_fields = ('image_preview',)


admin.site.register(Project)
admin.site.register(Skill)
admin.site.register(Image, ImageAdmin)
admin.site.register(Website, WebsiteAdmin)