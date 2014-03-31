# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.conf import settings
from snippet import views
from snippet import models as SnippetModels
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from django.contrib.auth.decorators import login_required
from snippet.views import Snippets, RobotsTxt
import os

sitemaps = {
    'snippets': GenericSitemap({
        'queryset': SnippetModels.Snippet.objects.all(),
        'date_field': 'created',
    }, changefreq='daily')
}

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'$^', Snippets.as_view(), kwargs={'order_by': '-created'}), 

    url(r'^admin/', include(admin.site.urls)),
                       
    url(r'snippet/', include('snippet.snippet_urls')),
    url(r'snippets/', include('snippet.snippets_urls')),

    # Built-in django accounts
    url(r'^accounts/', include('registration.backends.default.urls')),

    # Voting 
    url(r'^vote/', include('vote.urls')),

    # Built-in django comments
    url(r'comments/', include('django.contrib.comments.urls')),

    url(r'profile/', include('profile.urls')),
    # Sitemap
    url(r'sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

    # robots.txt
    url(r'robots\.txt$', RobotsTxt.as_view()),

)

if settings.DEBUG is True:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from debugpages.urls import debugpages_urlpatterns

    # Подключить обработку обычной статики
    urlpatterns += staticfiles_urlpatterns()

    # Подключить обработку верстаемых страниц
    urlpatterns += debugpages_urlpatterns

    # Подключить обработку статики для верстаемых страниц
    urlpatterns = patterns('',
        (r'^%s(?P<path>.*)$' % (settings.DEBUGPAGES_STATIC_URL[1:].replace('/', '\/')), 'django.views.static.serve', {'document_root': settings.DEBUGPAGES_STATICFILE_DIR}),
    )  + urlpatterns
