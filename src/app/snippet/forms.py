# -*- coding: utf-8 -*-
"""
Формы работы со сниппетами
"""

from django import forms
from django.utils.translation import ugettext as _
from snippet.models import Snippet, Tag, TaggedItem
from snippet.widgets import CommaTagsWidget
from django.contrib.auth.models import User

class SnippetForm(forms.ModelForm):
    """
    Класс для формы добавления/редактирования сниппета
    """

    # Comma separated tags
    cs_tags = forms.CharField(required=True, label=_("Tags"))

    class Meta:
        model = Snippet
        fields = ('title', 'description', 'cs_tags', 'body')
        widgets = {
            'body': forms.Textarea()
        }

    def __init__(self, *args, **kwargs):
        """
        Обнуляем массив тегов
        """
        super(SnippetForm, self).__init__(*args, **kwargs)
        self.str_tags = []

        # Задать значение поля со списком тегов при редактировании сниппета
        if 'instance' in kwargs:
            self.fields['cs_tags'].initial = ", ".join([entry['tag'] for entry in kwargs['instance'].tags.values('tag')])

    def clean_cs_tags(self):
        """
        Проверка тегов на валидоность
        """

        tags = [tag.strip() for tag in self.cleaned_data.get('cs_tags', '').split(',') if len(tag) != '']

        if len(tags) < 3:
            raise forms.ValidationError, _("3 tags at least")
        
        if len(tags) > 10:
            raise forms.ValidationError, _("10 tags maximum")

        self.str_tags = tags

        return self.cleaned_data.get('cs_tags')

    def save_tags(self, instance):
        """
        Сохранить теги для сниппета
        """

        instance.tags.clear()
        TaggedItem.objects.bulk_create([
            TaggedItem(tag=Tag.objects.get_or_create(tag=name)[0], snippet=instance)
            for name in self.str_tags
        ])

class AddSnippetForm(SnippetForm):
    """
    """

    def __init__(self, *args, **kwargs):
        """
        Здесь сохраняем в поле author ссылку на пользователя, который будет автором сниппета
        """

        try:
            self.author = kwargs.pop('author')
            if isinstance(self.author, User) is False:
                raise Exception, 'The `author` argument should be django.contrib.auth.models.User instance'
        except KeyError:
            self.author = None

        super(AddSnippetForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        """
        Прописываем автора сниппета и теги
        """

        if self.author is None:
            raise Exception, 'The `author` argument should be passed'

        instance = super(AddSnippetForm, self).save(commit=False)
        instance.author = self.author

        if commit:
            instance.save()
            self.save_tags(instance)

        return instance

class EditSnippetForm(SnippetForm):
    """
    Форма редактирования сниппета
    """
    cs_tags = forms.CharField(required=True, label=_("Tags"))

    def save(self, commit=True):
        """
        Переопределяем теги
        """

        instance = super(EditSnippetForm, self).save(commit=False)
        if commit:
            instance.save()
            self.save_tags(instance)
        return instance
