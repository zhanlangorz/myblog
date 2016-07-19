#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   Author  :   cold
#   E-mail  :   rootntsd@gmail.com
#   Date    :   14/10/1 12:21:19
#   Desc    :   
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    url(r'^', include('blog.urls')),
    url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
