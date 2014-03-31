# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from vote.views import VoteForSnippet

urlpatterns = patterns('', 
    url(r'for_snippet/(?P<snippet_id>\d+)/(?P<opinion>up|down)/$', login_required(VoteForSnippet.as_view()), name="vote_for_snippet"),
)
