#!/usr/bin/env python
#! coding: utf-8
from commands import getoutput
from os import system as run
from os.path import dirname
from shutil import move
from lib.text_processing import get_text
from lib.cache import KeyValueDatabase
from settings import api_ports, files_dir,\
                     cassandra_log_file, \
                     cassandra_commit_log_directory, \
                     cassandra_data_file_directory, \
                     redis_backup_dir


R = KeyValueDatabase()
    

def _start_cassandra():
    cmd = 'bin/cassandra/bin/cassandra &'
    run(cmd)
    print 'Cassandra started.'

def _start_redis():
    cmd = 'bin/redis/redis-server bin/redis/redis.conf &'
    run(cmd)
    print 'Redis started.'
    
def _start_controller():
    for port in api_ports:
        cmd = 'python controller.py ' + str(port) + ' &' 
        print "MEL's API Server listening on port %d" % port
        run(cmd)
        
def _start_nginx():
    cmd = 'bin/nginx/sbin/nginx &'
    run(cmd)
    print 'Load Balancer started'

def _update_nginx_config():
    conf = open('bin/nginx/conf/nginx.conf').read()
    
    # change root files folder
    s = get_text('root ', ';', conf)[0]
    conf = conf.replace(s, dirname(files_dir))
    
    # change frontendports
    s = get_text('upstream backends {', '}', conf)[0]
    
    ## generate new config string
    _s = 'server 127.0.0.1:%s;\n\t'
    new_backends = '\n\t'
    for port in api_ports:
        new_backends = new_backends + _s % port
    
    conf = conf.replace(s, new_backends)
    
    # backup old config
    move('bin/nginx/conf/nginx.conf', 'bin/nginx/conf/nginx.conf.bak')
    
    # write new config
    f = open('bin/nginx/conf/nginx.conf', 'w')
    f.write(conf)    
    
def _update_cassandra_config():
    #----- change log4j config -----
    conf = open('bin/cassandra/conf/log4j.properties').read()
    
    s = get_text('log4j.appender.R.File=', '\n', conf)[0]
    conf = conf.replace(s, cassandra_log_file)
    
    #backup old config
    move('bin/cassandra/conf/log4j.properties', 'bin/cassandra/conf/log4j.properties.bak')
    
    # write new config
    f = open('bin/cassandra/conf/log4j.properties', 'w')
    f.write(conf)
    
    #----- change cassandra config -----
    conf = open('bin/cassandra/conf/storage-conf.xml').read()
    s = get_text('<CommitLogDirectory>', '</CommitLogDirectory>', conf)[0]
    conf = conf.replace(s, cassandra_commit_log_directory)
    
    s = get_text('<DataFileDirectory>', '</DataFileDirectory>', conf)[0]
    conf = conf.replace(s, cassandra_data_file_directory)
    
    #backup old config
    move('bin/cassandra/conf/storage-conf.xml', 'bin/cassandra/conf/storage-conf.xml.bak')
    
    # write new config
    f = open('bin/cassandra/conf/storage-conf.xml', 'w')
    f.write(conf)

def _update_redis_config():
    conf = open('bin/redis/redis.conf').read()

    s = get_text('dir ', '\n', conf)[0]
    conf = conf.replace(s, redis_backup_dir)
    
    #backup old config
    move('bin/redis/redis.conf', 'bin/redis/redis.conf.bak')
    
    # write new config
    f = open('bin/redis/redis.conf', 'w')
    f.write(conf)
    
def _kill(s):
    cmd = 'ps aux | grep %s' % s
    output = getoutput(cmd)
    lines = output.split('\n')
    for line in lines:
        if 'grep' not in line:
            params = line.split()
            pid = params[1]
            run('kill -9 %s' % pid)
    
def start():
    _update_nginx_config() 
    _update_cassandra_config()
    _update_redis_config()
    _start_cassandra()
    _start_redis()
    _start_controller()
    _start_nginx()

def reload(s='controller.py'):
    print 'Restarting load balancer...'
    _update_nginx_config()
    run('bin/nginx/sbin/nginx -s reload')
    print 'Reload Loadbalancer: Done'
    
    cmd = 'ps a | grep %s' % s
    output = getoutput(cmd)
    lines = output.split('\n')
    for line in lines:
        if 'grep' in line:
            continue
        params = line.split()
        pid = params[0]
        port = params[-1]
        # kill one process
        run('kill -9 %s' % pid)
        run('python controller.py %s &' % port)
        print 'Restart worker listen on %s: Done!' % port
    
        
def refresh():
    R.flush()
    print 'Refresh done!'

def stop():
    _kill('cassandra')
    _kill('redis-server')
    _kill('nginx')
    _kill('controller.py')
    print 'Done!'
    
    
    
if __name__ == '__main__':
    import sys
    try:
        action = sys.argv[1]
        if action == 'refresh':
            refresh()
        elif action == 'start':
            start()
        elif action == 'stop':
            stop()
        elif action == 'reload':
            reload()
        else:
            print """
            Sử dụng: 
                
                python server_controller.py start | stop | reload | refresh
            
            Các tham số:
                * start: khởi động hệ thống
                * stop: dừng toàn bộ hệ thống
                * reload: cập nhật source code mới (các thông số cấu hình không ảnh hưởng)
                * refresh: xóa cache
            
            Vui lòng chạy server_controller duới quyền root.
            """
    except:
        print 'use: python server_controller.py start | stop | reload | refresh'
        sys.exit()