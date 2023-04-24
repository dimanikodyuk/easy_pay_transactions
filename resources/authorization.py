import requests
import json


def create_app():
    # Метод createApp
    resp_dic = {
      "appId": "",
      "pageId": "",
      "error_status": 0,
      "error": ""
    }

    url = "https://merchantapi.easypay.ua/api/system/createApp"

    payload = {}
    headers = {
      'PartnerKey': 'FinX',
      'locale': 'ua',
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    #print(response.text)
    response_status = response.status_code
    if response_status == 200:
        resp_data = json.loads(response.text)
        resp_dic['appId'] = resp_data['appId']
        resp_dic['pageId'] = resp_data['pageId']
        resp_dic['error'] = resp_data['error']
        return resp_dic
    else:
        resp_dic['error_status'] = 1
        return resp_dic


def create_session(app_id):
    # Метод createPage
    resp_dic = {
        "appId": "",
        "pageId": "",
        "request_session_id": "",
        "error_status": 0,
        "error": ""
    }

    url = "https://merchantapi.easypay.ua/api/system/createPage"

    payload = {}
    headers = {
        'PartnerKey': 'FinX',
        'locale': 'ua',
        'AppId': f'{app_id}',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_status = response.status_code
    if response_status == 200:
        resp_data = json.loads(response.text)
        resp_dic['appId'] = resp_data['appId']
        resp_dic['pageId'] = resp_data['pageId']
        resp_dic['request_session_id'] = resp_data['requestedSessionId']
        resp_dic['error'] = resp_data['error']
        return resp_dic
    else:
        resp_dic['error_status'] = 1
        return resp_dic


#res = create_app()
#res_new = create_session(res['appId'])
