#-*- encoding: utf-8 -*-
"""
html_util.py
Created on 2018/9/1 21:24
Copyright (c) 2018/9/1.
@author: ogc
"""
import urllib
class HtmlUtil:
    #获取字符编码集，默认utf-8
    def get_doc_charset(self,doc):
        charset='utf-8'
        meta=doc.xpath('//meta[@charset]')
        if meta and len(meta)>0:
            charset=meta[0].attrib.get('charset',charset)
        else:
            meta=doc.xpath("//meta[@http-equiv='Content-Type']")
            if meta and len(meta)>0:
                content=meta[0].attrib.get('content','')
                if content:
                    p=content.find('charset=')
                    if p>0:
                        charset=content[p+len('charset='):]
        return charset
    #这个是获取父路径？？
    def get_dom_parent_xpath(self,dom):
        parents=[]
        p=dom
        while True:
            if p is None:
                break
            parents.append(p)
            if p.attrib.get('id',None):
                break
            p=p.getparent()
        xpath=['/']
        for p in reversed(parents):
            id_name=p.attrib.get('id',None)
            class_name=p.attrib.get('class',None)
            if id_name:
                xpath.append('/')
                xpath.append(p.tag)
                xpath.append('[@id=\'')
                xpath.append(id_name)
                xpath.append('\']')
            elif class_name:
                xpath.append('/')
                xpath.append(p.tag)
                xpath.append('[contains(@class,\'')
                xpath.append(class_name)
                xpath.append('\']')
            else:
                xpath.append('/')
                xpath.append(p.tag)
        return "".join(xpath)
    #方法待定
    def get_dom_parent_xpath_js(self,dom):
        parents=[]
        p=dom
        while True:
            if p is None:
                break
            parents.append(p)
            if p.get('id',None):
                break
            p=p.parent
        xpath=['/']
        for p in reversed(parents):
            id_name=p.get('id',None)
            class_name=p.get('class',None)
            if id_name:
                xpath.append('/')
                xpath.append(p.name)
                xpath.append('[@id=\'')
                xpath.append(id_name)
                xpath.append('\']')
            elif class_name:
                xpath.append('/')
                xpath.append(p.name)
                xpath.append('[contains(@class,\'')
                xpath.append(class_name[0])
                xpath.append('\')]')
            else:
                xpath.append('/')
                xpath.append(p.name)
        return "".join(xpath)
    #从完整的url路径中切分出域名，如：实例结果为：www.baidu.com
    def get_url_host(self,url):
        s1=urllib.splittype(url)[1]
        return urllib.splithost(s1)[0]

if __name__=='__main__':
    f=HtmlUtil()
    print f.get_url_host("http://www.autohome.com.cn/all")
    print f.get_url_host("https://topic.autohome.com.cn/new/marketing/2018/3/qx60")
    from tld import get_fld
    a=get_fld("http://www.autohome.com.cn/all")
    b=get_fld("https://topic.autohome.com.cn/new/marketing/2018/3/qx60")
    print a,b,a==b
    # print f.get_dom_parent_xpath_js("这里的参数是dom")

