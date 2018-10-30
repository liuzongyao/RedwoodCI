#coding:UTF-8

import os
import requests
from requests.models import Response
import dpath.util
import copy
from common import IDict,JsonValueError,RequestError

class Sender():
    
    def __init__(self):
        '''
        需提前在本脚本文件所在路径下创建data目录
        '''
        self.__data_dir = os.path.dirname(os.path.abspath(__file__))+"/data/"
    
    def http_request(self,method,url,params=None,data=None,json=None,headers=None,cookies=None,timeout=None,**kwargs):
        return requests.request(method,url,params=params,data=data,json=json,headers=headers,cookies=cookies,timeout=timeout,**kwargs)
    
    def http_get(self,url,params=None,headers=None,cookies=None,timeout=None,**kwargs):
        return requests.get(url,params=params,headers=headers,cookies=cookies,timeout=timeout,**kwargs)
    
    def http_options(self,url,timeout=None,**kwargs):
        return requests.options(url,timeout=timeout,**kwargs)
    
    def http_head(self,url,timeout=None,**kwargs):
        return requests.head(url,timeout=timeout,**kwargs)
    
    def http_post(self,url,data=None,json=None,headers=None,cookies=None,timeout=None,**kwargs):
        return requests.post(url,data=data,json=json,headers=headers,cookies=cookies,timeout=timeout,**kwargs) 
    
    def http_put(self,url,data=None,json=None,headers=None,cookies=None,timeout=None,**kwargs):
        return requests.put(url, data=data, json=json, headers=headers,cookies=cookies,timeout=timeout,**kwargs)
    
    def http_patch(self,url,data=None,json=None,headers=None,cookies=None,timeout=None,**kwargs):
        return requests.patch(url,data=data,json=json,headers=headers,cookies=cookies,timeout=timeout,**kwargs)
    
    def http_delete(self,url,headers=None,cookies=None,timeout=None,**kwargs):
        return requests.delete(url,headers=headers,cookies=cookies,timeout=timeout,**kwargs)
    
    def http_upload_file(self,url,file_name,headers=None,cookies=None,timeout=None,**kwargs):
        '''
        以流的方式上传文件。
        '''
        with open(self.__data_dir+file_name,'rb') as fp:
            return self.http_post(url, data=fp,headers=headers,cookies=cookies,timeout=timeout,**kwargs)
        
    def read_file(self,file_name):
        '''
        读取文本文件内容。
        arg: [file_name] 文件名称。
        return: 文件内容
        '''
        with open(self.__data_dir+file_name,"r") as fp:
            return fp.read()
        
    def read_byte_file(self,file_name):
        '''
        读取二进制文件内容。
        arg: [file_name] 文件名称。
        return: 二进制文件内容
        '''
        with open(self.__data_dir+file_name,"rb") as fp:
            return fp.read()
    
    def string2json(self,string_data):
        '''
        将string 类型的json转成python dict类型。
        arg: [string_data] string类型的json数据。
        return: python dict.
        '''
        import json
        return json.loads(string_data)
    
    def json2string(self,json_data):
        '''
        将json转成string类型。
        arg: [json_data] python dict 类型的数据
        return: string类型的json
        '''
        import json
        return json.dumps(json_data)
        
    def throw_error_with_response_code(self,response,black_list = [],white_list = []):
        '''
        校验response code是否与预期一致，返回RequestError异常。
        arg: [response] requests.models.Response 类型
        arg: [black_list] 黑名单，当response code 在黑名单中时，返回RequestError异常。
        arg: [white_list] 白名单，当response code 不在白名单时，返回RequestError异常。
        注: 黑名单优先级高于白名单。当黑名单和白名单都有数据时，response code 在黑名单中才会返回RequestError异常。
            当黑名单和白名单都为空时，不做任何处理。
        '''
        if isinstance(response, Response):
            if black_list:
                if response.status_code in black_list:
                    raise RequestError("Request server error. code: [%s] reason: %s"%(response.status_code,response.reason))
            elif white_list:
                if response.status_code not in white_list:
                    raise RequestError("Request server error. code: [%s] reason: %s"%(response.status_code,response.reason))
            else:
                pass
#                raise RequestError("Request server error. code: [%s] reason: %s"%(response.status_code,response.reason))
        else:
            raise AttributeError("parameter 'response' must be Response type.[%s]"%type(response))
    
    def throw_error_with_json_value(self,response,json_path,value):
        '''
        通过 python dpath 库获取response中的值与预期结果进行比较，如不一致，返回JsonValueError异常。
        arg: [response] requests.models.Response 类型
        arg: [json_path] 从response数据中检索value的xpath.
            egg:
                src_data={
                    "a":1,
                    "b":{
                        "c":2,
                        "d":3
                        }
                    }
            检索 "c" --> /b/c
            检索 "a" --> /a
        arg: [value] 预期结果
        '''
        if isinstance(response, Response):
            rep_json = response.json()
            if not dpath.util.get(rep_json,json_path) == value:
                raise JsonValueError("Json value error.[%s]"%dpath.util.get(rep_json,json_path))
        else:
            raise AttributeError("parameter 'response' must be Response type.[%s]"%type(response))
    
    def __reduce_dict(self,dict_data,ret = {}):
        '''
        将多维字典降维到一维字典。
        src_data = {                                  dist_data = {
            "a":1,                                        "a":[1],
            "b":{                                         "c":[2,5],
                "c":2,                                    "d":[3,4,6],
                "d":[                                     "f":[7]
                    3,                                }
                    4                                 
                    ]                                 
                }                                     
            "e":[                  -->                
                {                                     
                    "c":5,                            
                    "d":6                             
                    },                                
                {                                     
                    "f":7                             
                    }                                 
                ]                                     
            } 
            
        arg: [dict_data] 要进行降维的dict对象。
        arg: [ret] 降维后的数据存放dict对象。
        return : 返回降维后的dict对象。
        '''
        for key in dict_data:
            if isinstance(dict_data[key],dict):
                self.__reduce_dict(dict_data[key],ret)
            elif isinstance(dict_data[key], list):
                self.__reduce_list_dict(dict_data[key], key, ret)
            else:
                if not ret.get(key):
                    ret[key] = [dict_data[key]]
                else:
                    ret[key].append(dict_data[key])
        return ret
    
    def __reduce_list_dict(self,list_dict,key,ret={}):
        '''
        对list中的值是dict类型的数据进行降维。
        arg: [list_dict] 值是dict的list. egg: [{"a":1},"v"]
        arg: [key] 存放到参数ret对象中的key，一般是该list在上级字典中key。
        arg: [ret] 数据存放的dict对象
        '''
        for i in list_dict:
            if isinstance(i, dict):
                self.__reduce_dict(i, ret)
            elif isinstance(i,list):
                self.__reduce_list_dict(i, key, ret)
            else:
                if not ret.get(key):
                    ret[key] = [i]
                else:
                    ret[key].append(i)
    
    def trow_error_with_low_dimensionality_dict_value(self,response,key,value):
        '''
        将多维字典降维到一维字典，然后通过索引key获取value与预期结果进行比较，不一致时返回JsonValueError异常。
        src_data = {                                  dist_data = {
            "a":1,                                        "a":[1],
            "b":{                                         "c":[2,5],
                "c":2,                                    "d":[3,4,6],
                "d":[                                     "f":[7]
                    3,                                }
                    4                                 
                    ]                                 
                }                                     
            "e":[                  -->                
                {                                     
                    "c":5,                            
                    "d":6                             
                    },                                
                {                                     
                    "f":7                             
                    }                                 
                ]                                     
            }                                         
        
        arg: [response] requests.models.Response 类型
        arg: [key] 字典检索的key 需是value不是字典的key。
        arg: [value] 预期结果
        '''
        if isinstance(response, Response):
            rsp_dict = response.json()
            low_dim_dict = self.__reduce_dict(rsp_dict)
            if isinstance(value, list):
                ret1=set(value)
                ret2=set(copy.deepcopy(low_dim_dict[key]))
                if ret1.intersection(ret2) != set(value):
                    raise JsonValueError("Json value error.target[%s] result[%s]"(value,low_dim_dict[key]))
            else:
                if value not in low_dim_dict[key]:
                    raise JsonValueError("Json value error.target[%s] result[%s]"(value,low_dim_dict[key]))
        else:
            raise AttributeError("parameter 'response' must be Response type.[%s]"%type(response))
    
    def throw_error_with_dict_value(self,response,value,path_key=""):
        '''
        将 json转成 IDict对象后通过索引获取值与期望值进行比较，与预期不符时返回JsonValueError错误。
        
        arg: [response] requests.models.Response 类型
        arg: [value] 预期返回结果
        arg: [path_key] 检索实际结果的路径。
            例：json_obj={
                    "a":1,
                    "b":{
                        "c":2,
                        "d":[
                            {
                                "e":3,
                                "f":4
                                },
                            {
                                "g":5
                                }
                            ]
                        }
                    }
            检索 "a" --> a
            检索 "c" --> b.c
            检索 "e" --> b.d._0.e  当value为list时索引前面加'_',如索引为0时写成'_0' 
            检索 "g" --> b.d._1.g  索引为1时，写成'_1'
        '''
        if isinstance(response, Response):
            rsp_dict = response.json()
            idict = IDict(rsp_dict)
            if path_key:
                val = idict
                for i in path_key.split("."):
                    val = getattr(idict, i)
                if val != value:
                    raise JsonValueError("Json value error.target[%s] result[%s]"(value,val))
            else:
                if idict != value:
                    raise JsonValueError("Json value error.target[%s] result[%s]"(value,idict))
        else:
            raise AttributeError("parameter 'response' must be Response type.[%s]"%type(response))
        
if __name__ == "__main__":
    pass


