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

import logging
from django.contrib.auth.models import User
from models import PhpbbUser
import password as php_password

from django.conf import settings

logging.basicConfig(level=logging.DEBUG)
logging.debug(str(getattr(settings, 'DEBUG', True)))
if getattr(settings, 'DEBUG', True):
    logging_level = logging.DEBUG
else:
    logging_level = logging.FATAL
logging.basicConfig(level=logging_level)

class PhpbbBackend:

    def authenticate(self, username=None, password=None):
        """Authenticate user against phpBB3 database.
        
        Check if the user exists in Django users. If not, create it.
        Then authenticate."""
        logging.debug("PhpbbBackend::authenticate()")
        user = None
        try:
            phpbb_user = PhpbbUser.objects.get(username = username)
        except PhpbbUser.DoesNotExist:
            # The user does not exist in phpBB. Bailing out.
            logging.info("User '%s' doesn't exist." % username)
            return None
        phpbb_checker = php_password.PhpbbPassword()
        if phpbb_checker.phpbb_check_hash(password, phpbb_user.user_password):
            logging.debug("User %s successfully authenticated "
                         "with phpBB database." % username)
        else:
            # Invalid password
            logging.info("Wrong password for user %s" % username)
            return None
        # At this point we have successfully checked phpBB user password.
        # Now we're getting and returning Django user. If necessary, we're
        # creating the user on the fly.
        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            logging.info("Creating new Django user '%s'" % username)
            if username:
                user = User(username = username, password = "")
                user.is_staff = False
                user.is_superuser = False
                user.email = phpbb_user.user_email
                user.save()
            else:
                logging.warning("User name empty. Not creating.")
                return None
        # In case the phpBB password has changed, we're updating user's
        # Django password. Django password is necessary when user wants to log
        # in to the admin interface.
        user.set_password(password)
        logging.debug("Returning user '%s'" % user)
        return user

    def get_user(self, user_id):
        user = User.objects.get(pk = user_id)
        logging.debug("get_user(): Returning user '%s'" % user)
        return user
