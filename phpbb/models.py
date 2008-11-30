# -*- coding: utf-8 -*-
# This file is part of django-phpbb, integration between Django and phpBB
# Copyright (C) 2007-2008  Maciej Bliziński
# 
# django-phpbb is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# django-phpbb is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with django-phpbb; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor,
# Boston, MA  02110-1301  USA

from django.db import models
from django.contrib.auth.models import User
from django.contrib.phpbb.utils import slugify
from datetime import datetime
from django.core import exceptions
from django.utils.encoding import force_unicode

class PhpbbUser(models.Model):
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=25)
    user_password = models.CharField(max_length=32)
    user_posts = models.IntegerField()
    user_email = models.CharField(max_length=255)
    user_website = models.CharField(max_length=100)
    user_avatar_type = models.IntegerField()
    user_avatar = models.CharField(max_length=250)
    user_regdate_int = models.IntegerField(db_column="user_regdate")
    user_lastvisit_int = models.IntegerField(db_column="user_regdate")
    user_sig_bbcode_uid = models.CharField(max_length=8)
    user_sig_bbcode_bitfield = models.CharField(max_length=255)
    def __unicode__(self):
        return self.username
    def user_regdate(self):
        return datetime.fromtimestamp(self.user_regdate_int)
    def user_lastvisit(self):
        return datetime.fromtimestamp(self.user_lastvisit_int)
    class Meta:
        db_table = 'phpbb3_users'
        ordering = ['username']


class DjangoPhpbbUserMapping(models.Model):
    """Maps phpBB users to Django users, 1:1."""
    django_user = models.OneToOneField(User)
    phpbb_user = models.ForeignKey(PhpbbUser, unique=True)


class PhpbbForum(models.Model):
    forum_id = models.IntegerField(primary_key=True)
    forum_name = models.CharField(max_length=60)
    forum_topics = models.IntegerField()
    forum_posts = models.IntegerField()
    forum_last_post = models.ForeignKey(
            'PhpbbPost', db_column='forum_last_post_id')
    forum_desc = models.TextField()
    def __unicode__(self):
        return force_unicode(self.forum_name)
    def get_absolute_url(self):
        return u"/forum/%s/%s/" % (self.forum_id, self.get_slug())
    def get_slug(self):
        return slugify(self.forum_name)
    class Meta:
        db_table = 'phpbb3_forums'
        ordering = ['forum_name']


class PhpbbTopic(models.Model):
    topic_id = models.IntegerField(primary_key=True)
    topic_title = models.CharField(max_length=60)
    topic_replies = models.IntegerField()
    topic_poster = models.ForeignKey(PhpbbUser, db_column='topic_poster')
    topic_time_int = models.IntegerField(db_column='topic_time')
    forum = models.ForeignKey(PhpbbForum)
    topic_last_post = models.ForeignKey('PhpbbPost', related_name='last_in')
    topic_first_post = models.ForeignKey('PhpbbPost', related_name='first_in')
    def get_title(self):
        return self.topic_title
    def __unicode__(self):
        return self.get_title()
    def get_absolute_url(self):
        return "/forum/topics/%s/%s/" % (self.topic_id, self.get_slug())
    def get_slug(self):
        return slugify(self.get_title())
    def topic_time(self):
        return datetime.fromtimestamp(self.topic_time_int)
    class Meta:
        db_table = 'phpbb3_topics'
        ordering = ['-topic_time_int']


class PhpbbPost(models.Model):
    """phpBB3 forum post."""
    PAGINATE_BY = 10
    post_id = models.IntegerField(primary_key=True)
    # post_title = models.CharField(max_length = 60)
    topic = models.ForeignKey(PhpbbTopic)
    poster = models.ForeignKey(PhpbbUser)
    post_time_int = models.IntegerField(db_column='post_time')
    post_text = models.TextField()
    def post_time(self):
        return datetime.fromtimestamp(self.post_time_int)
    def __unicode__(self):
        return force_unicode(u" (post_id=%s)" % self.post_id)
    def get_external_url(self):
        return ("http://www.atopowe-zapalenie.pl/forum/viewtopic.php?p=%s#%s" %
                (self.post_id, self.post_id))
    def get_absolute_url(self):
        return (u"/forum/topics/%s/%s/page%d/" %
                (self.topic.topic_id,
                 self.topic.get_slug(),
                 self.get_page()))
    def get_page(self):
        """TODO: find out, which post in the row it is."""
        return 1
    class Meta:
        db_table = 'phpbb3_posts'
        ordering = ['post_time_int']


class PhpbbAclOption(models.Model):
    auth_option_id = models.IntegerField(primary_key=True)
    is_global = models.IntegerField()
    is_local = models.IntegerField()
    founder_only = models.IntegerField()
    auth_option = models.CharField(max_length=60)
    class Meta:
        db_table = 'phpbb3_acl_options'
        ordering = ['auth_option']


class PhpbbAclRole(models.Model):
    role_id = models.IntegerField(primary_key=True)
    role_name = models.CharField(max_length=255)
    role_order = models.IntegerField()
    class Meta:
        db_table = 'phpbb3_acl_roles'
        ordering = ['role_order']


class PhpbbAclRoleData(models.Model):
    role_id = models.ForeignKey('PhpbbAclRole', db_column='role_id')
    auth_option_id = models.ForeignKey(
        'PhpbbAclOption', db_column='auth_option_id')
    auth_setting = models.IntegerField()
    class Meta:
        db_table = 'phpbb3_acl_roles_data'


class PhpbbConfig(models.Model):
    config_name = models.CharField(max_length=255, primary_key=True)
    config_value = models.CharField(max_length=255)
    is_dynamic = models.IntegerField()
    def __unicode__(self):
        return self.config_name
    class Meta:
        db_table = 'phpbb3_config'
        ordering = ['config_name']
        verbose_name = 'config entry'
        verbose_name_plural = 'config entries'
