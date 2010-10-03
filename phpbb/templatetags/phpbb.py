# -*- coding: UTF-8 -*-
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

import re

from django.template.defaultfilters import stringfilter
from django import template
from django.conf import settings

register = template.Library()


SUBS = (
        #lists
        (r'\[\*:[^\]]+\](.*?)\n \[/\*:[^\]]+\]',r'<li>\1</li>'),
        (r'\[\*:[^\]]+\](.*?)\[/\*:[^\]]+\]',r'<li>\1</li>'),
        (r'\[list:[^\]]+\](.*?)\[/list:[^\]]+\]',r'<ul>\1</ul>'),
        # URLS
        (r'\[url=([^\]]*)\]([^\[]*)\[/url\]', r'<a href="\1">\2</a>'),
        (r'\[url=([^\]]*):\w+\](.*?)\[/url:\w+\]', r'<a href="\1">\2</a>'),
        (r'\[url\](.*?)\[/url\]', r'<a href="\1">\1</a>'),
        # IMG
        (r'\[img:\w+\]([^\[]*)\[/img:\w+\]', r'<img src="\1" />'),
        # Smilies path
        ('{SMILIES_PATH}', settings.PHPBB_SMILIES_URL),
        # [u], [i], [b]
        (r'\[b:[^\]]*\]([^\[]*)\[/b:[^\]]*\]', r'<b>\1</b>'),
        (r'\[i:[^\]]*\]([^\[]*)\[/i:[^\]]*\]', r'<i>\1</i>'),
        (r'\[u:[^\]]*\]([^\[]*)\[/u:[^\]]*\]', r'<u>\1</u>'), #DEPRECATED, FIXME

#        (r'\[\*:[^\]]*\]([^\[]*)\[/i:[/\*^\]]*\]', r'<i>\1</i>'),
        #quote
        (r'\[quote:\w+\]([^\[]*)\[/quote:\w+\]', r'<blockquote>\1</blockquote>'),
        (r'\[quote=&quot;(.+?)&quot;:\w+\](.*)\[/quote:\w+\]', r'<blockquote><strong>\1:</strong><br /> \2</blockquote>'),
        (r'\[quote="(.+?)":\w+\](.*)\[/quote:\w+\]', r'<blockquote><strong>\1:</strong><br /> \2</blockquote>'),
        # size
        (r'\[size=([0-9]+):\w+\](.*)\[/size:\w+\]', r'<font size="\1">\2</font>'),
        # Automatically convert http:// in url
        (r'(\s)http://([\w,.?=%/-]+)', r'<a href="\2">\2</a>(\s)'),
        # Return to the line
        (r'\n', r'<br>\n'),
        ## No idea, really
        #(r'\?+', r'?'),
        # Remove all tags, don't know why you would want that
        #(r'<![^>]+>', r' '),
        #(r'<img[^>]+>', r' '),
        #(r'<a[^>]+>', r' '),
        #(r'</[^>]+>', r' '),
        )

# Compiled subs
CSUBS = [(re.compile(a,re.S),b) for a,b in SUBS]

@register.filter
@stringfilter
def bbcode(s):
    for pattern, replacement in CSUBS:
        s = pattern.sub(replacement, s)

    return s

bbcode.is_safe = True

@register.filter
def withlink(obj):
    return "<a href=\"%s\">%s</a>" % (obj.get_absolute_url(), str(obj))


