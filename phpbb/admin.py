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

from django.contrib import admin
from django.contrib.phpbb.models import PhpbbForum
from django.contrib.phpbb.models import PhpbbPost
from django.contrib.phpbb.models import PhpbbTopic
from django.contrib.phpbb.models import PhpbbUser
from django.contrib.phpbb.models import PhpbbConfig

class PhpbbForumAdmin(admin.ModelAdmin):
    list_display = (
            'forum_name',
            'forum_id',
            'forum_desc',
            )
admin.site.register(PhpbbForum, PhpbbForumAdmin)
class PhpbbTopicAdmin(admin.ModelAdmin):
    list_display = (
        'topic_title',
        'topic_id',
        'topic_time',
    )
admin.site.register(PhpbbTopic, PhpbbTopicAdmin)
class PhpbbPostAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'get_absolute_url', 'post_time', )
admin.site.register(PhpbbPost, PhpbbPostAdmin)
class PhpbbUserAdmin(admin.ModelAdmin):
    list_display = ('username',
                    'user_id',
                    'user_regdate',
                    'user_posts',
                    'user_email', )
admin.site.register(PhpbbUser, PhpbbUserAdmin)
class PhpbbConfigAdmin(admin.ModelAdmin):
    list_display = ('config_name',
                    'config_value',
                    'is_dynamic')
admin.site.register(PhpbbConfig, PhpbbConfigAdmin)
