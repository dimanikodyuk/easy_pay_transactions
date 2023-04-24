import pymysql
from db.config import host, user, password, database

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
    res = che.fetchone()
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
    res = che.fetchone()
    return res[0]

def insert_config(v_app_id, v_page_id):
    # insert згенерованих по запиту authorization.create_session даних
    ins = conn.cursor()
    ins_sql = f"CALL dwh.easy_pay_transaction_conf_ins('{v_app_id}', '{v_page_id}');"
    ins.execute(ins_sql)
    ins.close()

def update_config(v_app_id, v_page_id, v_type):
    # insert згенерованих по запиту authorization.create_session даних
    upd = conn.cursor()
    upd_sql = f"CALL dwh.easy_pay_transaction_conf_upd('{v_app_id}', '{v_page_id}', {v_type});"
    upd.execute(upd_sql)
    upd.close()


def update_lifetime_confg():
    upd = conn.cursor()
    upd_sql = f"""UPDATE dwh.easy_pay_transactions_config SET dt_life_app = DATE_ADD(NOW(), INTERVAL 3 MONTH)
    , dt_life_page = DATE_ADD(NOW(), INTERVAL 20 MINUTE) LIMIT 1;"""
    upd.execute(upd_sql)
    upd.close()


def update_config(p_app_id, p_page_id, p_type_id):
    upd = conn.cursor()
    upd_sql = f"CALL dwh.easy_pay_transaction_conf_upd({p_app_id}, {p_page_id}, {p_type_id})"
    upd.execute(upd_sql)
    upd.close()
