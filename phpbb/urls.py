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

from django.conf.urls.defaults import *
from django.utils.translation import gettext_lazy as _
import views
import models

forumqs = (models.PhpbbForum.objects.exclude(forum_name='INDEX PAGE').
           exclude(forum_name='MEMBERLIST').
           # FIXME: hardcoded forum IDs
           exclude(forum_id=15).
           exclude(forum_id=6))

forum_context = views.phpbb_config_context(None)

urlpatterns = patterns('',
    # TODO: add context with Django config
    (r'^$', 'django.views.generic.list_detail.object_list',
        {'queryset': forumqs,
         'extra_context': forum_context}),
    (r'^%s/(?P<topic_id>[0-9]+)/(?P<slug>[\w-]*)/page(?P<page_no>[0-9]+)/$' % (
    	    _("topics"),), 'django.contrib.phpbb.views.topic', ),
    (r'^%s/(?P<topic_id>[0-9]+)/(?P<slug>[\w-]*)/$' % (
    	    _("topics"),), 'django.contrib.phpbb.views.topic', ),
    (r'^(?P<forum_id>[0-9]+)/(?P<slug>[\w-]*)/$',
        'django.contrib.phpbb.views.forum_index', ),
    (r'^(?P<forum_id>[0-9]+)/(?P<slug>[\w-]*)/page(?P<page_no>[0-9]+)/$',
        'django.contrib.phpbb.views.forum_index', ),
    (r'^(?P<forum_id>[0-9]+)/$',
        'django.contrib.phpbb.views.forum_index', {'slug': ''}),
    (r'^unanswered/$', 'django.contrib.phpbb.views.unanswered', ),
    (r'^viewtopic.php$', 'django.contrib.phpbb.views.handle_viewtopic', ),
)
