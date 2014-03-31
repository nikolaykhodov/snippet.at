# -*- coding: utf-8 -*-
from django.forms import Widget
from django.utils.html import mark_safe, force_unicode
from django.forms.util import flatatt
from snippet.models import Tag

class CommaTagsWidget(Widget):
    """
    Виджет для отображения списка тегов сниппета в формате comma separated string
    Взято отсюда: http://stackoverflow.com/questions/4960445/display-a-comma-separated-list-of-manytomany-items-in-a-charfield-on-a-modelform
    """

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, type='text', name=name)
        objects = []
        for each in value:
            try:
                object = Tag.objects.get(pk=each)
            except:
                continue
            objects.append(object)

        values = []
        for each in objects:
            values.append(str(each))
        value = ', '.join(values)
        if value: # only add 'value' if it's nonempty
            final_attrs['value'] = force_unicode(value)
        return mark_safe(u'<input%s />' % flatatt(final_attrs))
