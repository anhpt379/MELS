#! coding: utf-8
"""
AoiRadio Server-side System
===========================
    * Description: Server-side of AoiRadio - 
                            An Interactive Radio and Music Recommender System
    * Created on: Mar 2, 2010
    * Author: AloneRoad 
"""
# pylint -disable-msg:C0103
""" Kết nối đến ApiServer, ngừng dịch vụ, lấy mã nguồn mới từ Subversion
Server về, cài đặt rồi khởi chạy lại.
"""
from lib import ssh

private_key = "id_rsa"
remote = ssh.Connection('3.3.3.60', 'root', private_key)

def resetApiServer():
    """ Shutdown API Server, get latest source code, install and re-run """
    for line in remote.execute("ps xa | grep python"):
        fields  = line.split()
        pid     = fields[0]
        path = fields[5] 
                                                                                
        if path.find('updateApiServer.py') == -1: # except itself
            remote.execute('kill -9 %s' % pid)                                  
            print 'Killed %s.' % path                                                        
                                                    
    print "Downloading latest source code..."
    cmd = 'svn co svn://3.3.3.50:9629/AoiRadio /srv/www/AoiRadio'
    remote.execute(cmd)
                                                                                                  
    # Install new version
    print 'Install new source code...'
    remote.execute('cd /srv/www/AoiRadioProject')
    remote.execute('python setup.py install')
                                                          
    # Restart the process
    print 'Starting API Handler...'
    ports = (8000, 8001, 8002, 8003)
    for port in ports:                                                        
        print 'Listen on port %d\t' % port,
        cmd = 'python /srv/www/AoiRadioProject/APIHandler.py %d &' % port
        remote.run(cmd)
        print 'Done'                                                                    
    print 'Update done!'    
                                                                          
if __name__ == '__main__':
    resetApiServer()         