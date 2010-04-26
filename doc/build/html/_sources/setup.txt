==============================================
Hướng dẫn cài đặt trên Server CentOS 5.4 32bit
==============================================

Cài đặt server
==============

    * Chuyển boot level về 3
        1. Sửa cấu hình khởi động ở file ``inittab``: ``vim /etc/inittab`` 
        2. Chuyển  ``id:5:initdefault:`` thành ``id:3:initdefault:``
        3. Khởi động lại server: ``reboot``
       
    * Hạn chế các dịch vụ thừa khởi chạy cùng hệ thống
        Gõ ``setup``, vào ``System Services``
            Chỉ kích hoạt các dịch vụ sau:    
                * auditd
                * crond
                * iptables
                * kudzu
                * network
                * restorecond
                * sshd
                * syslog
                * microcode_ctl (not AMD machines only)
                * irqbalance (if multiple cores, multiple processors, hyperthreading
            
    * Kích hoạt ``Firewall configuration`` > ``Customize`` và mở 2 cổng HTTP và SSH     
        

Cấu hình đăng nhập
==================

    * sao chép file id_rsa.pub từ máy điều khiển vào thư mục /root/.ssh/ trên server sử dụng rsync::
            
            rsync -v -e ssh /home/AloneRoad/.ssh/id_rsa.pub root@203.128.246.61:~/.ssh/
    
    * đăng nhập server và thực hiện lệnh sau::
            
            cd /root/.ssh/
            cat id_rsa.pub >> authorized_keys
            
    * sau khi thực hiện xong bạn có thể vô hiệu hóa hình thức đăng nhập server bằng mật khẩu để tăng tính bảo mật
    

Cài đặt Python 2.6.x
====================
    
    * Chuẩn bị::
        
        rpm -Uvh http://yum.chrislea.com/centos/5/i386/chl-release-5-3.noarch.rpm
        rpm -Uvh http://download.fedora.redhat.com/pub/epel/5/i386/epel-release-5-3.noarch.rpm
        rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-CHL

        yum groupinstall -y 'Development Tools'
        yum install -y openssl-devel* zlib*
        
        
    * Cài đặt Python 2.6::
    
        * Tải mã nguồn mới nhất về::
            
            cd /usr/local/src
            wget 
            tar zxvf
        
        * Build và cài đặt::
            
            ./configure --prefix=/opt/python2.6 --with-threads --enable-shared
            make
            make install
        
        * Cấu hình::
        
            vim /root/.bash_profile
        
            #Chèn vào phần cuối của file
                alias python='/opt/python2.6/bin/python'
                alias python2.6='/opt/python2.6/bin/python'
                PATH=$PATH:/opt/python2.6/bin
            
            cat >> /etc/ld.so.conf.d/opt-python2.6.conf
            # gõ vào
                /opt/python2.6/lib 
            # và nhấn 'enter'
            # sau đó nhấn 'ctrl+d'
            ldconfig
            
            chmod -R a+w /opt/python2.6/bin/
            
            cd /opt/python2.6/lib/python2.6/config
            ln -s ../../libpython2.6.s
    
        * Lưu và thoát:: ``ESC`` + ``:wq!``
        #yum install -y python26 python26-devel
    
    * alias python=/usr/bin/python26
    
    * Cài đặt các thư viện bổ sung::
        
        * paramiko::
    
            easy_install paramiko
        
        * hashlib (for python 2.4)
        * simplejson (for python2.4)
        * email
        * functools
        
        
    * Cài đặt java::
        
        yum install -y java
    
    * Cài đặt Git::
        
        yum install -y git        