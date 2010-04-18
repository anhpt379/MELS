==================
MEL's API Document
==================

    Copyright 2010 VinhCom Corp,. All rights reserved.

    :Mô tả: Mobile English Learning
    :Phiên bản: 0.9.1
    :Người soạn: Phạm Tuấn Anh


.. contents:: **Nội dung tài liệu**
    :depth: 2
    :backlinks: top


What's new?
===========
 
    * Sử dụng định dạng XML cho toàn bộ dữ liệu trả về
    
    * Tất cả từ khóa sử dụng tiếng Anh, chữ thường, có gạch dưới phân cách từ 
    
    * Thuộc tính ``status_code`` có trong mọi lời trả về
    
    * Tham số ``api_key`` có trong mọi lời yêu cầu
    
    * Sử dụng ký tự ``:`` để phân cách phần phương thức và các tham số 
      Sử dụng ký tự ``&`` để phân cách giữa các tham số
      Giá trị của các tham số được đặt trong cặp ký tự ``'`` hoặc ``"``
      
 
Change logs
===========


Tổng quan
=========

* MEL API có thể truy cập tại địa chỉ: http://192.168.1.104/
* Định dạng trả về: `XML <http://en.wikipedia.org/wiki/XML>`_



Status Codes
============

    **Thông tin**:

        * ``200 OK``: Thao tác thực hiện thành công
        
        * ``201 Created``: Tài khoản đã được tạo
        
        * ``202 Accepted``: Đăng nhập thành công
        
        * ``204 No Content``: Không có kết quả nào
        
        * ``302 Found``: Dữ liệu kiểm tra có trong CSDL
            
        * ``304 Not Modified``: Không có dữ liệu nào mới.
    
        
    **Lỗi phía Client 4xx**:
    
        * ``400 Bad Request``: Yêu cầu không hợp lệ
            
        * ``401 Unauthorized``: Thiếu mã xác thực hoặc mã xác thực không đúng
            
        * ``402 Payment Required``: Thời gian dùng thử đã hết. Vui lòng nâng cấp tài khoản để tiếp tục sử dụng.
        
        * ``403 Forbidden``: Yêu cầu đúng, nhưng bị từ chối. Thuộc tính `description` trong nội dung trả về sẽ mô tả chi tiết hơn. Thông thường mã lỗi này xuất hiện là do số yêu cầu vượt quá giới hạn cho phép 
        
        * ``404 Not Found``: Phương thức này không tồn tại.
                
        * ``405 Method Not Allowed``: Phương thức này không được hệ thống hỗ trợ
            
        * ``406 Not Acceptable``: Giá trị của một/một vài tham số không hợp lệ.
        
        * ``409 Conflict``: File upload trùng với một file đã có trên hệ thống
    

    **Lỗi phía Server 5xx**:
    
        * ``500 Internal Server Error``: Hệ thống gặp phải một lỗi không rõ nguyên nhân. Vui lòng báo lại cho bộ phận quản trị để xử lý vấn đề này.  
        
        * ``502 Bad Gateway``: Server ngừng hoạt động hoặc đang được nâng cấp
        
        * ``503 Service Unavailable``: Server đang hoạt động nhưng quá tải. Vui lòng thử lại sau. 
            
        
    
API Key
=======

    * Đăng ký một API key
 
    * Cấu hình tài khoản của bạn
        - Tổng số lượt yêu cầu/ngày: 
        - Khoảng cách giữa 2 lần yêu cầu (ms):
    * API mặc định dành cho các phiên bản di động là: ``c74df88f0b1db2e4f48fdc4903851d41``  
            (không giới hạn tổng số lượt yêu cầu và khoảng thời gian trễ giữa 2 lần yêu cầu)

Những phần chung
================

Định dạng trả về
----------------
    .. code-block:: xml
        
        <?xml version="1.0" encoding="utf-8"?>
        <api version="0.9.1" last_update="06-04-2010">Nội dung trả về</api>

    .. note:: 
        
        * Giá trị của thuộc tính ``version`` và ``last_update`` có thể sẽ khác ở trên
        * ``Nội dung trả về`` sẽ thay đổi tùy từng trường hợp cụ thể
 
    Ví dụ:
    
    .. code-block:: xml
        
        <?xml version="1.0" encoding="utf-8"?>
        <api version="0.9.1" last_update="06-04-2010">
            <error status_code="400" description="Yêu cầu không hợp lệ"/>
        </api>
    

Thông báo lỗi
-------------
    Những thông báo dưới đây có thể gặp trong bất cứ yêu cầu nào được hệ thống hỗ trợ. Các lỗi này sẽ không đề cập đến trong những phần sau nhưng được coi như sẽ xuất hiện trong mọi trường hợp.

    .. code-block:: xml
        
        <error status_code="400" description="Yêu cầu không hợp lệ"/>
    
    .. code-block:: xml
               
        <error status_code="401" description="api_key không hợp lệ"/>
   
    .. code-block:: xml
    
        <error status_code="403" description="api_key này chỉ được phép sử dụng %s lần một ngày"/>
   
    .. code-block:: xml
    
        <error status_code="403" description="Khoảng thời gian tối thiểu giữa 2 lần request phải lớn hơn %s mili-giây"/>
   
    .. code-block:: xml
        
        <error status_code="405" description="Phương thức này không được hệ thống hỗ trợ"/>
        
    .. code-block:: xml
    
        <error status_code="500" description="Hệ thống gặp một lỗi chưa rõ nguyên nhân. Vui lòng báo lại cho bộ phận quản trị nếu gặp thông báo này"/>
   

Nhóm xác thực
=============
    
Đăng ký
-------

    * **Mẫu yêu cầu**:
        .. code-block:: sql
            
            register:username="foo"&password="bar"&phone_number="foobar"&api_key="fubar"
            
    * **Các tham số**:
        - ``username``: tên đăng nhập
        - ``password``: mật khẩu đăng nhập (phía client phải mã hóa md5 trước khi gửi lên
        - ``phone_number``: số điện thoại đang dùng
        - ``api_key``: api_key được server cung cấp
        
    * **Xác thực**: không yêu cầu
    
    * **Phương thức**: ``HTTP GET``
    
    * **Trả lời**:
        .. code-block:: xml
            
            <register status_code="201" description="Đăng ký thành công"/>
     
    * **Các trường hợp lỗi**:
            .. code-block:: xml
                          
               <error status_code="406" description="Tham số không hợp lệ"/>
            
            .. code-block:: xml
                          
               <error status_code="406" description="Tên đăng nhập chỉ được dùng các ký tự a-z, A-Z và .-_@"/>
            
            .. code-block:: xml
                          
               <error status_code="406" description="Mật khẩu phải được mã hóa md5 trước khi gửi lên"/>
               
            .. code-block:: xml
                          
               <error status_code="406" description="phone_number không hợp lệ"/>
            
            .. seealso::
                `Các thông báo lỗi chung <#cac-thong-bao-loi-chung>`_
               
Đăng nhập
---------

    * **Mẫu yêu cầu**:
        .. code-block:: sql
            
            login:username="foo"&password="bar"&api_key="foobar"
            
    * **Các tham số**:
        - ``username``: tên đăng nhập
        - ``password``: mật khẩu đăng nhập (phía client phải mã hóa md5 trước khi gửi lên
        - ``api_key``: api_key được server cung cấp
        
    * **Xác thực**: không yêu cầu
    
    * **Phương thức**: ``HTTP GET``
    
    * **Trả lời**:
        .. code-block:: xml
            
            <login session_id="foobar" status_code="202" description="Đăng nhập thành công"/>
    
        .. note:: ``session_id`` là một chuỗi gồm 32 ký tự và thay đổi mỗi lần đăng nhập      
    
    * **Các trường hợp lỗi**:
            .. code-block:: xml
            
                <error status_code="401" description="Tên đăng nhập/mật khẩu không hợp lệ"/>
                  
            .. code-block:: xml
            
                <error status_code="402" description="Thời gian dùng thử đã hết"/>
                  
            .. seealso::
                `Các thông báo lỗi chung <#cac-thong-bao-loi-chung>`_
        
Đăng xuất
---------

    * **Mẫu yêu cầu**: 
        .. code-block:: sql
    
            logout:session_id="foo"&api_key="foobar"
    
    * **Các tham số**:
        - ``session_id``: được trả về khi đăng nhập thành công
        - ``api_key``: server cung cấp
    
    * **Xác thực**: yêu cầu đã đăng nhập
    
    
    * **Phương thức**: ``HTTP GET``
    
    * **Trả lời**:
        .. code-block:: xml
    
            <logout status_code="200" description="Đăng xuất thành công"/>
        
    * **Các trường hợp lỗi**:
            .. code-block:: xml
        
                <error status_code="401" description="session_id không hợp lệ"/>
       
            .. seealso::
                `Các thông báo lỗi chung <#cac-thong-bao-loi-chung>`_


Kích hoạt tài khoản
-------------------


Lấy mã kích hoạt mới (dành cho bộ phận quản trị)
------------------------------------------------


                
Nhóm từ điển
============

Tra cứu
-------
    Hiện tại hệ thống hỗ trợ 3 loại từ điển là từ điển Anh-Việt, từ điển Việt-Anh và từ điển Anh-Anh
    
    * **Mẫu yêu cầu**:
        .. code-block:: sql
            
            lookup:keyword="foo"&session_id="bar"&api_key="foobar"
    
    * **Các tham số**:
        
        - ``keyword``: từ muốn tra
        - ``session_id``: session_id nhận được sau khi đăng nhập thành công
        - ``api_key``: được phía server cung cấp
        
    * **Xác thực**: yêu cầu đã đăng nhập
    
    * **Phương thức**: ``HTTP GET``
    
    * **Trả lời**:
        .. code-block:: xml
            
            <lookup status_code="200" description="baz" keyword="foo" mean="bar" spell="foobar"/>
        
        .. note::
            
            * ``keyword``: từ đuợc tra
            * ``mean``: nghĩa của từ được tra
            * ``spell``: phiên âm quốc tế của từ được tra       
            * Giá trị của thuộc tính keyword, mean, spell sẽ thay đổi tùy từng yêu cầu
    
    * **Các trường hợp lỗi**:
        .. code-block:: xml
            
            <error status_code="404" description="Từ khóa bạn tìm không có trong từ điển"/>
            

Nhóm bài giảng
==============
Danh sách các mức trình độ
--------------------------
    
    * **Mẫu yêu cầu**:
        .. code-block:: sql
        
            levels:lang="foo"&session_id="bar"&api_key="foobar"
    
    * **Các tham số**:
        
        - ``lang``: là ``en`` hoặc ``vi``
        - ``session_id``: session_id nhận được sau khi đăng nhập thành công
        - ``api_key``: server cung cấp
    
    * **Xác thực**: yêu cầu đã đăng nhập
    
    * **Phương thức**: ``HTTP GET``
    
    * **Trả lời**: 
        .. code-block:: xml
        
            <level name="foo"/>
            <level name="bar"/>
            ...
        
        .. note:: 
            
            * giá trị ``foo`` và ``bar`` sẽ thay đổi tùy thuộc vào nội dung biên tập
            * số ``<level name="foobar"/>`` cũng sẽ phụ thuộc vào quá trình phân loại của bộ phận nội dung      
    
    * **Các trường hợp lỗi**:
        .. code-block:: xml
            
            <error status_code="401" description="session_id không hợp lệ"/>
        
        .. code-block:: xml
            
            <error status_code="404" description="Cấu hình hệ thống sai"/>

Danh sách các bài học
---------------------
    
    * **Mẫu yêu cầu**:
        .. code-block:: sql
        
            lessons:lang="foo"&level="baz"&session_id="bar"&api_key="foobar"
    
    * **Các tham số**:
        
        - ``lang``: là ``en`` hoặc ``vi``
        - ``level``: tên level người dùng chọn
        - ``session_id``: session_id nhận được sau khi đăng nhập thành công
        - ``api_key``: server cung cấp
    
    * **Xác thực**: yêu cầu đã đăng nhập
    
    * **Phương thức**: ``HTTP GET``
    
    * **Trả lời**: 
        .. code-block:: xml
        
            <lesson name="foo"/>
            <lesson name="bar"/>
            ...
        
        .. note:: 
            
            * giá trị ``foo`` và ``bar`` sẽ thay đổi tùy thuộc vào nội dung biên tập
            * số ``<lesson name="foobar"/>`` cũng sẽ phụ thuộc vào quá trình phân loại của bộ phận nội dung      
    
    * **Các trường hợp lỗi**:
        .. code-block:: xml
            
            <error status_code="401" description="session_id không hợp lệ"/>
        
        .. code-block:: xml
            
            <error status_code="404" description="Cấu hình hệ thống sai"/>           


Nghe bài giảng
--------------
    
    * **Mẫu yêu cầu**:
        .. code-block:: sql
        
            listen:lang="foo"&level="baz"&lesson="fu"&session_id="bar"&api_key="foobar"
    
    * **Các tham số**:
        
        - ``lang``: là ``en`` hoặc ``vi``
        - ``level``: tên level người dùng chọn
        - ``lesson``: bài học người dùng ch
        - ``session_id``: session_id nhận được sau khi đăng nhập thành công
        - ``api_key``: server cung cấp
    
    * **Xác thực**: yêu cầu đã đăng nhập
    
    * **Phương thức**: ``HTTP GET``
    
    * **Trả lời**: 
        .. code-block:: xml
        
            <audio title="foo" description="bar" link="foobar"/>
            <audio title="fu" description="baz" link="fubaz"/>
            ...
        
        .. note:: 
            
            * giá trị của các thuộc tính ``title``, ``description``, ``link`` sẽ thay đổi tùy thuộc vào nội dung biên tập
            * số thẻ ``<audio/>`` cũng sẽ phụ thuộc vào quá trình phân loại của bộ phận nội dung      
    
    * **Các trường hợp lỗi**:
        .. code-block:: xml
            
            <error status_code="401" description="session_id không hợp lệ"/>
        
        .. code-block:: xml
                
            <error status_code="404" description="Cấu hình hệ thống sai"/>  


 
        