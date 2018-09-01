#-*- encoding: utf-8 -*-
"""
file_util.py
Created on 2018/9/1 21:14
Copyright (c) 2018/9/1.
@author: ogc
"""
import os
import content
class FileUtil:
    #判断路径是否存在，否则创建新路径
    def create_path(self,path):
        if not os.path.exists(path):
            os.makedirs(path)
    #覆盖写入文件
    def write_file_line_pattern(self,path,dataList,pattern='w'):
        f=file(path,pattern)
        for data in dataList:
            line=data.__str__()+content._SEQ2
            f.write(line)
        f.close()
    #覆盖写入文件
    def write_file_line(self,path,dataList):
        self.write_file_line_pattern(path,dataList)
    #写入单条记录
    def write_file_content_pattern(self,path,content,pattern='w'):
        f=file(path,pattern)
        f.write(content)
        f.close()
    #
    def write_file_content(self,path,content):
        self.write_file_content_pattern(path,content)
    #读文件，每行换行符替换,读出来的汉字是unicode
    def read_file(self,path):
        list=[]
        f=file(path)
        while True:
            line=f.readline()
            if len(line)==0:
                break
            list.append(line.replace('\n','').replace('\r\n',''))
        f.close()
        return list

if __name__=='__main__':
    f=FileUtil()
    list=f.read_file("D:\\1.txt")
    print list
