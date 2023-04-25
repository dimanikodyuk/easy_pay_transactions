import pymysql
from db.config import host, user, password, database
from logger.logs import logger_easy_pay

conn = pymysql.connect(host=host, port=3306, user=user, passwd=password, db=database,
                       autocommit=True, charset="utf8")


def check_app():
    che = conn.cursor()
    che_sql = f"""SELECT 0 AS app_id
  UNION ALL
SELECT e.app_id
  FROM dwh.easy_pay_transactions_config e
    WHERE e.dt_life_app > NOW()
ORDER BY 1 DESC
LIMIT 1"""
    che.execute(che_sql)
    logger_easy_pay.info("METHOD: check_app()")
    #logger_easy_pay.info(f"SQL: {che_sql}")

    res = che.fetchone()

    logger_easy_pay.info(f"RES: {res[0]}")
    return res[0]


def check_page():
    che = conn.cursor()
    che_sql = f"""SELECT 0 AS app_id
      UNION ALL
    SELECT e.page_id
      FROM dwh.easy_pay_transactions_config e
        WHERE e.dt_life_page > NOW()
    ORDER BY 1 DESC
    LIMIT 1"""
    che.execute(che_sql)

    logger_easy_pay.info("METHOD: check_page()")
    #logger_easy_pay.info(f"SQL: {che_sql}")

    res = che.fetchone()

    logger_easy_pay.info(f"RES: {res[0]}")

    return res[0]


def insert_config(v_app_id, v_page_id):
    # insert згенерованих по запиту authorization.create_session даних
    ins = conn.cursor()
    ins_sql = f"CALL dwh.easy_pay_transaction_conf_ins('{v_app_id}', '{v_page_id}');"
    logger_easy_pay.info(f"METHOD: insert_config({v_app_id}, {v_page_id})")
    ins.execute(ins_sql)
    ins.close()


def update_config(v_app_id, v_page_id, v_type):
    # insert згенерованих по запиту authorization.create_session даних
    upd = conn.cursor()
    upd_sql = f"CALL dwh.easy_pay_transaction_conf_upd('{v_app_id}', '{v_page_id}', {v_type});"
    logger_easy_pay.info(f"METHOD: update_config({v_app_id}, {v_page_id}, {v_type})")
    upd.execute(upd_sql)
    upd.close()


def update_lifetime_config():
    upd = conn.cursor()
    upd_sql = f"""UPDATE dwh.easy_pay_transactions_config SET dt_life_app = DATE_ADD(NOW(), INTERVAL 3 MONTH)
    , dt_life_page = DATE_ADD(NOW(), INTERVAL 20 MINUTE) LIMIT 1;"""
    logger_easy_pay.info("METHOD: update_lifetime_config()")
    upd.execute(upd_sql)
    upd.close()


def insert_transaction(p_transaction_id, p_service_key, p_order_id, p_amount, p_description,
                       p_date_create, p_date_finalize, p_payment_state,  p_original_transaction_id):
    ins = conn.cursor()
    ins_sql = f"""INSERT INTO dwh.easy_pay_transactions(dt_ins, transactionId, serviceKey, orderId, amount, description, 
    dateCreate, dateFinalize, paymentState, originalTransactionId)
    VALUES(NOW(), {p_transaction_id}, '{p_service_key}', '{p_order_id}', {p_amount}, '{p_description}', '{p_date_create}',
    '{p_date_finalize}', '{p_payment_state}', '{p_original_transaction_id}');"""

    logger_easy_pay.info("METHOD: insert_transaction()")
    logger_easy_pay.info(f"SQL: {ins_sql}")

    ins.execute(ins_sql)
    ins.close()


def check_transaction_id(p_transaction_id):
    ch = conn.cursor()
    ch_sql = f""" SELECT 0
  UNION ALL
SELECT e.id
  from dwh.easy_pay_transactions e
  WHERE e.transactionId = {p_transaction_id}
ORDER BY 1 DESC
  LIMIT 1 """
    ch.execute(ch_sql)
    res = ch.fetchone()
    ch.close()

    return res[0]
