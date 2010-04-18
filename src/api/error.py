#!/usr/bin/env python
#! coding: utf-8

class Error:
    def __init__(self):
        pass
    
    def bad_request(self, description="Yêu cầu không hợp lệ"):
        xml = """<error status_code="400" description="%s"/>""" % description
        return xml
    
    def not_found(self, description="Page not found"):
        xml = """<error status_code="404" description="%s"/>""" % description
        return xml
    
    def param_error(self, description="Tham số không hợp lệ"):
        xml = """<error status_code="406" description="%s"/>""" % description
        return xml
    
    def authen_error(self, description="session_id không hợp lệ"):
        xml = """<error status_code="401" description="%s"/>""" % description
        return xml
    
    def trial_expired(self, description="Thời hạn dùng thử đã hết"):
        xml = '<error status_code="402" description="%s"/>' % description
        return xml