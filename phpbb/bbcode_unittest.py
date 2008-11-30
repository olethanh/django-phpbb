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

import unittest
import bbcode
# http://labix.org/mocker
import mocker


class BbCodeUnitTest(unittest.TestCase):

    def setUp(self):
        self.mocker = mocker.Mocker()
        self.user = self.mocker.mock()
        self.b1 = bbcode.BbCode(self.user)

    def tearDown(self):
        del self.b1

    def testFoo(self):
        self.user.replay()
        self.b1.bbcode_cache_init()


class BbCodeFirstPassUnitTest(unittest.TestCase):

    def setUp(self):
        self.bfp1 = bbcode.BbCodeFirstPass()

    def tearDown(self):
        del self.bfp1

    def testWarnMsg1(self):
        self.assertEquals(self.bfp1.warn_msg, [])


class BitFieldUnitTest(unittest.TestCase):

    def setUp(self):
        self.b1 = bbcode.BitField("EA==\n")

    def testGet0(self):
        self.assertEquals(self.b1.get(0), 0)
    
    def testGet3(self):
        self.assertEquals(self.b1.get(3), 16)
    
    def testGet4(self):
        self.assertEquals(self.b1.get(4), 0)
    
    def testSet0(self):
        self.b1.set(0)
        self.assertEquals(self.b1.get(0), 128)

    def testSet1(self):
        self.b1.set(0)
        self.assertEquals(self.b1.get_bin(), "10010000")
    
    def testGetBin(self):
        self.assertEquals(self.b1.get_bin(), "00010000")

    def testGetAllSet(self):
        self.b1.set(7)
        self.assertEquals(self.b1.get_all_set(), [3, 7])
    
    def testGetBlob(self):
        self.assertEquals(self.b1.get_blob(), '\x10')

    def testMerge(self):
        b1 = bbcode.BitField()
        b2 = bbcode.BitField()
        b1.set(0)
        b2.set(1)
        self.assertEquals(b2.get(1), 64)
        b1.merge(b2)
        self.assertEquals(b1.get(0), 128)
        self.assertEquals(b1.get(1), 64)
        del b1, b2
    
    def tearDown(self):
        del self.b1


if __name__ == '__main__':
    unittest.main()
