#!/usr/bin/python
# -*- coding: utf-8 -*-

# mysql_repair_encoding.py is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# django-phpbb is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with django-phpbb; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor,
# Boston, MA  02110-1301  USA

"""mysql_repair_encoding.py - Fixes utf-8 represented as latin1 in MySQL."""

__author__ = "Maciej Bliziński"
__version__ = "1.0.0"

import MySQLdb
import optparse
import getpass

class EncodingFixer(object):
    """Returns SQL code to fix encodings."""
    GET_TABLES_SQL = """
SELECT
    table_name,
    column_name,
    column_type,
    character_set_name
FROM
    columns
WHERE
    table_schema = %s
    AND
    (
        data_type = 'varchar'
            OR
        data_type = 'text'
    )
    AND
    character_set_name != 'utf8'
;
"""

    def __init__(self, db_name, mysql_user, mysql_passwd=None):
        self.db_name = db_name
        if mysql_passwd:
            passwd = getpass.getpass("Password of MySQL %s user: " % mysql_user)
            self.conn = MySQLdb.connect(db='information_schema',
                    user=mysql_user,
                    passwd=passwd)
        else:
            self.conn = MySQLdb.connect(db='information_schema',
                    user=mysql_user)

    def get_sql_statements(self):
        """Returns a list of SQL statements."""
        sql_list = []
        c = self.conn.cursor()
        c.execute(self.GET_TABLES_SQL, (self.db_name,))
        if not c.rowcount:
            sql_list.append("-- No non-utf-8 columns found.")
            return sql_list
        sql_list.append("-- Got %s rows." % c.rowcount)
        row = c.fetchone()
        while row:
            table_name, column_name, column_type, character_set_name = row
            sql_list.append(("ALTER TABLE %s MODIFY COLUMN %s %s "
                   "CHARACTER SET utf8 COLLATE utf8_bin;"
                    ) % (table_name, column_name, column_type))
            sql_list.append("UPDATE %s SET %s = CONVERT(CONVERT(CONVERT("
                   "%s USING %s) USING binary) USING utf8);"
                   % (table_name, column_name, column_name, character_set_name))
            row = c.fetchone()
        return sql_list

    def get_sql(self):
        return "\n".join(self.get_sql_statements())


def main():
    parser = optparse.OptionParser()
    parser.add_option("-d", "--database",
                      dest="database",
                      help="MySQL database name")
    parser.add_option("-u", "--user", dest="user")
    parser.add_option("-p", "--password",
                      dest="passwd",
                      default=None,
                      action="store_true",
                      help="Use password")
    (options, args) = parser.parse_args()
    if not options.database:
        raise Exception("Please provide a database name. Use --help.")
    if not options.user:
        raise Exception("Please provide a user name. Use --help.")
    f = EncodingFixer(
            db_name=options.database,
            mysql_user=options.user,
            mysql_passwd=options.passwd)
    print f.get_sql()


if __name__ == "__main__":
    main()
