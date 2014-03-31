# -*- coding: utf8 -*-
"""
Менеджер работы со сниппетами
"""

from django.contrib.contenttypes.models import ContentType
from django.db import models

class SnippetManager(models.Manager):
    """
    Менеджер для удобных оберток для выбора сниппетов
    """

    def get_by_request_kwargs(self, **kwargs):
        """
        Обертка поиска сниппета по массиву named groups: ключевому слову (url_keyword) или по номеру (snippet_id)
        """
        return self.get(models.Q(id=kwargs.get('snippet_id', -1)) | models.Q(url_keyword=kwargs.get('url_keyword', None)))

class TagManager(models.Manager):
    """ Менеджер для тегов """

    def with_info(self):
        """ 
        Возврашает список объектов Tag с дополнительными полями 
        followers (количество подписчиков) и snippets (количество сниппетов с этим тегом) 
        """

        tag_contenttype_id = ContentType.objects.get_by_natural_key('snippet', 'tag').pk
        return self.raw("""SELECT snippet_tag.id, snippet_tag.tag, sn.snippets, fl.followers from snippet_tag
                        INNER JOIN (SELECT tag_id, COUNT(*) as snippets FROM snippet_taggeditem GROUP BY tag_id) as sn ON (sn.tag_id = snippet_tag.id)
                        LEFT JOIN (SELECT object_id, COUNT(*) as followers FROM stream_follower  WHERE content_type_id=%(type_id)s GROUP BY object_id) as fl ON (fl.object_id = snippet_tag.id) 
                        ORDER by sn.snippets DESC LIMIT 100""" % dict(type_id=tag_contenttype_id))[0:100]
            

class FavouriteManager(models.Manager):
    """ Менеджер для списка избранного """

    def is_favourited(self, snippet, user):
        """ Возвращает True, если сниппет добавлен в избранное """
        return self.filter(snippet=snippet, user=user).exists()

    def favourite(self, snippet, user):
        """ Добавляе сниппет в список избранного """
        return self.create(snippet=snippet, user=user)

    def unfavourite(self, snippet, user):
        """ Удаляет сниппет из списка избранного """
        self.filter(snippet=snippet, user=user).delete()


