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

# TODO: Implement sitemap caching.

from django.contrib import sitemaps
from models import PhpbbTopic, PhpbbPost, PhpbbForum
from urls import forumqs

class PhpbbForumSitemap(sitemaps.Sitemap):
    def items(self):
        return forumqs
    def lastmod(self, obj):
        try:
            return obj.forum_last_post.post_time()
        except PhpbbPost.DoesNotExist: 
            return None

class PhpbbTopicSitemap(sitemaps.Sitemap):
    # Default limit value is too high; requests retrieving thousands of posts
    # take a long time to execute.
    limit = 500
    def items(self):
        return (PhpbbTopic.
                objects.
                exclude(forum__forum_id=15).
                exclude(forum__forum_id=6))
    def lastmod(self, obj):
        try:
            return obj.topic_last_post.post_time()
        except PhpbbPost.DoesNotExist:
            return None
