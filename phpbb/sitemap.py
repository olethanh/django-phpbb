# -*- coding: utf-8 -*-
# This file is part of django-phpbb, integration between Django and phpBB
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

from django.contrib import sitemaps
from atopowe.phpbb.models import ForumTopic, ForumPost, ForumForum
from atopowe.phpbb.urls import forumqs

class ForumForumSitemap(sitemaps.Sitemap):
    changefreq = "monthly"
    priority = 0.4
    def items(self):
        return forumqs

class ForumTopicSitemap(sitemaps.Sitemap):
    changefreq = "monthly"
    priority = 0.4
    def items(self):
        return ForumTopic.objects.exclude(forum__forum_id=15).exclude(forum__forum_id=6)
    def lastmod(self, obj):
        try:
            return obj.topic_last_post.get_time()
        except ForumPost.DoesNotExist:
            return None
