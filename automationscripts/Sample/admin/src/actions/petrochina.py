# _*_ coding: UTF-8 _*_

import json
import csv
import requests
import os

class Sender:
    def __init__(self):
        self.data_dir = os.path.dirname(os.path.abspath(__file__))+"/data/"

    def sender(self, kwargs):
        method = kwargs['method']
        url = kwargs['url']
        headers = self.covert_to_dict(kwargs, 'headers')
        # query parameters
        payload = self.covert_to_dict(kwargs, 'payload')
        # from data for put and post
        data = self.covert_to_dict(kwargs, 'data')
        # json data for put and post
        body = kwargs.get('body')
        # Files & binary data
        file_key = kwargs.get('file_key')
        file_value = kwargs.get('file_value')
        if file_key and file_value:
            file_name = self.data_dir + file_value
            files = {file_key: (file_value, open(file_name, 'rb'))}
            response = requests.request(method, url, params=payload, data=data, json=body, files=files, headers=headers)
            return response
        else:
            response = requests.request(method, url, params=payload, data=data, json=body, headers=headers)
            return response

    def covert_to_dict(self, params, key):
        if key in params.keys():
            if params[key]:
                return json.loads(params[key])
        else:
            return None

    def covert_to_dict_from_file(self, params):
        # 将a=b&c=d格式的字符串格式化为字典
        file_name = self.data_dir + params['raw_data_file']
        with open(file_name,'r') as fp:
            a = fp.read().split('&')
            b = []
            for i in range(len(a)):
                b = b + a[i].split('=')
            keys = [b[i] for i in range(len(b)) if i % 2 == 0]
            values = [b[i] for i in range(len(b)) if i % 2 == 1]
            data = dict(zip(keys, values))
            return json.dumps(data)

    def get_query_by_file(self, params):  # 解析query部分
        file_name = self.data_dir + params.get('file_name')
        with open(file_name,'r') as fp:
            return json.dumps(json.load(fp))

    def get_query_list(self, params):
        column = params['column']
        new_params = {}
        fields_list = []
        filename = self.data_dir + params['file_name']
        with open(filename) as f:
            reader = csv.DictReader(f)
            for row in reader:
                for i in range(len(column)):  # row 返回每一行的字典
                    print row[column[i]]
                    new_params.update({column[i]: row[column[i]]})
                manual = json.dumps(new_params)
                fields_list.append(manual)
        return fields_list

    def get_multiple(self, params):
        responses = []
        method = params['method']
        url = params['url']
        fields = params['fields_list']
        headers = params.get('headers')
        for i in range(len(fields)):
            r = self.sender({'method': method, 'url': url, 'fields': fields[i], 'headers': headers})
            responses.append(r)
        return responses

    def get_value_by_key(self, params):
        response = params['response']
        response = json.loads(response.text)
        key = params['key']
        return response[key]

    def assertEqual(self, params):
        assert params['A'] == params['B']

    def assertNotEqual(self,params):
        assert params['A'] != params['B']

    def assertTrue(self,params):
        assert params['A']

    def assertFalse(self,params):
        assert not params['A']

    def assertIsNone(self,params):
        if not params['A']:
            assert True

    def assertIsNotNone(self, params):
        if params['A']:
            assert True