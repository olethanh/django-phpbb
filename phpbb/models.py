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
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from phpbb.utils import slugify
from datetime import datetime
from django.core import exceptions
from django.utils.encoding import force_unicode
from django.utils.translation import gettext_lazy as _

class PhpbbUser(models.Model):
    """Model for phpBB user."""
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=25)
    user_password = models.CharField(max_length=32)
    user_posts = models.IntegerField()
    user_email = models.CharField(max_length=255)
    user_website = models.CharField(max_length=100)
    user_avatar_type = models.IntegerField()
    user_avatar = models.CharField(max_length=250)
    user_regdate_int = models.IntegerField(db_column="user_regdate")
    user_lastvisit_int = models.IntegerField(db_column="user_lastvisit")
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
    forum_last_post = models.OneToOneField(
            'PhpbbPost',
            db_column='forum_last_post_id',
            related_name="last_post_of_forum")
    forum_desc = models.TextField()
    parent = models.ForeignKey('self', related_name="child")
    left = models.OneToOneField('self', related_name="right_of")
    right = models.OneToOneField('self', related_name="left_of")
    def __unicode__(self):
        return force_unicode(self.forum_name)
    def __str__(self):
        return str(self.forum_name)
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
    topic_last_post = models.OneToOneField(
            'PhpbbPost',
            related_name='last_post_of_topic')
    topic_first_post = models.OneToOneField(
            'PhpbbPost',
            related_name='first_post_of_topic')
    topic_last_post_time_int = models.IntegerField(
            db_column='topic_last_post_time')
    def get_title(self):
        return self.topic_title
    def topic_last_post_time(self):
        return datetime.fromtimestamp(self.topic_last_post_time_int)
    def __unicode__(self):
        return self.get_title()
    def get_absolute_url(self):
        return "/forum/%s/%s/%s/" % (
        		_("topics"),
        		self.topic_id,
        		self.get_slug())
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
    forum = models.ForeignKey(PhpbbForum)
    poster = models.ForeignKey(PhpbbUser)
    post_time_int = models.IntegerField(db_column='post_time')
    post_text = models.TextField()
    def post_time(self):
        return datetime.fromtimestamp(self.post_time_int)
    def __unicode__(self):
        return force_unicode(u" (post_id=%s)" % self.post_id)
    def get_external_url(self):
        # Example:
        # http://www.atopowe-zapalenie.pl/forum/viewtopic.php?p=80491#p80491
        return ("http://www.atopowe-zapalenie.pl/forum/viewtopic.php?p=%s#p%s"
                % (self.post_id, self.post_id))
    def get_absolute_url(self):
        return (u"/forum/%s/%s/%s/page%d/" %
                (_("topics"),
                 self.topic.topic_id,
                 self.topic.get_slug(),
                 self.get_page()))
    def get_page(self):
        """TODO: find out, which post in the row it is."""
        return 1
    class Meta:
        db_table = 'phpbb3_posts'
        ordering = ['post_time_int']


class PhpbbGroup(models.Model):
    id = models.IntegerField(primary_key=True, db_column='group_id')
    group_type = models.IntegerField()
    group_founder_manage = models.IntegerField()
    group_name = models.CharField(max_length=255)
    group_desc = models.TextField()
    group_desc_bitfield = models.CharField(max_length=255)
    group_desc_options = models.IntegerField()
    def __unicode__(self):
        return u"PhpbbGroup(%s, %s)" % (self.id, self.group_name)
    class Meta:
        db_table = 'phpbb3_groups'
        ordering = ['id']


class PhpbbAclRole(models.Model):
    role_id = models.IntegerField(primary_key=True)
    role_name = models.CharField(max_length=255)
    role_description = models.TextField()
    role_type = models.CharField(max_length=10)
    role_order = models.IntegerField()
    def __unicode__(self):
        return force_unicode(self.role_name)
    class Meta:
        db_table = 'phpbb3_acl_roles'
        ordering = ['role_name']


class PhpbbAclOption(models.Model):
    auth_option_id = models.IntegerField(primary_key=True)
    auth_option = models.CharField(max_length=60)
    is_global = models.IntegerField()
    is_local = models.IntegerField()
    founder_only = models.IntegerField()
    def __unicode__(self):
        return self.auth_option
    class Meta:
        db_table = 'phpbb3_acl_options'
        ordering = ['auth_option_id']


# These classes would need Django to support composite keys. There is a fork of
# Django with a partial implementation:
# http://github.com/dcramer/django-compositepks/tree/master
#
# However, this class is now kept commented out to allow to use django-phpbb
# with the main django branch.
#
## class PhpbbAclRoleDatum(models.Model):
##     role_id = models.ForeignKey(PhpbbAclRole,
##                                 db_column='role_id')
##     auth_option = models.ForeignKey(PhpbbAclOption,
##     		                           db_column='auth_option_id')
##     auth_setting = models.IntegerField()
##     def __unicode__(self):
##         return u"%s, %s => %s" % (self.role_id,
##                                   self.auth_option,
##                                   self.auth_setting)
##     class Meta:
##         primary_key = ('role_id', 'auth_option')
##         db_table = 'phpbb3_acl_roles_data'
##         verbose_name_plural = 'Phpbb acl role data'
##         unique_together = (('role_id', 'auth_option'),)
## 
## 
## class PhpbbAclGroup(models.Model):
##     group = models.ForeignKey(PhpbbGroup, db_column="group_id")
##     forum = models.ForeignKey(PhpbbForum, db_column="forum_id")
##     auth_option = models.ForeignKey(PhpbbAclOption,
##     		                    db_column="auth_option_id")
##     auth_role = models.ForeignKey(PhpbbAclRole,
##     		                  db_column="auth_role_id")
##     auth_setting = models.IntegerField()
##     def __unicode__(self):
##         return ((u"PhpbbAclGroup(%s, %s, %s, %s)")
##                 % (self.forum,
##                    self.group,
##                    self.auth_option,
##                    self.auth_setting))
##     class Meta:
##         primary_key = ('forum', 'group', 'auth_option', 'auth_role')
##         db_table = 'phpbb3_acl_groups'
##         ordering = ['group', 'auth_role']


class PhpbbConfig(models.Model):
    config_name = models.CharField(max_length=255, primary_key=True)
    config_value = models.CharField(max_length=255)
    is_dynamic = models.IntegerField()
    def __unicode__(self):
        return self.config_name
    class Meta:
        db_table = 'phpbb3_config'
        ordering = ['config_name']
        verbose_name = 'Phpbb config entry'
        verbose_name_plural = 'Phpbb config entries'
