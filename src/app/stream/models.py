# -*- coding: utf8 -*-
from django.db import models

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from stream.managers import FollowerManager, ActionManager
from django.utils.html import mark_safe, force_unicode
from django.core.urlresolvers import reverse

class Follower(models.Model):
    """
    Класс для слежения за изменениями с различными объектами
    """

    class Meta:
        unique_together = ('user', 'content_type', 'object_id', )

    user = models.ForeignKey(User)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    follow_object = generic.GenericForeignKey('content_type', 'object_id')

    when = models.DateTimeField(auto_now_add=True)

    objects = FollowerManager()


class Action(models.Model):
    """
    Класс действий для ленты событий
    """

    user = models.ForeignKey(User)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    follow_object = generic.GenericForeignKey('content_type', 'object_id')

    verb = models.CharField(max_length=1024)
    when = models.DateTimeField(auto_now_add=True)

    objects = ActionManager()

    def __unicode__(self):
        """ Возвращает текстовое представлене действия """
        
        return u'%(username)s %(verb)s %(obj)s' % {
            'username': self.user.username,
            'verb': self.verb,
            'obj': self.follow_object
        }

    def timesince(self):
        from django.utils.timesince import timesince
        return timesince(self.when)
