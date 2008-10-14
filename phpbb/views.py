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

from phpbb.models import ForumForum, ForumTopic, ForumPost
from django.http import HttpResponseRedirect, Http404
from django.template.context import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.core.paginator import ObjectPaginator, InvalidPage
from django.core import exceptions


def forum_index(request, forum_id, slug, page = None, paginate_by = 10):
    if page:
        try:
            if int(page) == 1:
                return HttpResponseRedirect("../")
        except:
            pass
        path_prefix = "../"
    else:
        path_prefix = ""
    try:
        page = int(page)
    except:
        page = 1
    if not(page >= 1 and page <= 1000):
        raise Http404
    f = ForumForum.objects.get(pk = forum_id)
    # if f.auth_read != 0:
    #     raise Http404
    if f.get_slug() != slug:
        return HttpResponseRedirect(f.get_absolute_url())
    topics = f.forumtopic_set.all()
    paginator = ObjectPaginator(topics, paginate_by)
    try:
        object_list = paginator.get_page(page - 1)
    except InvalidPage:
        raise Http404
    c = RequestContext(request, {
            'path_prefix': path_prefix,
            'is_paginated': paginator.pages > 1,
            'results_per_page': paginate_by,
            'has_next': paginator.has_next_page(page - 1),
            'has_previous': paginator.has_previous_page(page - 1),
            'page': page,
            'next': page + 1,
            'previous': page - 1,
            'pages': paginator.pages,
            'hits' : paginator.hits,
            'page_list': range(1, paginator.pages + 1),
    })
    return render_to_response("phpbb/forum_detail.html", {
        'object': f,
        'topics': object_list,
        }, context_instance = c)


def topic(request, topic_id, slug, page = None, paginate_by = 10):
    if page:
        try:
            if int(page) == 1:
                return HttpResponseRedirect("../")
        except:
            pass
        path_prefix = "../"
    else:
        path_prefix = ""
    try:
        page = int(page)
    except:
        page = 1
    if not(page >= 1 and page <= 1000):
        raise Http404
    try:
        t = ForumTopic.objects.get(pk = topic_id)
    except exceptions.ObjectDoesNotExist, e:
        raise Http404
    # if t.forum.auth_read != 0:
    #     raise Http404
    posts = t.forumpost_set.all()
    if t.get_slug() != slug:
        return HttpResponseRedirect(t.get_absolute_url())
    paginator = ObjectPaginator(posts, paginate_by)
    try:
        object_list = paginator.get_page(page - 1)
    except InvalidPage:
        raise Http404
    c = RequestContext(request, {
            'path_prefix': path_prefix,
            'is_paginated': paginator.pages > 1,
            'results_per_page': paginate_by,
            'has_next': paginator.has_next_page(page - 1),
            'has_previous': paginator.has_previous_page(page - 1),
            'page': page,
            'next': page + 1,
            'previous': page - 1,
            'pages': paginator.pages,
            'hits' : paginator.hits,
            'page_list': range(1, paginator.pages + 1),
    })
    return render_to_response("phpbb/topic_detail.html", {
        'object': t,
        'posts': object_list,
        }, context_instance = c)


def unanswered(request):
    topics = ForumTopic.objects.filter(topic_replies = 0)
    return render_to_response("phpbb/unanswered.html", {
        'topics': topics,
        }, context_instance = RequestContext(request))


def handle_viewtopic(request):
    if request.GET.has_key('t'):
        topic_id = request.GET['t']
        t = ForumTopic.objects.get(pk = topic_id)
        return HttpResponseRedirect(t.get_absolute_url())
    if request.GET.has_key('p'):
        topic_id = request.GET['p']
        t = ForumPost.objects.get(pk = topic_id)
        return HttpResponseRedirect(t.get_absolute_url())
