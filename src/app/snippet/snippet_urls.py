# -*- coding: utf-8 -*-
"""
URL для /snippet/...
"""
from django.conf.urls.defaults import *
from snippet.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('', 
    # Add a Snippet page
    url(r'^add/$', login_required(AddSnippet.as_view()), name='snippet_add'),

    # Snippet page
    url(r'^(?P<snippet_id>\d+)/$', Snippet.as_view(), name='snippet_page'),
    url(r'^(?P<url_keyword>[a-zA-Z0-9\-_]+)/$', Snippet.as_view(), name='snippet_page'),

    # Edit snippet
    url(r'^(?P<snippet_id>\d+)/edit/$', EditSnippet.as_view(), name='snippet_edit'),

    url(r'^(?P<snippet_id>\d+)/favourite/$', login_required(FavouriteSnippet.as_view()), name='snippet_favourite'),

)
