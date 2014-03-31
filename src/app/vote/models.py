# -*- coding: utf8 -*-
from django.db import models
from snippet.models import Snippet
from django.contrib.auth.models import User
from vote.managers import SnippetVoteManager

class SnippetVote(models.Model):

    class Meta:
        unique_together = (("who", "snippet"), )

    who = models.ForeignKey(User)
    snippet = models.ForeignKey(Snippet)
    rate = models.IntegerField(default=+1)
    when = models.DateTimeField(auto_now_add=True)

    objects = SnippetVoteManager()
