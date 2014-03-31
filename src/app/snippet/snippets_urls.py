# -*- coding: utf8 -*-
"""
URL для /snippets/...
"""

from django.conf.urls.defaults import *
from snippet.views import *

urlpatterns = patterns('',

    # Snippet list
    url(r'^/$', Snippets.as_view(), name='snippets_dir', kwargs={'order_by': '-created'}),
    url(r'^fresh/$', Snippets.as_view(), name='snippets_fresh', kwargs={'order_by': '-created'}),
    url(r'^top/$', Snippets.as_view(), name='snippets_top', kwargs={'order_by': '-score'}),
    url(r'^tag/(?P<tag>[^/]+)/$', Snippets.as_view(), name='snippets_tag', kwargs={'filter_by_tag': True}),
    url(r'^search/$', Snippets.as_view(), name='snippets_search', kwargs={'is_search': True}),

    # List all tags
    url(r'^all_tags/$', Tags.as_view(), name='snippets_alltags'),
)
