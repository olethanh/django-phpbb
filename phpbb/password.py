import md5

class PhpbbPassword(object):
    """PhpBB3 password compatibility class.
    
Ported from:
http://code.phpbb.com/repositories/entry/5/trunk/phpBB/includes/functions.php
    """

    itoa64 = "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    wrong = "*"

    def php_hash(self, password):
        """Hash the password."""
        raise NotImplementedError


    def phpbb_check_hash(self, password, hash):
        """Check for correct password.

        @param string $password The password in plain text
        @param string $hash The stored password hash

        @return bool Returns true if the password is correct, false if not.
        """
        if len(hash) == 34:
            return self._hash_crypt_private(password, hash, self.itoa64) == hash
        password_hash = md5.md5()
        password_hash.update(password)
        return password_hash.hexdigest() == hash


    def _hash_gensalt_private(self, input, itoa64=itoa64,
            iteration_count_log2=6):
        """Generate salt for hash generation."""
        raise NotImplementedError


    def _hash_encode64(self, input, count, itoa64=itoa64):
        """Encode hash."""
        output = ""
        i = 0
        first = True # emulate do ... while ... construct
        while first or (i < count):
            first = False
            value = self._ordx(input, i)
            i += 1
            output += itoa64[value & 0x3f]
            if i < count:
                value |= self._ordx(input, i) << 8;
            output += itoa64[(value >> 6) & 0x3f]
            if i >= count:
                i += 1
                break
            i += 1
            if i < count:
                value |= self._ordx(input, i) << 16;
            output += itoa64[(value >> 12) & 0x3f]
            if i >= count:
                i += 1
                break
            i += 1
            output += itoa64[(value >> 18) & 0x3f]
        return output


    def _hash_crypt_private(self, password, setting, itoa64=itoa64):
        """The crypt function/replacement
        
        'setting' means 'hash' or 'salt' here."""
        output = self.wrong
        if type(password) != str:
            password = str(password)
        if setting[0:3] != "$H$":
            return output
        count_log2 = itoa64.index(setting[3])
        if count_log2 < 7 or count_log2 > 30:
            return output
        count = 1 << count_log2
        salt = setting[4:12]
        if len(salt) != 8:
            return output
        # Copied from PHP source code:
        #
        # We're kind of forced to use MD5 here since it's the only cryptographic
        # primitive available in all versions of PHP currently in use.  To
        # implement our own low-level crypto in PHP would result in much worse
        # performance and consequently in lower iteration counts and hashes that
        # are quicker to crack (by non-PHP code).
        hash = md5.md5()
        hash.update(salt + password)
        first = True # emulating the "do ... while ..." construct
        while count or first:
            first = False
            # 16-character binary digest is used here.
            hash_digest = hash.digest()
            hash = md5.md5()
            hash.update(hash_digest + password)
            count -= 1
        output = setting[0:12]
        output += self._hash_encode64(hash.digest(), 16, itoa64)
        return output


    def _ordx(self, input, idx):
        """Emulating PHP behavior:

        - When extracting a character outside the string length, PHP
          returns nothing and doesn't generate an error.
        - When calculating ord() of a null object, PHP returns 0.
        """
        if idx >= len(input):
            return 0
        else:
            return ord(input[idx])
