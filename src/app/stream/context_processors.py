# -*- coding: utf-8 -*-
"""
Добавляет переменные в контекст для глобальной ленты активности
"""

from stream.models import Action

def recent_activity(request):
    """
    Возвращает последние события на сайте
    """

    return {'recent_activity': Action.objects.get_latest().select_related('user', 'follow_object')}
