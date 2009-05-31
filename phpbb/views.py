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

from models import PhpbbForum, PhpbbTopic, PhpbbPost, PhpbbConfig
from django.http import HttpResponseRedirect, Http404
from django.template.context import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.core.paginator import Paginator, InvalidPage
from django.core import exceptions

def phpbb_config_context(request):
    try:
        sitename = PhpbbConfig.objects.get(pk='sitename').config_value
        site_desc = PhpbbConfig.objects.get(pk='site_desc').config_value
    except PhpbbConfig.DoesNotExist, e:
        sitename = "PhpBB site"
        site_desc = "A forum: %s" % e
    return {
            'sitename': sitename,
            'site_desc': site_desc,
    }

def forum_index(request, forum_id, slug, page_no = None, paginate_by = 10):
    if page_no:
        try:
            if int(page_no) == 1:
                return HttpResponseRedirect("../")
        except ValueError:
            pass
        path_prefix = "../"
    else:
        path_prefix = ""
    try:
        page_no = int(page_no)
    except ValueError:
        page_no = 1
    except TypeError:
        page_no = 1
    if not(page_no >= 1 and page_no <= 1000):
        raise Http404
    f = PhpbbForum.objects.get(pk = forum_id)
    if f.get_slug() != slug:
        return HttpResponseRedirect(f.get_absolute_url())
    topics = f.phpbbtopic_set.all().order_by('-topic_last_post_time_int')
    paginator = Paginator(topics, paginate_by)
    print "page_no:", page_no
    try:
        print "requesting page"
        page = paginator.page(page_no)
        print "got page", page
    except InvalidPage:
        raise Http404
    c = RequestContext(request, {
            'path_prefix': path_prefix,
            'is_paginated': paginator.num_pages > 1,
            'results_per_page': paginate_by,
            'has_next': page.has_next(),
            'has_previous': page.has_previous(),
            'page': page_no,
            'next': page_no + 1,
            'previous': page_no - 1,
            'pages': paginator.num_pages,
            'hits' : 'what hits?',
            'page_list': range(1, paginator.num_pages + 1),
    }, [phpbb_config_context])
    return render_to_response("phpbb/forum_detail.html", {
        'object': f,
        'topics': page.object_list,
        }, context_instance=c)


def topic(request, topic_id, slug, page_no = None, paginate_by = 10):
    if page_no:
        try:
            if int(page_no) == 1:
                return HttpResponseRedirect("../")
        except:
            pass
        path_prefix = "../"
    else:
        path_prefix = ""
    try:
        page_no = int(page_no)
    except:
        page_no = 1
    if not(page_no >= 1 and page_no <= 1000):
        raise Http404
    try:
        t = PhpbbTopic.objects.get(pk = topic_id)
    except exceptions.ObjectDoesNotExist, e:
        raise Http404
    posts = t.phpbbpost_set.all()
    if t.get_slug() != slug:
        return HttpResponseRedirect(t.get_absolute_url())
    paginator = Paginator(posts, paginate_by)
    try:
        page = paginator.page(page_no)
    except InvalidPage:
        raise Http404
    c = RequestContext(request, {
            'path_prefix': path_prefix,
            'is_paginated': paginator.num_pages > 1,
            'results_per_page': paginate_by,
            'has_next': page.has_next(),
            'has_previous': page.has_previous(),
            'page': page_no,
            'next': page_no + 1,
            'previous': page_no - 1,
            'pages': paginator.num_pages,
            'hits' : "hits? what hits?",
            'page_list': range(1, paginator.num_pages + 1),
    }, [phpbb_config_context])
    return render_to_response("phpbb/topic_detail.html", {
        'object': t,
        'posts': page.object_list,
        }, context_instance=c)


def unanswered(request):
    topics = PhpbbTopic.objects.filter(topic_replies = 0)
    c = RequestContext(request, {}, [phpbb_config_context])
    return render_to_response(
            "phpbb/unanswered.html",
            {'topics': topics,},
            context_instance=c)


def handle_viewtopic(request):
    if request.GET.has_key('t'):
        topic_id = request.GET['t']
        t = PhpbbTopic.objects.get(pk = topic_id)
        return HttpResponseRedirect(t.get_absolute_url())
    if request.GET.has_key('p'):
        topic_id = request.GET['p']
        t = PhpbbPost.objects.get(pk = topic_id)
        return HttpResponseRedirect(t.get_absolute_url())
