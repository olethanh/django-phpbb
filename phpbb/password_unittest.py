#!/usr/bin/python

import password
import unittest

class PhpbbPassword(unittest.TestCase):

    def setUp(self):
        self.p1 = password.PhpbbPassword()

    def tearDown(self):
        del self.p1

    def test_hash_crypt_private01(self):
        """Wrong length."""
        self.assertEquals(
                self.p1.wrong,
                self.p1._hash_crypt_private('foo', 'bar'))

    def test_hash_crypt_private02(self):
        self.assertEquals(
                "$H$9qS9RNyN8vivqlYBLHPGI9g5HJWHvD1",
                self.p1._hash_crypt_private(
                    "foobar", "$H$9qS9RNyN8vivqlYBLHPGI9g5HJWHvD1")) 

    def test_unicodePassword(self):
        self.assertEquals(
                "$H$9qS9RNyN8vivqlYBLHPGI9g5HJWHvD1",
                self.p1._hash_crypt_private(
                    unicode("foobar"), "$H$9qS9RNyN8vivqlYBLHPGI9g5HJWHvD1")) 

    def test_hash_crypt_private03(self):
        """No $H$ at the beginning."""
        self.assertEquals(
                self.p1.wrong,
                self.p1._hash_crypt_private(
                    'foo', '0123456789023456789012345678901234'))

    def test_hash_encode64_1(self):
        self.assertNotEquals("", self.p1._hash_encode64("foobar", 6));

    def test_hash_encode64_2(self):
        self.assertEquals("axqPW3aQ", self.p1._hash_encode64("foobar", 6));

    def test_hash_encode64_3(self):
        self.assertEquals("........", self.p1._hash_encode64("", 6));

    def test_hash_encode64_4(self):
        self.assertEquals("a/......", self.p1._hash_encode64("f", 6));

    def test_hash_encode64_5(self):
        self.assertEquals("..", self.p1._hash_encode64("", 0));

    def test_phpbb_check_hash(self):
        self.assertTrue(self.p1.phpbb_check_hash(
            "foobar", "$H$9qS9RNyN8vivqlYBLHPGI9g5HJWHvD1")) 

    def test_ordx1(self):
        self.assertEquals(0, self.p1._ordx("", 0));

    def test_ordx2(self):
        self.assertEquals(97, self.p1._ordx("a", 0));

    def test_ordx3(self):
        self.assertEquals(0, self.p1._ordx("a", 1));


if __name__ == "__main__":
    unittest.main()
