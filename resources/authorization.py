import requests
import json
import base64
import hashlib
import hmac
from db.config import secret_key


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
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
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

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
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


def sign():

    url = "https://merchantapi.easypay.ua/api/merchant/history/transactions"

    payload = json.dumps({
        "serviceKeys": [ "MERCHANT-TEST-7559", "MERCHANT-TEST" ],
        "dateStart": "2023-03-01T00:00:19.738Z",
        "dateEnd": "2023-03-02T17:28:19.738Z",
        "pageNumber": 2,
        "countPerPage": 7
    })

    payload = json.dumps({
        "serviceKeys": [
            "MERCHANT-TEST"
        ],
        "dateStart": "2023-03-01",
        "dateEnd": "2023-03-02",
        "pageNumber": 2,
        "countPerPage": 7
    })

    #test = bytes(secret_key+payload, 'UTF-8')
    #sign = base64.b64encode(hashlib.sha256(test)) # b'sign_row')
    #print(sign)

    clientId = bytes(payload, 'utf-8')
    secret = bytes(secret_key, 'utf-8')

    base64signature = base64.b64encode(hmac.new(secret, clientId, digestmod=hashlib.sha256).digest())
    print(base64signature)

    headers = {
        'appId': '7399751b-d00e-47e6-8b2d-d15e1311654f',
        'pageId': 'ed15dfe8-d6a8-4c2e-a333-f51b1196d6a5',
        'partnerKey': 'finx',
        'sign': f'{sign}',
        'Content-Type': 'application/json',
        'locale': 'uk',
    }


    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    print(response.text)







#res = create_app()
#res_new = create_session(res['appId'])
sign()