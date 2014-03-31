# -*- coding: utf8 -*-
"""
Менеджеры для работы с лентой активности
"""

from lib.gfk import GFKManager
from django.db.models import get_model
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

class FollowerManager(GFKManager):
    """
    Менеджер для Follower
    """

    def filter_obj(self, instance):
        """ """

        content_type = ContentType.objects.get_for_model(instance).pk
        return self.filter(content_type=content_type, object_id=instance.pk)

    def is_following(self, user, instance):
        """ Возвращает True, если пользовател user следит за объектом instance """
        
        if not user or user.is_anonymous():
            return False

        return self.filter_obj(instance).filter(user=user).exists()

    def followers(self, instance):
        """ Возвращает список пользователей, которые следят за instance """
        return [f.user for f in self.filter_obj(instance).prefetch_related('user')]


    def following(self, user):
        """ Возвращает список объектов, за которыми следит пользователь user """
        return [f.follow_object for f in self.filter(user=user).prefetch_related('follow_object')]

class ActionManager(GFKManager):
    """
    Менеджер для Action
    """

    def get_latest(self, quantity=10):
        return self.order_by('-id')[:quantity]

