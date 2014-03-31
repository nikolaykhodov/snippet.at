# -*- coding: utf8 -*-
"""
Модели
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext as _
from snippet.managers import SnippetManager, TagManager, FavouriteManager
import re
import snippet.signals
from django.core.urlresolvers import reverse

class Snippet(models.Model):
    author = models.ForeignKey(User)
    # Время публикации
    created = models.DateTimeField(auto_now_add=True)
    # Название сниппета
    title = models.CharField(max_length=64)
    # Описание сниппета
    description = models.CharField(max_length=128)
    # Тело
    body = models.CharField(max_length=8192)
    # Рейтинг
    score = models.IntegerField(default=0)
    # Количество комментариев
    comments = models.IntegerField(default=0)

    # Теги
    tags = models.ManyToManyField('Tag', through='TaggedItem')

    # Ключевое слово в URL
    url_keyword = models.CharField(max_length=1024, db_index=True, blank=True, default='')
    
    objects = SnippetManager()

    def age(self):
        """
        Возвращает возраст сниппета текстом
        """

        delta = timezone.now() - self.created 
        
        if delta.days > 7:
            return self.created.strftime("%x")
        elif 1 <= delta.days and delta.days <= 7:
            return _(u"%s days ago") % delta.days
        elif delta.seconds >= 7200:
            return _(u"%s hours ago") % (delta.seconds / 3600)
        elif 3600 <= delta.seconds and delta.seconds < 7200:
            return _(u"1 hour ago")
        elif delta.seconds >= 600:
            return _(u"%s minutes ago") % (delta.seconds / 60)
        else:
            return _(u'right now')
    age = property(age)

    def generate_url_keyword(self):
        """
        Возвращает (ключевое слово для URL, True, если запись с таким url_keyword не существует в базе данных).
        """

        # Все НЕлатинские символы и НЕцифры преобразовать в пробелы и разбить на слова через пробелы
        words = [word for word in re.sub(r'[^a-zA-Z0-9]', ' ', self.title).lower().split(' ') if word != '']
        url_keyword = '-'.join(words)

        # Если что-то осталось
        if url_keyword != '':
            # Уникальность ключевого слова
            try:
                Snippet.objects.get(url_keyword=url_keyword)
                return (url_keyword, False)
            except:
                return (url_keyword, True)
        else:
            return (url_keyword, False)
        
    def get_absolute_url(self):
        """
        Возвращает путь к странице сниппета
        """

        return reverse('snippet_page', args=[self.url_keyword if self.url_keyword != '' else self.id])
        
    def save(self, *args, **kwargs):
        """
        Автоматически создает url_keyword (при возможности) при добавлении сниппета
        """

        if self.pk is not None:
            return super(Snippet, self).save(*args, **kwargs)
        # Запись еще не создана
        url_keyword, unique = self.generate_url_keyword()
        
        # Если ключевое слово создано и уникально
        if url_keyword != '' and unique is True:
            self.url_keyword = url_keyword
            super(Snippet, self).save(*args, **kwargs)
        # Если ключевое слово - дубликат
        elif url_keyword != '' and unique is False:
            # Сохранить запись, получить номер записи и добавить его после ключевого слова
            super(Snippet, self).save(*args, **kwargs)
            self.url_keyword = "%s-%s" % (url_keyword, self.id)
            super(Snippet, self).save()
        else:
            # Сохранить без ключевого слова
            super(Snippet, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.title

class Tag(models.Model):
    tag = models.CharField(max_length=64, unique=True, db_index=True)

    objects = TagManager()

    def __unicode__(self):
        return u'%s' % self.tag

    def get_absolute_url(self):
        return reverse('snippets_tag', args=[self.tag])

class TaggedItem(models.Model):

    tag = models.ForeignKey(Tag)
    snippet = models.ForeignKey(Snippet)

class Favourite(models.Model):
    """
    Модель для добавленных в избранное сниппетов
    """

    class Meta:
        unique_together = ('snippet', 'user', )

    snippet = models.ForeignKey(Snippet)
    user = models.ForeignKey(User)

    objects = FavouriteManager()
