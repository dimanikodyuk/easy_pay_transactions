from resources.authorization import create_app, create_page, get_data, check_data_page
from db.models import insert_config, update_config, check_app, check_page, update_lifetime_config, insert_transaction
from logger.logs import logger_easy_pay


if __name__ == "__main__":

    if check_page() == "0":
        logger_easy_pay.error("main.py - оновлюємо appId та pageId")

        if check_app() == "0":
            row = create_app()
            update_config(f"{row['appId']}", f"{row['pageId']}", 1)

        else:
            logger_easy_pay.error("main.py - оновлюємо pageId")
            row = create_page(check_app())
            update_config(f"{row['appId']}", f"{row['pageId']}", 2)

    v_app_id = check_app()
    v_page_id = check_page()
    #pages_count = check_data_page(v_app_id, v_page_id)
    #print(f"Йдемо в цикл з кількістю ітерацій {pages_count}")
    #get_data(v_app_id, v_page_id, 1)

    get_data(v_app_id, v_page_id, 1)

