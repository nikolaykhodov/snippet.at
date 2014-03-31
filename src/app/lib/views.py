# -*- coding: utf8 -*-

"""
Классы view
"""
from django.views.generic.list import ListView

class RangeListView(ListView):
    """
    Класс для view с пагинацией с ссылками не только на следующую и предыдущую страницу, а 
    еще с ссылками в диапозоне [current_page - page_range; current_page + page_range].

    Список страниц передается через массив `pages` в контексте.

    В классе надо задать параметр page_range для задания размера диапозона.
    """

    def get_context_data(self, **kwargs):
        """
        Здесь мы добавляем в контекст информацмю о списке страниц
        """
        
        context = super(RangeListView, self).get_context_data(**kwargs)

        if 'is_paginated' in context:
            # текущая страница
            number = context['page_obj'].number
            # номер последней страницы
            last = context['paginator'].page_range[-1]

            # список страниц
            context['pages'] = [
                n for n in xrange(number - self.page_range, number + self.page_range)
                if n >= 1 and n <= last
            ]

        return context

