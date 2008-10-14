# -*- coding: UTF-8 -*-
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

from django.contrib.auth.models import User
from atopowe.phpbb.models import ForumUser
import md5

class PhpbbBackend:
    def authenticate(self, username = None, password = None):
        """Check if the user exists in Django users. If not, create it.
        Then authenticate."""
        user = None
	wrongly_encoded_username = username.decode('utf-8').encode('latin2').decode('latin1')
        try:
            phpbb_user = ForumUser.objects.get(username = wrongly_encoded_username)
        except ForumUser.DoesNotExist:
            # The user does not exist in phpBB. Bailing out.
            return None
        m = md5.new()
        m.update(password)
        pass_md5 = m.hexdigest()
        # print "%s, %s" % (pass_md5, phpbb_user.user_password)
        if pass_md5 == phpbb_user.user_password:
            valid = True
        else:
            # Invalid password
            return None
        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            if username is not None:
                user = User(username = username, password = "")
                user.set_password(password)
                user.is_staff = False
                user.is_superuser = False
                user.email = phpbb_user.user_email
                user.save()
            else:
                return None
        return user
    def get_user(self, id):
        return User.objects.get(pk = id)
