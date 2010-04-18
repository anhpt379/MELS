#! coding: utf-8
import pycassa as cassa
from hashlib import sha512, md5
from cassandra.ttypes import NotFoundException, InvalidRequestException
from settings import cassandra_keyspace, cassandra_hosts
from error import Error

class Log:
    def __init__(self):
        # Connect to Cassandra servers
        client = cassa.connect(cassandra_hosts)
        self.a = cassa.ColumnFamily(client, cassandra_keyspace, 
                                            'Users', super=True)
        self.error = Error()
    
#    def write(self, session_id):
#        try:
#            username = self.a.get('session_id', session_id)['username']
#        except (NotFoundException, InvalidRequestException, KeyError):
#            return self.error.param_error("session_id không hợp lệ")
#        username = username.strip().lower()
#        self.a.insert(username, {'log', {'item)
        
    def get(self, user_id):
        pass
    

if __name__ == "__main__":
    pass