# -*- coding: utf8 -*-
from django.views.generic.base import TemplateView
from django.conf import settings
from django.http import Http404

class DebugPageView(TemplateView):
    """
    Класс для отладки верстаемых страниц. Отлаживаемые шаблоны берет из 
    директории DEBUGPAGES_TEMPLATES_DIR, а также подменяет переменную STATIC_URL 
    на DEBUGPAGES_STATIC_URL. Данный режим работает только в отладочном режиме (DEBUG=True)
    """

    def get(self, request, *args, **kwargs):
        """
        Только GET-запросы
        """

        if settings.DEBUG is not True:
            raise Http404

        self.template_name = kwargs.get('page', '')
        return self.render_to_response(self.get_context_data(**kwargs))
