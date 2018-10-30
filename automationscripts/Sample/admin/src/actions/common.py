#coding:utf-8
'''
Created on Oct 30, 2018

@author: lijunlei
'''
class IDict(dict):
    '''
    重写dict __getattr__方法实现通过获取attribute的方式检索dict中的数据。
    egg: 
        src_dict={
            "a":1,
            "b":{
                "c":2,
                "d":[3,4]
                }
            }
    获取 "a"的值            -->  src_dict.a      等同于 src_dict["a"]
    获取 "c"的值            -->  src_dict.b.c    等同于 src_dict["b"]["c"]
    获取 "d"的值中第一个值    -->  src_dict.b.d._0 等同于 src_dict["b"]["d"][0]
    '''
    def __getattr__(self,key):
        value=self[key]
        if isinstance(value, dict):
            return IDict(value)
        elif isinstance(value, list):
            return IList(value)
        else:
            return value

class IList(list):
    '''
    重写list __getattr__方法实现通过获取attribute的方式检索list中的数据。
    egg:
        src_list= ["a","b",1]
        获取"a"  --> src_list._0 等同于src_list[0]
    '''
    def __getattr__(self,index):
        value=self[int(index[1:])]
        if isinstance(value, dict):
            return IDict(value)
        elif isinstance(value, list):
            return IList(value)
        else:
            return value
        
class RequestError(Exception):
    '''request error'''

class JsonValueError(Exception):
    '''Json value error'''