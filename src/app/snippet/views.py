# -*- coding: utf-8 -*-
from snippet.forms import AddSnippetForm, EditSnippetForm
from stream.signals import action_signal
from snippet.models import  Tag
from snippet.models import  Favourite
from snippet import models 
from lib.decorators import render_json
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.base import View
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from lib.views import RangeListView

class Snippets(RangeListView):
    """
    Отображение списка сниппетов
    """

    template_name = 'snippet/index.html'
    context_object_name = 'snippets'
    paginate_by = 10
    page_range = 5

    def get_queryset(self):
        """
        Возвращает Queryset для формирования списка сниппетов
        """

        queryset = models.Snippet.objects.all()
        
        if self.order_by:
            queryset = queryset.order_by(self.order_by)
        
        if self.filter_by_tag:
            tag = get_object_or_404(Tag, tag=self.tag_name)
            queryset = queryset.filter(tags=tag.id)

        if self.is_search:
            queryset = queryset.filter(Q(title__contains=self.search_query) | Q(body=self.search_query))

        return queryset

    def get_context_data(self, **kwargs):
        """
        Добавляет поисковой запрос для отображения на странице, если он был
        """

        context = super(Snippets, self).get_context_data(**kwargs)
        

        if self.search_query is not None:
            context['search_query'] = self.search_query

        if self.search_query:
            context['index_page_title'] = 'Search Results for "%s"' % self.search_query
        elif self.filter_by_tag:
            context['index_page_title'] = '%s snippets' % (self.tag_name)

        return context
    
    def dispatch(self, request, *args, **kwargs):
        """
        Формирует флаги на фильтрации сниппетов
        """

        # Порядок сортировки
        self.order_by = kwargs['order_by'] if 'order_by' in kwargs else None
        
        # Поиск по ключевым словам
        self.is_search = 'is_search' in kwargs
        self.search_query = request.REQUEST.get('query', None)

        # Фильтрация по тегу
        self.filter_by_tag = 'filter_by_tag' in kwargs
        self.tag_name = kwargs['tag'] if 'tag' in kwargs else None

        return super(Snippets, self).dispatch(request, *args, **kwargs)

class AddSnippet(TemplateView):
    """
    Страница добавления сниппета
    """

    template_name = 'snippet/add_snippet.html'

    def get_context_data(self, **kwargs):
        """
        Здесь добавляем форму в контекст
        """

        context = super(AddSnippet, self).get_context_data(**kwargs)
        context['form'] = kwargs['form']

        return context

    def get(self, request):
        """
        GET-запрос
        """

        return self.render_to_response(self.get_context_data(form=AddSnippetForm()))

    def post(self, request):
        """
        POST-запрос и добавление сниппета
        """

        form = AddSnippetForm(self.request.POST, author=self.request.user)
        if form.is_valid():
            # Сохранить сниппет
            form.save()

            # Добавить упоминание в ленту
            action_signal.send(request.user, verb=_("created snippet"), obj=form.instance)

        return self.render_to_response(self.get_context_data(form=form))

class EditSnippet(TemplateView):
    """
    Редактирование сниппета
    """

    template_name = 'snippet/edit_snippet.html'

    def get_context_data(self, **kwargs):
        """
        Добавляем форму для редактирования в контекст
        """

        context = super(EditSnippet, self).get_context_data(**kwargs)
        context['form'] = kwargs['form']

        return context

    def get(self, request, **kwargs):
        """
        Отобразить форму редактирования сниппета
        """
        return self.render_to_response(self.get_context_data(form=EditSnippetForm(instance=self.snippet)))

    def post(self, request, **kwargs):
        """
        Сохранить сниппет
        """
        
        form = EditSnippetForm(request.POST, instance=self.snippet)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.snippet.get_absolute_url())
        return self.render_to_response(self.get_context_data(form=form))

    def dispatch(self, request, *args, **kwargs):
        """
        Разрешать редактирование только автору
        """

        self.snippet = models.Snippet.objects.get_by_request_kwargs(**kwargs)
        if self.snippet.author.pk != request.user.pk:
            raise Http404

        return super(EditSnippet, self).dispatch(request, *args, **kwargs)

class Snippet(TemplateView):
    """
    Страница сниппета
    """

    template_name = 'snippet/snippet.html'

    def get_context_data(self, **kwargs):
        """
        Добавляем в контекст информацию о сниппете
        """

        try:
            snippet = models.Snippet.objects.get_by_request_kwargs(**kwargs)
        except models.Snippet.DoesNotExist, ex:
            raise Http404
        
        context = super(Snippet, self).get_context_data(**kwargs)
        context['snippet'] = snippet

        # Пользователь - автор ?
        if self.request.user.is_authenticated():
            context['user_is_author'] = snippet.author.pk == self.request.user.pk

        # Добавить инфу, добавлен ли сниппет в избранное
        context['is_fav'] = self.request.user.is_authenticated() and Favourite.objects.is_favourited(snippet, self.request.user)

        return context

class Tags(RangeListView):
    """
    Страница всех тегов
    """

    template_name = 'snippet/all_tags.html'
    context_object_name = 'tags'
    paginate_by = 20
    page_range = 5

    def get_queryset(self):
        """ Возвращает Queryset """
        return Tag.objects.with_info()

class RobotsTxt(TemplateView):
    template_name = 'robots.txt'

class FavouriteSnippet(View):
    """
    Добавление/удаление сниппета в избранное
    """

    @render_json(HttpResponse)
    def post(self, request, snippet_id):
        snippet = get_object_or_404(models.Snippet, pk=snippet_id)
        is_fav = Favourite.objects.is_favourited(snippet, request.user)
        
        if is_fav:
            Favourite.objects.unfavourite(snippet, request.user)
        else:
            Favourite.objects.favourite(snippet, request.user)

        return dict(answer='ok', is_fav=not is_fav)

    get = post

