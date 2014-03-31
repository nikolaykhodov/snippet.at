# -*- coding: utf8 -*-

from django.test import TestCase
from django.contrib.auth.models import User
import stream.models as models 
import stream.actions as actions
from snippet.models import Snippet, Tag, TaggedItem

class FollowerTest(TestCase):

    def setUp(self):
        self.u1 = User.objects.get_or_create(username='u1')[0]
        self.u2 = User.objects.get_or_create(username='u2')[0]
        self.u3 = User.objects.get_or_create(username='u3')[0]

        self.snippet = Snippet.objects.get_or_create(author=self.u1)[0]
        self.tag1 = Tag.objects.get_or_create(tag='python')[0]
        self.tag2 = Tag.objects.get_or_create(tag='django')[0]
        self.tag3 = Tag.objects.get_or_create(tag='c++')[0]
        TaggedItem.objects.get_or_create(snippet=self.snippet, tag=self.tag1)
        TaggedItem.objects.get_or_create(snippet=self.snippet, tag=self.tag2)
        TaggedItem.objects.get_or_create(snippet=self.snippet, tag=self.tag3)

        actions.follow(self.u1, self.u2)
        actions.follow(self.u1, self.u3)
        
        actions.follow(self.u2, self.u1)

        actions.follow(self.u3, self.u1)
        actions.follow(self.u3, self.u2)


        actions.follow(self.u1, self.tag1)
        actions.follow(self.u2, self.tag2)
        actions.follow(self.u3, self.tag3)

        actions.follow(self.u3, self.snippet)

    def test_u1(self):
        self.assertEqual(models.Follower.objects.is_following(self.u1, self.u2), True)
        self.assertEqual(models.Follower.objects.is_following(self.u1, self.u3), True)
        self.assertEqual(models.Follower.objects.is_following(self.u1, self.tag1), True)

        self.assertEqual(models.Follower.objects.is_following(self.u1, self.tag2), False)
        self.assertEqual(models.Follower.objects.is_following(self.u1, self.tag3), False)

        self.assertEqual(models.Follower.objects.followers(self.u1), [self.u2, self.u3])
        self.assertEqual(models.Follower.objects.following(self.u1), [self.u2, self.u3, self.tag1])

    def test_u2(self):
        self.assertEqual(models.Follower.objects.is_following(self.u2, self.u1), True)
        self.assertEqual(models.Follower.objects.is_following(self.u2, self.tag2), True)

        self.assertEqual(models.Follower.objects.is_following(self.u2, self.u3), False)
        self.assertEqual(models.Follower.objects.is_following(self.u2, self.tag3), False)

        self.assertEqual(models.Follower.objects.followers(self.u2), [self.u1, self.u3])
        self.assertEqual(models.Follower.objects.following(self.u2), [self.u1, self.tag2])

    def test_u3(self):
        self.assertEqual(models.Follower.objects.is_following(self.u3, self.u1), True)
        self.assertEqual(models.Follower.objects.is_following(self.u3, self.u2), True)
        self.assertEqual(models.Follower.objects.is_following(self.u3, self.tag3), True)

        self.assertEqual(models.Follower.objects.is_following(self.u3, self.tag1), False)
        self.assertEqual(models.Follower.objects.is_following(self.u3, self.tag2), False)

        self.assertEqual(models.Follower.objects.followers(self.u3), [self.u1])
        self.assertEqual(models.Follower.objects.following(self.u3), [self.u1, self.u2, self.tag3, self.snippet])

    
    def test_unfollow(self):
        actions.unfollow(self.u1, self.u3)
        actions.unfollow(self.u3, self.tag3)
        actions.unfollow(self.u3, self.snippet)
        actions.unfollow(self.u3, self.u2)

        self.assertEqual(models.Follower.objects.followers(self.u3), [])
        self.assertEqual(models.Follower.objects.following(self.u3), [self.u1])


class ActionTest(TestCase):

    def setUp(self):
        self.u1 = User.objects.get_or_create(username='u1')[0]
        self.u2 = User.objects.get_or_create(username='u2')[0]
        self.u3 = User.objects.get_or_create(username='u3')[0]

        self.snippet = Snippet.objects.get_or_create(author=self.u1, title="Test")[0]
        self.tag1 = Tag.objects.get_or_create(tag='python')[0]
        self.tag2 = Tag.objects.get_or_create(tag='django')[0]
        self.tag3 = Tag.objects.get_or_create(tag='c++')[0]
        TaggedItem.objects.get_or_create(snippet=self.snippet, tag=self.tag1)
        TaggedItem.objects.get_or_create(snippet=self.snippet, tag=self.tag2)
        TaggedItem.objects.get_or_create(snippet=self.snippet, tag=self.tag3)

        actions.follow(self.u1, self.u2)
        actions.follow(self.u1, self.u3)
        
        actions.follow(self.u2, self.u1)

        actions.follow(self.u3, self.u1)
        actions.follow(self.u3, self.u2)


        actions.follow(self.u1, self.tag1)
        actions.follow(self.u2, self.tag2)
        actions.follow(self.u3, self.tag3)

        actions.follow(self.u3, self.snippet)

        actions.unfollow(self.u1, self.u3)
        actions.unfollow(self.u3, self.tag3)
        actions.unfollow(self.u3, self.snippet)
        actions.unfollow(self.u3, self.u2)


    def test_latest(self):
        gauge = [u'u1 started to follow u2',
                 u'u1 started to follow u3',
                 u'u2 started to follow u1',
                 u'u3 started to follow u1',
                 u'u3 started to follow u2',
                 u'u1 started to follow python',
                 u'u2 started to follow django',
                 u'u3 started to follow c++',
                 u'u3 started to follow Test',
                 u'u1 stopped following u3',
                 u'u3 stopped following c++',
                 u'u3 stopped following Test',
                 u'u3 stopped following u2']
                 
        actions = map(lambda x: unicode(x), models.Action.objects.all())
        self.assertEqual(actions, gauge)
