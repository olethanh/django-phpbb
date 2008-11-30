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

"""Port of phpBB's bbcode.

Sources:
http://code.phpbb.com/repositories/entry/5/trunk/phpBB/includes/bbcode.php
http://code.phpbb.com/repositories/entry/5/trunk/phpBB/includes/message_parser.php
"""

import logging

def decbin(n):
    """PHP in-built function port."""
    bin_str = ""
    if n < 0:
        raise ValueError, "Positive integer required"
    if n == 0:
        return '0'
    while n > 0:
        bin_str = str(n % 2) + bin_str
        n = n >> 1
    return bin_str


class BitField(object):
    """Bitfield class from phpBB.

http://code.phpbb.com/repositories/entry/5/trunk/phpBB/includes/functions_content.php"""
    def __init__(self, bitfield=""):
        self.data = bitfield.decode("base64")
    
    def get(self, n):
        byte = n >> 3
        if len(self.data) >= byte + 1:
            c = self.data[byte]
            # Lookup the (n % 8)th bit of the byte
            bit = 7 - (n & 7);
            return ord(c) & (1 << bit)
        else:
            return False

    def set(self, n):
        byte = n >> 3
        bit = 7 - (n & 7)
        if len(self.data) >= byte + 1:
            # Strings in Python are immutable.
            list_data = list(self.data)
            list_data[byte] = chr(ord(self.data[byte]) | (1 << bit))
            self.data = "".join(list_data)
        else:
            self.data += chr(0) * (byte - len(self.data))
            self.data += chr(1 << bit)

    def clear(self, n):
        byte = n >> 3
        if len(self.data) >= byte + 1:
            bit = 7 - (n & 7)
            # Strings in Python are immutable.
            list_data = list(self.data)
            list_data[byte] = chr(ord(self.data[byte]) &~ (1 << bit))
            self.data = "".join(list_data)

    def get_blob(self):
        return self.data

    def get_base64(self):
        return self.data.encode("base64")

    def get_bin(self):
        bin = "";
        data_len = len(self.data)
        for i in range(data_len):
            # str_pad(decbin(ord($this->data[$i])), 8, '0', STR_PAD_LEFT);
            bin += decbin(ord(self.data[i])).rjust(8, '0')
        return bin

    def get_all_set(self):
        pairs_with_ones = filter(lambda x: x[1] == '1',
                                 enumerate(self.get_bin()))
        return [x[0] for x in pairs_with_ones]

    def merge(self, bitfield):
        # Python doesn't support binary operations on strings
        data_list = list(self.data)
        # When PHP makes an 'or' on two strings of different length, it
        # justifies to the left before merging.
        max_len = max(len(self.data), len(bitfield.get_blob()))
        a = self.get_blob().ljust(max_len, chr(0))
        b = bitfield.get_blob().ljust(max_len, chr(0))
        dst_list = []
        for i in range(max_len):
            dst_list.append(chr(ord(a[i]) | ord(b[i])))
        self.data = "".join(dst_list)


class BbCode(object):
    """Port of bbcode phpBB class.

Differences from the original class:

- user is passed to the constructor (on original code, a global variable is
  used)
"""
    
    def __init__(self, user, bitfield=""):
        self.user = user
        if bitfield:
            self.bbcode_bitfield = bitfield
            self.bbcode_cache_init()
        self.bbcode_uid = ''
        self.bbcode_bitfield = ''
        self.bbcode_cache = []
        self.bbcode_template = []
        self.bbcodes = [] 
        self.template_bitfield = None
        self.template_filename = ''

    def bbcode_cache_init(self):
        if not self.template_filename:
            template_bitfield = BitField(self.user.user_sig_bbcode_bitfield)
            # TODO: continue from here.
            # Create a way to access phpBB settings.


class BbCodeFirstPass(BbCode):

    def __init__(self, message="", warn_msg=None, parsed_items=None):
        self.message = message
        if not warn_msg:
            warn_msg = []
        self.warn_msg = warn_msg
        if not parsed_items:
            parsed_items = []
        self.parsed_items = parsed_items

    def parse_bbcode(self):
        if not self.bbcodes:
            self.bbcode_init()
