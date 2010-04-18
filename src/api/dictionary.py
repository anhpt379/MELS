#!/usr/bin/env python
#! coding: utf-8
from lib.text_processing import xml_format
from pycassa import connect, ColumnFamily
from cassandra.ttypes import NotFoundException, InvalidRequestException
from settings import cassandra_keyspace, cassandra_hosts
from error import Error


class Dictionary:
    """
    Nhóm chức năng từ điển:
        * Tra từ Anh-Việt
        * Tra từ Việt-Anh
    """
    def __init__(self):
        # Connect to Cassandra servers
        client = connect(cassandra_hosts)
        self.d = ColumnFamily(client, cassandra_keyspace, 'Dictionary', super=True)
        self.u = ColumnFamily(client, cassandra_keyspace, 'Users', super=True)
        self.e = Error()
    
    def _lookup(self, keyword, dict_type='en_vi'):
        try:
            return self.d.get(dict_type, super_column=str(keyword))
        except (NotFoundException, InvalidRequestException):
            return None
    
    def lookup(self, environ):
        try:
            session_id = environ['request']['session_id']
        except KeyError:
            return self.e.authen_error("Thiếu session_id")
        try:
            self.u.get('session_id', super_column=session_id)
        except (NotFoundException, InvalidRequestException):
            return self.e.authen_error()
        result = self._lookup(environ['request']['keyword'])
        result2 = self._lookup(environ['request']['keyword'], 'vi_en')
        result3 = self._lookup(environ['request']['keyword'], 'en_en')
        if (result is None) and (result2 is None) and (result3 is None):
            return self.e.not_found("Từ khóa bạn tìm không có trong từ điển")
        xml = []
        if result is not None:
            xml.append('<result type="en_vi" keyword="%s" mean="%s" spell="%s" status_code="200"/>' \
                % (xml_format(environ['request']['keyword']), 
                   xml_format(result['nghia']), 
                   xml_format(result['phien_am_quoc_te'])))
        if result2 is not None:
            xml.append('<result type="vi_en" keyword="%s" mean="%s" spell="" status_code="200"/>' \
                % (xml_format(environ['request']['keyword']), 
                   xml_format(result2['nghia'])))
        return '\n\n'.join(xml)

    def total_words(self, dict_type='en_vi'):
        return self.d.get_count(dict_type)
    

if __name__ == '__main__':
    from api.authentication import Authentication
    session_id = Authentication()._login('Tuan Anh', 'pta')
    print session_id
    environ = {}
    environ['request'] = {}
    environ['request']['session_id'] = session_id
    environ['request']['keyword'] = 'ai nấy'
    print Dictionary().lookup(environ)