# -*- coding: utf-8 -*-
"""
URL для /profile/
"""

from django.conf.urls.defaults import *
from profile.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',

    url(r'^(?P<username>[a-zA-Z0-9\-_]{3,30})/$', Profile.as_view(), name='user_profile'),
    url(r'^(?P<username>[a-zA-Z0-9\-_]{3,30})/favourites/$', Favourites.as_view(), name='user_profile_favourites'),
    url(r'^my/$', login_required(MyProfile.as_view()), name='my_profile'),
    url(r'^my/favourites/$', login_required(MyFavourites.as_view()), name='my_profile_favourites'),
)
