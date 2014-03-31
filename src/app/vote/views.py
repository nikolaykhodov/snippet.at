# -*- coding: utf8 -*-
from django.views.generic.base import View
from vote.models import SnippetVote
from lib.decorators import render_json
from snippet.models import Snippet
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import F
from django.db import IntegrityError

class VoteForSnippet(View):
    """
    Голосование за сниппет
    """

    @render_json(HttpResponse)
    def post(self, request, snippet_id, opinion):
        """
        Обработка запроса на голосование
        """
        snippet = get_object_or_404(Snippet, id=snippet_id)

        try:
            new_score = SnippetVote.objects.vote(snippet, request.user, +1 if opinion == 'up' else -1)
        except IntegrityError:
            return dict(error=dict(message="Already voted", code="already_voted"))

        return dict(answer='ok', new_score=new_score)
