#!/usr/bin/env python
#! coding: utf-8
from string import lowercase
from random import random
from hashlib import sha512, md5
from datetime import datetime
from pycassa import connect, ColumnFamily
from cassandra.ttypes import NotFoundException, InvalidRequestException
from settings import cassandra_keyspace, cassandra_hosts, trial_time
from error import Error


class Authentication:
    """
    Nhóm chức năng quản lý người dùng
    Các hành động hỗ trợ:
        * đăng ký
        * đăng nhập
        * đăng xuất
    """
    def __init__(self):
        # Connect to Cassandra servers
        client = connect(cassandra_hosts)
        self.a = ColumnFamily(client, cassandra_keyspace, 
                                    'Users', super=True)
        self.e = Error()

    def _check(self, username):
        try:
            username = username.strip().lower()
            self.a.get(username)
            return 1
        except (NotFoundException, InvalidRequestException):
            return 0
    
    def _remove(self, username):
        try: 
            username = username.strip().lower()
            self.a.remove(username)
            return 1
        except (NotFoundException, InvalidRequestException):
            return 0
    
    def _register(self, username, password, phone_number):
        try:
            username = username.strip().lower()
            if self._check(username) == 1:
                return False
            salt = str(random()) 
            password = sha512(password + salt).hexdigest()
            self.a.insert(username, {'info': {'password': password,
                                              'salt': salt,
                                              'phone_number': str(phone_number),
                                              'join_time': str(datetime.now())}})
            return True
        except (NotFoundException, InvalidRequestException):
            return False
    
    def _login(self, username, password):
        try:
            username = username.strip().lower()
            store_data = self.a.get(username, super_column='info')
            store_passwd = store_data['password']
            store_salt = store_data['salt']
            store_join_time = datetime.strptime(store_data['join_time'], '%Y-%m-%d %H:%M:%S.%f')
            password = sha512(password + store_salt).hexdigest()
            if password == store_passwd:
                session_id = md5(username + str(datetime.now())).hexdigest()
                #--- check trial expire ---
                delta = datetime.now() - store_join_time
                if delta.days > trial_time:
                    return 402
                #--- end check ---
                self.a.insert('session_id', 
                              {session_id: {'username': username,
                                            'timestamp': str(datetime.now())}})
                return session_id
            return False
        except (NotFoundException, InvalidRequestException):
            return False
    
    def _logout(self, session_id):
        try:
            self.a.get('session_id', super_column=session_id)    # check if exist
            self.a.remove('session_id', session_id)
            return True
        except (NotFoundException, InvalidRequestException):
            return False
    
    def register(self, environ):
        try:
            username = environ['request']['username']
            password = environ['request']['password']
            phone_number = environ['request']['phone_number']
        except KeyError:
            return self.e.bad_request("Hành động này yêu cầu 4 tham số: username, password, phone_number và api_key")
        username = username.strip().lower()
        # check params
        allow_chars = lowercase + '.-_@'
        for char in username:
            if char not in allow_chars:
                self.e.param_error("Tên đăng nhập chỉ được dùng các ký tự a-z, A-Z và .-_@")
        if len(password) != 32:
            return self.e.param_error("Mật khẩu phải được mã hóa md5 trước khi gửi lên")
        
        #----- check phone_number (dạng 841673450799) -----        
        if phone_number != '':
            phone_number = phone_number.replace(' ', '')
            phone_number = "\t" + phone_number
            if phone_number.startswith('\t+'):
                phone_number = phone_number.replace('\t+', '\t') # remove +
            # normalize
            if phone_number.startswith('\t09'):
                phone_number = phone_number.replace('\t09', '849')
            elif phone_number.startswith('\t01'):
                phone_number = phone_number.replace('\t01', '841')
            else:
                return self.e.param_error("phone_number không hợp lệ")
            if len(phone_number) in (11, 12):
                try:
                    phone_number = int(phone_number)
                except ValueError: # not int
                    return self.e.param_error("phone_number không hợp lệ")
            else:
                return self.e.param_error("phone_number không hợp lệ")
        #----- end phone_number check -----
        result = self._register(username, password, phone_number)
        if result is True:
            xml = '<register status_code="201" description="Tài khoản đã được tạo thành công"/>'
            return xml
        else:
            xml = '<register status_code="406" description="Tham số không hợp lệ"/>'
            return xml
    
    def login(self, environ):
        try:
            username = environ['request']['username']
            password = environ['request']['password']
        except KeyError:
            return self.e.bad_request("Hành động này yêu cầu 3 tham số: username, password và api_key")
            
        result = self._login(username, password)
        if result is False:
            xml = '<login status_code="401" description="Tên đăng nhập/mật khẩu không hợp lệ"/>'
            return xml
        elif result == 402:
            return self.e.trial_expired()
        else:
            xml = '<login status_code="202" session_id="%s" description="Đăng nhập thành công"/>' % (result)
            return xml
    
    def logout(self, environ):
        try:
            session_id = environ['request']['session_id']
        except KeyError:
            return self.e.bad_request("Hành động này yêu cầu 2 tham số: session_id và api_key")
            
        result = self._logout(session_id)
        if result is True:
            xml = '<logout status_code="200" description="Đăng xuất thành công"/>'
            return xml
        else:
            xml = '<logout status_code="401" description="session_id không hợp lệ"/>'
            return xml


if __name__ == '__main__':
    from hashlib import md5
    a = Authentication()
    a._remove('Tuan Anh')
    
    password = md5('pta').hexdigest()
    print a._register('Tuan Anh', password, '01673450799')
    print a._login('Tuan Anh', password)
    print a._logout(a._login('Tuan Anh', password))

    environ = {}
    environ['request'] = {}
    environ['request']['session_id'] = a._login('testafds', password)
    print environ['request']['session_id'] 
    print a.logout(environ)