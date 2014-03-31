# -*- coding: utf8 -*-

from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from lib.views import RangeListView
from snippet.models import Snippet
from snippet.models import TaggedItem
from snippet.models import Favourite
from django.db.models import Count

class Profile(RangeListView):
    """
    Профиль произвольного пользователя
    """

    template_name = 'profile/profile.html'
    context_object_name = 'snippets'
    paginate_by = 10
    page_range = 5
    tab = "profile"


    def get_queryset(self):
        return Snippet.objects.filter(author=self.user).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)

        # Текущая вкладка
        context["tab"] = self.tab

        # Инфа о пользователе
        context['user_profile'] = self.user

        # 5 наиболее популярных тегов этого пользователя
        context['user_stat'] = [tag['tag__tag'] for tag in TaggedItem.objects.filter(snippet__author=self.user).values('tag__tag').annotate(tcount=Count('tag')).order_by('-tcount')[:5]]

        return context

    def dispatch(self, request, *args, **kwargs):
        """
        Находим пользователя, профиль которого надо показать
        """

        self.user = get_object_or_404(User, username=kwargs.get('username', None))
        return super(Profile, self).dispatch(request, *args, **kwargs)
    
class FavouritesMixin(object):
    """
    Примесь: Избранные сниппеты пользователя
    """

    tab = "favourites"

    def get_queryset(self):
        """ Возвращает QuerySet """
        favs = Favourite.objects.filter(user=self.user).values_list('snippet')
        return Snippet.objects.filter(pk__in=favs).order_by('-id')

class MyProfileMixin(object):
    """
    Примесь: профиль залогиненного пользователя
    """

    template_name = 'profile/my.html'


class Favourites(FavouritesMixin, Profile): 
    """
    Список избранных сниппетов
    """

    pass

class MyProfile(MyProfileMixin, Profile):
    """
    Страница залогиненного пользователя
    """


    def dispatch(self, request, *args, **kwargs):
        """
        Переопредяем пользователя для отображения
        """

        self.user = request.user
        return super(Profile, self).dispatch(request, *args, **kwargs)

class MyFavourites(FavouritesMixin, MyProfile):
    """
    Список избранных постов залогиненного пользователя
    """
    pass
