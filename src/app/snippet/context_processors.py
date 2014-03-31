# -*- coding: utf-8 -*-
"""
Добавляет переменную {{ tag_stat }} в шаблон для вывода статистики на страницах сайта
"""

from snippet.models import TaggedItem
from django.db.models import Count

def tag_stat(request):
    """
    Возвращает глобальную статистику по тегам на сайте
    """

    return {'tag_stat': [tag['tag__tag'] for tag in TaggedItem.objects.values('tag__tag').annotate(tcount=Count('tag')).order_by('-tcount')[:5]]}
