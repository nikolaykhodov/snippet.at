# -*- coding: utf8 -*-
""" Перехват сигнала "Комменатрий оставлен" и последующее добавление данного события в ленту событий """

from django.contrib.comments.signals import comment_was_posted
from stream.signals import action_signal
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver

@receiver(comment_was_posted)
def comment_posted_handler(sender, **kwargs):
    """ Обработчик """

    user = kwargs.pop('request').user
    comment = kwargs.pop('comment')

    # Найти объект, к которому оставлен комментарий
    ct = ContentType.objects.get_for_id(comment.content_type_id)
    snippet = ct.get_object_for_this_type(pk=comment.content_object.pk)

    action_signal.send(user, verb=_('commented on'), obj=snippet)

