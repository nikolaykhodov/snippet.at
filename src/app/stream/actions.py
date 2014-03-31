# -*- coding: utf8 -*-

from stream.signals import action_signal
from stream.models import Follower
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

def follow(user, obj):
    """ Пользователь начинает следить за действиями объекта obj """

    follower, created = Follower.objects.get_or_create(
        user=user,
        content_type=ContentType.objects.get_for_model(obj),
        object_id=obj.pk
    )

    if created:
        action_signal.send(sender=user, verb=_('started to follow'), obj=obj)

    return follower

def unfollow(user, obj):
    """ Пользователь user перестает следить за измененияи """

    Follower.objects.filter(
        user=user, 
        content_type=ContentType.objects.get_for_model(obj),
        object_id=obj.pk
    ).delete()
    action_signal.send(sender=user, verb=_('stopped following'), obj=obj)
