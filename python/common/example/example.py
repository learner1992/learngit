#-*- encoding: utf-8 -*-
"""
example.py
Created on 2018/9/2 23:37
Copyright (c) 2018/9/2.
@author: ogc
"""
import mx.URL,sys,re
from tld import get_tld,get_fld
from bs4 import BeautifulSoup
from python.common.util.request_util import RequestUtil
from python.common.util.html_util import HtmlUtil
from python.common.util.util import Util
from lxml import etree

def test_beautiful():
    # url='http://roll.news.qq.com'
    url='http://www.baidu.com'
    # url='http://roll.mil.news.sina.com.cn/col/zgjq/index/shtml'

    r=RequestUtil()
    hu=HtmlUtil()
    html=r.http_get_phandomjs(url)
    print get_title(html)
    # domain=get_tld(url)
    domain=get_fld(url)
    host=hu.get_url_host(url)
    u=Util()
    print "domain:",domain,":host:",host
    soup=BeautifulSoup(html,'lxml')

    print hu.get_doc_charset(etree.HTML(html)),"###################3"
    a_docs=soup.find_all("a")
    for a in a_docs:
        a_href=get_format_url(url,a,host)
        if a.text:
            print a.text
        if a_href:
            xpath=hu.get_dom_parent_xpath_js(a)
            print a_href,'_',xpath,u.get_md5(xpath)


def get_format_url(url, a_doc, host):
    a_href = a_doc.get('href')
    try:
        if a_href is not None and a_href.__len__() > 0:
            a_href = str(a_href).strip()
            a_href = a_href[:a_href.index('#')] if a_href.__contains__('#') else a_href
            # a_href = a_href.encode('utf8')
            # a_href = urllib.quote(a_href,safe='.:/?&=')
            if a_href.startswith('//'):
                url = 'https:' + a_href if url.startswith('https:') else 'http:' + a_href
                url = mx.URL.URL(str(url))
                a_href = url.url
            elif a_href.startswith('/'):
                url = 'https://' + host + a_href if url.startswith('https:') else 'http://' + host + a_href
                url = mx.URL.URL(str(url))
                a_href = url.url
            elif a_href.startswith('./') or a_href.startswith('../'):
                url = mx.URL.URL(str(url) + '/' + a_href)
                a_href = url.url
            elif not a_href.startswith('javascript') and not a_href.startswith('mailto') and not a_href.startswith(
                    'http') and a_href != '':
                url = 'https://' + host + '/' + a_href if url.startswith('https:') else 'http://' + host + '/' + a_href
                url = mx.URL.URL(str(url))
                a_href = url.url
            a_href = a_href[:-1] if a_href.endswith('/') else a_href
            # a_href = a_href.lower()
        get_tld(a_href)
    except:
        return ''

    if not a_href.startswith('http'):
        return ''
#这里是对后面的参数排序，进行归一化
    if a_href.__contains__('?'):
        a_params_str = a_href[a_href.index('?') + 1:]
        a_params = a_params_str.split('&')
        a_params.sort()
        a_params_str = '&'.join(a_params)
        a_href = a_href[:a_href.index('?') + 1] + a_params_str

    return a_href
def get_title(Html):
    '''
    用re抽取网页Title
    '''
    # Html = utf8_transfer(Html)
    compile_rule = ur'<title>.*</title>'
    title_list = re.findall(compile_rule, Html)
    if title_list == []:
        title = ''
    else:
        title = title_list[0][7:-8]
    return title

if __name__=="__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    # print get_title("https://blog.csdn.net/zmx729618/article/details/54093532")
    test_beautiful()


