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

from django import template
import re

register = template.Library()

# @register.filter
def bbcode(s):
    # s = re.sub(r'\[quote:\w+\]([^\[]*)\[/quote:\w+\]', r'<blockquote>\1</blockquote>', s)
    s = re.sub(r'\[quote:\w+\]([^\[]*)\[/quote:\w+\]', r'<blockquote>\1</blockquote>', s)
    s = re.sub(r'\[quote:\w+="([\w\s]+)"\]([^\[]*)\[/quote:\w+\]', r'<blockquote><strong>\1:</strong><br /> \2</blockquote>', s)
    # s = re.sub(r'\[size=([0-9]+):\w+\](.*)\[/size:\w+\]', r'<font size="\1">\2</font>', s)
    s = re.sub(r'\[b:[^\]]*\]([^\[]*)\[/b:[^\]]*\]', r'<b>\1</b>', s)
    s = re.sub(r'\[i:[^\]]*\]([^\[]*)\[/i:[^\]]*\]', r'<i>\1</i>', s)
    # s = re.sub(r'(\s)http://([\w,.?=%/-]+)', r'<a href="\2">\2</a>(\s)', s)
    s = re.sub(r'\[url=([^\]]*)\]([^\[]*)\[/url\]', r'<a href="\1">\2</a>', s)
    s = re.sub(r'\[url\]([^\[]*)\[/url\]', r'<a href="\1">\1</a>', s)
    s = re.sub(r'\[img:\w+\]([^\[]*)\[/img:\w+\]', r'<img src="\1" />', s)
    s = re.sub(r':lol:', r'<img alt="Hahaha!" src="http://www.atopowe-zapalenie.pl/forum/images/smiles/icon_lol.gif" />', s)
    s = re.sub(r':wink:', r'<img alt="Puszcza oczko" src="http://www.atopowe-zapalenie.pl/forum/images/smiles/icon_wink.gif" />', s)
    s = re.sub(r':!:', r'/!\\', s)
    s = re.sub(r'\n\n', r'\n', s)
    # Cudzysłowy drukarskie
    # s = re.sub(r'"([^"]+)"', r'„\1”', s)
    # usuwamy odstępy przed interpunkcją
    s = re.sub(r'\s+([?!.,]\))', r'\1', s)
    # spacja po interpunkcji
    # s = re.sub(r'([?!.,\)])([\wąćęłńóśżź])', r'\1 \2', s)
    # musi być spacja przed nawiasem
    # s = re.sub(r'([\wąćęłńóśżź])(\()', r'\1 \2', s)
    s = re.sub(r'\?+', r'?', s)
    # Remove HTML comment tags
    s = re.sub(r'<![^>]+>', r' ', s)
    s = re.sub(r'<img[^>]+>', r' ', s)
    s = re.sub(r'<a[^>]+>', r' ', s)
    s = re.sub(r'</[^>]+>', r' ', s)
    # change URLs
    s = re.sub(r'\[url=([^]]+)\]([^\[]+)\[/url:?[^]]+\]', r'\2', s)
    # TODO: implement links
    # re.sub(r'\[url=([^]]+)\]([^\[]+)\[/url:?[^]]+\]', r'<a href="\1">\2</a>',
    # s)
    # Quotations
    s = re.sub(r'\[quote=([^]]+)\]([^\[]+)\[/quote:?[^]]+\]', r'"""\2"""', s)
    return s

# @register.filter
def withlink(obj):
    return "<a href=\"%s\">%s</a>" % (obj.get_absolute_url(), str(obj))

register.filter('bbcode', bbcode)
register.filter('withlink', withlink)

class BaseForumNode(template.Node):
    pass

def forum_list(parser, token):
    """Gets list of forums."""
    pass

register.tag(forum_list)
