# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from debugpages.views import DebugPageView

debugpages_urlpatterns = patterns('',
    url(r'^debugpages/(?P<page>[a-zA-Z\.\-_0-9/]+)$', DebugPageView.as_view()),
)
