#!/usr/bin/env python
#! coding: utf-8
from random import choice
from string import letters, digits
from datetime import datetime
from pycassa import connect, ColumnFamily
from cassandra.ttypes import NotFoundException
from settings import cassandra_keyspace, cassandra_hosts
from error import Error


class ActiveCode:
    def __init__(self):
        # Connect to Cassandra servers
        client = connect(cassandra_hosts)
        self.u = ColumnFamily(client, cassandra_keyspace, 
                                    'Users', super=True)
        self.e = Error()

    def _gen_active_code(self, length=6, chars=(letters + digits)):
        return ''.join([choice(chars) for _ in xrange(length)])
    
    def _is_exist(self, code):
        try:
            self.u.get('active_codes', super_column=code)
            return True
        except NotFoundException:
            return False
            
    def get_new_code(self):
        new = self._gen_active_code()
        while self._is_exist(new) is True:
            new = self._gen_active_code()
        # store in database
        self.u.insert('active_codes', {new: {'create_time': str(datetime.now())}})
        return new
    
    def active(self, username, active_code):
        if self._is_exist(active_code) is False:
            return False
        self.u.insert('active_codes', {active_code: {'active_time': str(datetime.now()),
                                                     'owner': str(username)}})
        return True
    
    def stats(self):
        return self.u.get('active_codes')
            
    
if __name__ == '__main__':
    print ActiveCode().get_new_code()
    print ActiveCode().stats()