# -*- coding: utf8 -*-
"""
Декораторы
"""

import json

def render_json( response_class=None):
    """
    Декоратор над методами class-based view для прозрачной сериализации 
    объекта в ответ браузеру
    """
    def wrapper(handler):
        """ Основная обертка """
        def handler_wrapper(self, *args, **kwargs):
            """
            Сериализуем объект в ответ класса response_class
            """
            answer = handler(self, *args, **kwargs)

            return response_class(
                json.dumps(answer),
                content_type='application/json'
            )

        return handler_wrapper
    return wrapper
