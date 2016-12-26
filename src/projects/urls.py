from django.conf.urls import include, url
from django.contrib import admin

from .views import (projects_home, project_detail,)

urlpatterns = [
    url(r'^$', projects_home, name='home'),
    url(r'^(?P<slug>[\w-]+)/$', project_detail, name='detail'),
    
    
]
