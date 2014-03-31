# -*- coding: utf8 -*-
"""
Менеджеры для работы с голосованием
"""

from django.db import models
from django.db.models import F

class SnippetVoteManager(models.Manager):
    """
    Менеджер для голосования
    """

    def is_voted(self, snippet, user):
        """ Возвращает значение голоса или None """

        try:
            return self.get(snippet=snippet, who=user).rate
        except:
            return None

    def vote(self, snippet, user, rate):
        """
        Голосует за сниппет и обновляет его рейтинг. Возвращает новое значение рейтинга.
        Параметры:
            -- snippet - 
            -- user - 
            -- rate - целое число (+1 или -1)
        """

        self.create(who=user, snippet=snippet, rate=rate)
        snippet.__class__.objects.filter(pk=snippet.pk).update(score = F('score') + rate)
        snippet.score += rate

        return snippet.score
            
