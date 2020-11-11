# -*- coding: utf-8 -*-
import requests
import json
url = 'http://model-admin-dev.crealitygroup.com/api/cxy/model/modelGroupList'
headers = {'content-type': "application/json;charset=UTF-8",
           "__CXY_APP_ID_": "creality_model",
           "__CXY_DUID_": "2fe87108-2b1e-447d-aab7-ea42417ca95f",
           "__CXY_OS_LANG_": "1",
           "__CXY_OS_VER_": "Windows 10",
           "__CXY_PLATFORM_": "2",
           }
body = {
    "page": 1,
    "pageSize": 10,
    "listType": 1, }

res = requests.post(url=url, data=json.dumps(body), headers=headers)
data = res.content.decode()
print(res.status_code)  # 返回200
print(data)  # 返回的html
