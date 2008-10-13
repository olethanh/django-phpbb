# -*- coding: utf-8 -*-
# This file is part of Atopowe, a Django site with phpBB integration
# Copyright (C) 2007  Maciej Bliziński
# 
# Atopowe is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# Atopowe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Atopowe; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor,
# Boston, MA  02110-1301  USA

from django.db import models
from django.contrib.auth.models import User
from atopowe.portal.utils import slugify
from datetime import datetime
from django.core import exceptions
# from atopowe.phpbb.views import PAGINATE_BY

def repair_latin1_encoding(s):
    try:
        return s.decode('utf-8').encode('latin1').decode('latin2')
    except:
        return s


# Create your models here.
class ForumUser(models.Model):
    user_id = models.IntegerField(primary_key = True)
    username = models.CharField(max_length = 25)
    user_password = models.CharField(max_length = 32)
    user_posts = models.IntegerField()
    user_email = models.CharField(max_length = 255)
    user_website = models.CharField(max_length = 100)
    user_avatar_type = models.IntegerField()
    user_avatar = models.CharField(max_length = 250)
    def get_username(self):
        return repair_latin1_encoding(self.username)
    def __unicode__(self):
        return self.get_username()
    class Meta:
        db_table = 'phpbb3_users'
        ordering = ['username']
    class Admin:
        pass

class DjangoPhpbbUserMapping(models.Model):
    django_user = models.OneToOneField(User)
    phpbb_user = models.ForeignKey(ForumUser,
            unique = True)

class ForumForum(models.Model):
    forum_id = models.IntegerField(primary_key = True)
    forum_name = models.CharField(max_length = 60)
    forum_topics = models.IntegerField()
    forum_posts = models.IntegerField()
    forum_last_post = models.ForeignKey('ForumPost', db_column = 'forum_last_post_id')
    # forum_order = models.IntegerField()
    forum_desc = models.TextField()
    # auth_read = models.SmallIntegerField()
    def __unicode__(self):
        return repair_latin1_encoding(self.forum_name)
        # return self.get_name()
	# return self.forum_name.encode('latin1').decode('latin2')
	# return self.forum_name
	# return "Type: '%s'" % type(self.forum_name)
    def get_absolute_url(self):
        return u"/forum/%s/%s/" % (self.forum_id, self.get_slug())
    def get_slug(self):
        return slugify(self.get_name())
    def get_name(self):
        # raise exceptions.ObjectDoesNotExist
        return repair_latin1_encoding(self.forum_name)
    def get_desc(self):
        return repair_latin1_encoding(self.forum_desc)
    class Meta:
        db_table = 'phpbb3_forums'
        ordering = ['forum_name']
    class Admin:
        pass


class ForumTopic(models.Model):
    topic_id = models.IntegerField(primary_key = True)
    topic_title = models.CharField(max_length = 60)
    topic_replies = models.IntegerField()
    topic_poster = models.ForeignKey(ForumUser, db_column = 'topic_poster')
    topic_time = models.IntegerField()
    forum = models.ForeignKey(ForumForum)
    topic_last_post = models.ForeignKey('ForumPost', related_name = 'last_in')
    topic_first_post = models.ForeignKey('ForumPost', related_name = 'first_in')
    def get_title(self):
        return repair_latin1_encoding(self.topic_title)
    def __unicode__(self):
        return self.get_title()
    def get_absolute_url(self):
        return "/forum/tematy/%s/%s/" % (self.topic_id, self.get_slug())
    def get_slug(self):
        return slugify(self.get_title())
    class Meta:
        db_table = 'phpbb3_topics'
        ordering = ['-topic_time']
        # ordering = ['-topic_last_post_id']
        # order_with_respect_to = 'topic_last_post'
        # ordering = ['-post_time']
    class Admin:
        pass

class ForumPost(models.Model):
    PAGINATE_BY = 10
    post_id = models.IntegerField(primary_key = True)
    # post_title = models.CharField(max_length = 60)
    topic = models.ForeignKey(ForumTopic)
    poster = models.ForeignKey(ForumUser)
    post_time = models.IntegerField()
    post_text = models.TextField()
    def get_time(self):
        return datetime.fromtimestamp(self.post_time)
    def __unicode__(self):
        return unicode(self.post_id)
    def get_external_url(self):
        return "http://www.atopowe-zapalenie.pl/forum/viewtopic.php?p=%s#%s" % (self.post_id, self.post_id)
    def get_absolute_url(self):
        # return self.topic.get_absolute_url()
        return "/forum/tematy/%s/%s/page%d/" % (self.topic.topic_id, self.topic.get_slug(), self.get_page())
    def get_page(self):
        # TODO: find out, which post in the row it is.
        return 1
    # def get_forumtopic_order(self):
    #     return self.post_time

    class Meta:
        db_table = 'phpbb3_posts'
        ordering = ['post_time']
    class Admin:
        pass
    def foo(self):
        return u"foobar"


class ForumAclOption(models.Model):
    auth_option_id = models.IntegerField(primary_key = True)
    is_global = models.IntegerField()
    is_local = models.IntegerField()
    founder_only = models.IntegerField()
    auth_option = models.CharField(max_length = 60)
    class Meta:
        db_table = 'phpbb3_acl_options'
        ordering = ['auth_option']
    class Admin:
        pass

class ForumAclRole(models.Model):
    role_id = models.IntegerField(primary_key = True)
    role_name = models.CharField(max_length = 255)
    role_order = models.IntegerField()
    class Meta:
        db_table = 'phpbb3_acl_roles'
        ordering = ['role_order']
    class Admin:
        pass

class ForumAclRoleData(models.Model):
    role_id = models.ForeignKey('ForumAclRole', db_column = 'role_id')
    auth_option_id = models.ForeignKey('ForumAclOption', db_column = 'auth_option_id')
    auth_setting = models.IntegerField()
    class Meta:
        db_table = ['phpbb3_acl_roles_data']
    class Admin:
        pass

