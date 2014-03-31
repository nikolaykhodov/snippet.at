# -*- coding: utf8 -*-
"""
Тесты для системы голосования
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.db import IntegrityError
from vote.models import SnippetVote
from snippet.models import Snippet


class VotingTest(TestCase):
    """ """

    def setUp(self):
        self.u1 = User.objects.create(username='u1')
        self.u2 = User.objects.create(username='u2')
        self.u3 = User.objects.create(username='u3')
        self.u4 = User.objects.create(username='u4')

        self.snippet1 = Snippet.objects.create(author=self.u1)
        self.snippet2 = Snippet.objects.create(author=self.u1)

    def test_voting(self):

        self.assertEqual(SnippetVote.objects.vote(self.snippet1, self.u1, +1), +1)
        self.assertEqual(SnippetVote.objects.vote(self.snippet1, self.u3, +1), +2)
        self.assertEqual(SnippetVote.objects.vote(self.snippet1, self.u4, -1), +1)

        self.assertEqual(SnippetVote.objects.vote(self.snippet2, self.u2, -1), -1)
        self.assertEqual(SnippetVote.objects.vote(self.snippet2, self.u3, -1), -2)
        self.assertEqual(SnippetVote.objects.vote(self.snippet2, self.u4, +1), -1)

class AfterVotingTest(TestCase):
    """ """

    def setUp(self):
        self.u1 = User.objects.create(username='u1')
        self.u2 = User.objects.create(username='u2')
        self.u3 = User.objects.create(username='u3')
        self.u4 = User.objects.create(username='u4')

        self.snippet1 = Snippet.objects.create(author=self.u1)
        self.snippet2 = Snippet.objects.create(author=self.u1)

        SnippetVote.objects.vote(self.snippet1, self.u1, +1)
        SnippetVote.objects.vote(self.snippet1, self.u3, +1)
        SnippetVote.objects.vote(self.snippet1, self.u4, -1)

        SnippetVote.objects.vote(self.snippet2, self.u2, -1)
        SnippetVote.objects.vote(self.snippet2, self.u3, -1)
        SnippetVote.objects.vote(self.snippet2, self.u4, +1)

    def test_after_voting(self):

        self.assertEqual(SnippetVote.objects.is_voted(self.snippet1, self.u1), +1)
        self.assertEqual(SnippetVote.objects.is_voted(self.snippet2, self.u2), -1)

        self.assertEqual(SnippetVote.objects.is_voted(self.snippet1, self.u2), None)
        self.assertEqual(SnippetVote.objects.is_voted(self.snippet2, self.u1), None)

        self.assertEqual(Snippet.objects.get(pk=self.snippet1.pk).score, +1)
        self.assertEqual(Snippet.objects.get(pk=self.snippet2.pk).score, -1)

    def test_repeat_voting(self):
        self.assertRaises(IntegrityError, SnippetVote.objects.vote, self.snippet1, self.u1, +1)
        self.assertRaises(IntegrityError, SnippetVote.objects.vote, self.snippet1, self.u1, -1)
