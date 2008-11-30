# -*- coding: UTF-8 -*-
#
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

from django.utils.translation import gettext_lazy as _
from django.contrib.syndication.feeds import Feed
from models import PhpbbPost

class LatestPhpbbPosts(Feed):
    title = u"Forum"
    link = "/forum/"
    description = _("Newest posts on the forum.")
    def items(self):
        return (PhpbbPost.objects.order_by('-post_time_int').
            exclude(topic__forum__forum_id=15).
            exclude(topic__forum__forum_id=6)[:20])
    def item_link(self, obj):
        return obj.get_external_url()
