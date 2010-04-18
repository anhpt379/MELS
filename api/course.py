#!/usr/bin/env python
#! coding: utf-8
import os
from lib.cache import KeyValueDatabase
from pycassa import connect, ColumnFamily
from cassandra.ttypes import NotFoundException, InvalidRequestException
from settings import data_folder, audio_url_prefix, cassandra_keyspace, cassandra_hosts
from api.error import Error

class Course:
    def __init__(self):
        self.cache = KeyValueDatabase()
        client = connect(cassandra_hosts)
        self.u = ColumnFamily(client, cassandra_keyspace, 
                                            'Users', super=True)
        self.error = Error()
        
    def refresh(self):
        self.cache.flush()
    
    def _levels(self, lang='en'):
        key = 'levels_%s' % (lang)
        results = self.cache.get(key)
        if results:
            return results
        try:
            parent_folder = unicode(os.path.join(data_folder, lang))
            _levels = os.listdir(parent_folder)
            if _levels == []:
                return self.error.not_found("Chưa có dữ liệu")
            results = []
            # get only folder names
            for level in _levels:
                if os.path.isdir(os.path.join(parent_folder, level)):
                    results.append(level)
            results = sorted(results)
            self.cache.set(key, results)
            return results
        except OSError:
            return 404
    
    def _lessons(self, level, lang='en'):
        key = 'lessons_%s_%s' % (level, lang)
        results = self.cache.get(key)
        if results:
            return results
        try:
            parent_folder = unicode(os.path.join(data_folder, lang))
            parent_folder = os.path.join(parent_folder, level)
            _lessons = os.listdir(parent_folder)
            if _lessons == []:
                return self.error.not_found("Chưa có dữ liệu")
            results = []
            for lesson in _lessons:
                if os.path.isdir(os.path.join(parent_folder, lesson)):
                    results.append(lesson)
            results = sorted(results)
            self.cache.set(key, results)
            return results       
        except OSError:
            return 404
        
    def _listen(self, level, lesson, lang='en'):
        key = 'listen_%s_%s_%s' % (level, lesson, lang)
        results = self.cache.get(key)
        if results:
            return results
        try:
            parent_folder = unicode(os.path.join(data_folder, lang, level, lesson))
            audio = os.listdir(parent_folder)
            if audio == []:
                return self.error.not_found("Chưa có dữ liệu")
            results = []
            for i in audio:
                title = None
                description = None
                if i.endswith('.inf'):
                    # add '\t' to detect end string when replace
                    i = i + '\t'
                    amr = os.path.join(parent_folder, i.replace('.inf\t', '.amr'))
                    if not os.path.exists(amr): # check amr file exist
                        return 404
                    i = i.replace('\t', '') # restore i
                    # file inf chứa 2 biến là title và description
                    cmd = open(os.path.join(parent_folder, i))
                    exec(cmd)   # thực hiện chuỗi như là 1 lệnh
                    info = {'title': title,
                            'description': description,
                            'audio_file': amr.replace(data_folder, '')}
                    results.append(info)
            results = sorted(results)
            self.cache.set(key, results)
            return results
        except OSError:
            return 404  
        
    def levels(self, environ):
        try:
            lang = environ['request']['lang']
            if lang not in ('en', 'vi'):
                return self.error.param_error("Hệ thống chỉ hỗ trợ 2 ngôn ngữ là en và vi")
            session_id = environ['request']['session_id']
        except KeyError:
            return self.error.authen_error()
        try:
            self.u.get('session_id', super_column=session_id)
        except (NotFoundException, InvalidRequestException):
            return self.error.authen_error()
        results = self._levels(lang)
        if results == 404:
            return self.error.not_found("Cấu hình hệ thống sai")
        xml = ['<level name="%s"/>' % result for result in results]
        return '\n\t'.join(xml)
    
    def lessons(self, environ):
        try:
            level = environ['request']['level']
            lang = environ['request']['lang']
            if lang not in ('en', 'vi'):
                return self.error.param_error("Hệ thống chỉ hỗ trợ 2 ngôn ngữ là en và vi")
            session_id = environ['request']['session_id']
        except KeyError:
            return self.error.authen_error()
        try:
            self.u.get('session_id', super_column=session_id)
        except (NotFoundException, InvalidRequestException):
            return self.error.authen_error()
        results = self._lessons(level, lang)
        if results == 404:
            return self.error.not_found("Cấu hình hệ thống sai")
        xml = ['<lesson name="%s"/>' % result for result in results]
        return '\n\t'.join(xml)
        
    def listen(self, environ):
        try:
            level = environ['request']['level']
            lang = environ['request']['lang']
            if lang not in ('en', 'vi'):
                return self.error.param_error("Hệ thống chỉ hỗ trợ 2 ngôn ngữ là en và vi")
            lesson = environ['request']['lesson']
            session_id = environ['request']['session_id']
        except KeyError:
            return self.error.authen_error()
        try:
            self.u.get('session_id', super_column=session_id)
        except (NotFoundException, InvalidRequestException):
            return self.error.authen_error()
        results = self._listen(level, lesson, lang)
        if results == 404:
            return self.error.not_found("Cấu hình hệ thống sai")
        xml = ['<audio title="%s" description="%s" link="%s"/>' \
               % (x['title'], x['description'], audio_url_prefix + x['audio_file']) \
               for x in results]
        return '\n\t'.join(xml)
    
if __name__ == '__main__':
    c = Course()
    c.refresh()
##    print c._levels()
#    print '-' * 80
##    print c._lessons('2. Elementary')
#    print '-' * 80
#    print c._audio('2. Elementary', 'Lesson 01 - Nice to meet you!')
    environ = {}
    environ['request'] = {}
    environ['request']['level'] = '2. Elementary'
    environ['request']['lang'] = 'en'
    environ['request']['lesson'] = 'Lesson 01 - Nice to meet you!'
    print c.listen(environ)