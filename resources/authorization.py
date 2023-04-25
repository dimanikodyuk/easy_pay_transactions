import requests
import json
import base64
import hashlib
import datetime
from db.config import secret_key
from db.models import check_app, check_page, insert_transaction, check_transaction_id, insert_config, update_lifetime_config
from logger.logs import logger_easy_pay


# Метод creaApp (створення appId та pageId)
def create_app():
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

    logger_easy_pay.info(f"METHOD: create_app()")
    logger_easy_pay.info(f"URL: {url}")
    logger_easy_pay.info(f"HEADERS {headers}")
    logger_easy_pay.info(f"RESPONSE_STATUS: {response_status}")
    logger_easy_pay.info(f"RESPONSE: {response.text}")

    if response_status == 200:
        resp_data = json.loads(response.text)
        resp_dic['appId'] = resp_data['appId']
        resp_dic['pageId'] = resp_data['pageId']
        resp_dic['error'] = resp_data['error']
        return resp_dic
    else:
        resp_dic['error_status'] = 1
        return resp_dic


# Метод createPage (оновлення pageId)
def create_page(app_id):
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

    logger_easy_pay.info(f"METHOD: create_page()")
    logger_easy_pay.info(f"URL: {url}")
    logger_easy_pay.info(f"HEADERS {headers}")
    logger_easy_pay.info(f"RESPONSE_STATUS: {response_status}")
    logger_easy_pay.info(f"RESPONSE: {response.text}")

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

def check_data_page(p_app_id, p_page_id):
    url = "https://merchantapi.easypay.ua/api/merchant/history/transactions"
    today = datetime.datetime.today() - datetime.timedelta(days=1)
    p_dt1 = today.strftime("%Y-%m-%dT00:00:00")
    p_dt2 = today.strftime("%Y-%m-%dT23:59:59")

    payload = json.dumps({
        "serviceKeys": [
            "FINX-CREDIT-TO-CARD"
        ],
        "dateStart": f"{p_dt1}",
        "dateEnd": f"{p_dt2}",
        "pageNumber": 1,
        "countPerPage": 500
    })

    # Генерація підпису (sign)
    key_and_body = (secret_key + payload).encode('utf-8')
    hash_object = hashlib.sha256(key_and_body)
    base64_encoded = base64.b64encode(hash_object.digest())
    key = base64_encoded.decode('utf-8')

    headers = {
        'appId': f'{p_app_id}',
        'pageId': f'{p_page_id}',
        'partnerKey': 'finx',
        'sign': key,
        'Content-Type': 'application/json',
        'locale': 'uk',
    }

    logger_easy_pay.info(f"HEADER: {headers}")

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    print(response.text)

    resp_data = json.loads(response.text)
    return resp_data['pagingData']['pagesCount']


# Отримуємо список транзакцій за вчорашній день
def get_data(p_app_id, p_page_id, p_page_num):

    url = "https://merchantapi.easypay.ua/api/merchant/history/transactions"
    today = datetime.datetime.today() - datetime.timedelta(days=1)
    #p_dt1 = today.strftime("%Y-%m-%dT%H:%M:%S")
    #p_dt2 = datetime.datetime.today().strftime("%Y-%m-%dT%H:%M:%S")
    p_dt1 = today.strftime("%Y-%m-%dT00:00:00")
    p_dt2 = today.strftime("%Y-%m-%dT23:59:59")

    logger_easy_pay.info(f"Вибірка за період {p_dt1} - {p_dt2}")
    payload = json.dumps({
        "serviceKeys": [
            "FINX-CREDIT-TO-CARD"
        ],
        "dateStart": f"{p_dt1}",
        "dateEnd": f"{p_dt2}",
        "pageNumber": p_page_num,
        "countPerPage": 500
    })

    # Генерація підпису (sign)
    key_and_body = (secret_key + payload).encode('utf-8')
    hash_object = hashlib.sha256(key_and_body)
    base64_encoded = base64.b64encode(hash_object.digest())
    key = base64_encoded.decode('utf-8')

    headers = {
        'appId': f'{p_app_id}',
        'pageId': f'{p_page_id}',
        'partnerKey': 'finx',
        'sign': key,
        'Content-Type': 'application/json',
        'locale': 'uk',
    }

    logger_easy_pay.info(f"HEADER: {headers}")

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    print(response.text)

    if response.status_code == 200:
        resp_data = json.loads(response.text)
        #print(resp_data['pagingData'])
        for row in resp_data['items']:
            print(row)
            p_transaction_id = row['transactionId']

            if check_transaction_id(p_transaction_id) == 0:
                p_service_key = row['serviceKey']
                p_order_id = row['orderId']
                p_amount = row['amount']
                p_description = row['description']
                p_date_create = datetime.datetime.fromisoformat(row['dateCreate'])
                p_date_finalize = datetime.datetime.fromisoformat(row['dateFinalize'])
                p_payment_state = row['paymentState']
                p_original_transaction_id = row['originalTransactionId']

                p_dt_create = p_date_create.strftime("%Y-%m-%d %H:%M:%S")
                p_dt_finalize = p_date_finalize.strftime("%Y-%m-%d %H:%M:%S")

                insert_transaction(p_transaction_id, p_service_key, p_order_id, p_amount, p_description, p_dt_create,
                                   p_dt_finalize, p_payment_state, p_original_transaction_id)

                update_lifetime_config()

            #else:
            #   logger_easy_pay.warn(f"Транзакція № {p_transaction_id} вже наявна в БД")

    else:
        logger_easy_pay.error(f"ERROR: {response.text}")

#v_app = check_app()
#v_page = check_page()
#get_data(v_app, v_page)

