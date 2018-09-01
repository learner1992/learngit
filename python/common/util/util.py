#-*- encoding: utf-8 -*-
"""
util.py
Created on 2018/8/31 20:11
Copyright (c) 2018/8/31.
@author: ogc
"""
import hashlib,json,uuid

class Util:
    def get_dict_value(self,data,key):
        if data=="":
            data={}
        if data.has_key(key):
            return data[key]
        else:
            return None
    def quotes(self,str):
        return str.replace('\"','\'').replace('\\','')
    def get_local_ip(self):
        import platform
        plat=platform.system()
        ip=None
        if plat=='Windows' or plat=='Darwin':
            import socket
            ip=socket.gethostbyname(socket.gethostname())
        elif plat=='Linux':
            import socket,fcntl,struct
            s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            ip=socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s','enp4s0f1'[:15]))[20:24])
        return ip
    def get_md5(self,str):
        md5=hashlib.md5()
        md5.update(str)
        md5=md5.hexdigest()
        return md5
    def get_uuid(self,value,namespace=uuid.NAMESPACE_URL):
        UUID_SHA=uuid.uuid5(namespace,value)
        return str(UUID_SHA)
    def get_json_dict(self,str):
        rs=True
        try:
            rs=json.load(str)
        except:
            rs=False
        return rs

if __name__=="__main__":
    pass