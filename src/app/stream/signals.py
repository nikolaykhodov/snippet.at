# -*- coding: utf8 -*-
""" Сигналы для ленты активности """

from stream.models import Action
from django.dispatch import receiver
from django.dispatch import Signal
from django.contrib.contenttypes.models import ContentType

action_signal=Signal(providing_args=['user', 'verb', 'obj'])

@receiver(action_signal)
def action_handler(sender, **kwargs):
    """ Создает действие и возвращает его """
    
    user = sender
    verb = kwargs.pop('verb')
    obj = kwargs.pop('obj')

    Action.objects.create(
        user=user,
        content_type=ContentType.objects.get_for_model(obj),
        object_id=obj.pk,
        verb=unicode(verb)
    )
