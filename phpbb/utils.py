#!/usr/bin/python
# -*- coding: utf-8 -*-
# This file is part of django-phpbb, a Django-phpBB integration project
# Copyright (C) 2007-2008  Maciej Bliziński
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

import re
import string

def slugify(s):
    # FIXME: This is Polish-language-specific.
    STOPLIST = [ 'i', 'a', 'z', 'w', 'u', 'o', 
            'jak', 'sie', 'do', 
            'na', 'to', 'quot', 'gt',
            ]
    if type(s) != unicode:
        s = unicode(s, 'utf-8')
    s = s.lower()
    # FIXME: This is Polish-language-specific.
    s = s.replace(u'ą', u'a')
    s = s.replace(u'ć', u'c')
    s = s.replace(u'ę', u'e')
    s = s.replace(u'ł', u'l')
    s = s.replace(u'ń', u'n')
    s = s.replace(u'ó', u'o')
    s = s.replace(u'ś', u's')
    s = s.replace(u'ż', u'z')
    s = s.replace(u'ź', u'z')
    s = s.encode('utf-8')
    keywords = re.findall(r'\w+', s.lower())
    for stopkw in STOPLIST:
        while stopkw in keywords:
            keywords.remove(stopkw)
    return u'-'.join(keywords)
