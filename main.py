from resources.authorization import create_app, create_session
from db.models import insert_config, update_config, check_app, check_page

if __name__ == "__main__":
    # pageId - не діючий
    if check_page() == 0 or check_page() == "0":
        # appId - не діючий (оновлюємо і appId, pageId)
        if check_app() == 0 or check_app() == "0":
            row = create_app()
            update_config(f"'{row['appId']}'", f"'{row['pageId']}'", 1)
        else:
            # якщо pageId не діючий, але appId - діючий, оновлюємо лише pageId
            row = create_session(check_app())
            update_config(f"'{row['appId']}'", f"'{row['pageId']}'", 2)
    else:
        # в іншому випадку отримуємо діючий pageId для подальших запитів
        res = check_page()
        print(res)


    #res = create_app()
    #print(res)
    #insert_app(res['appId'], res['pageId'])

    """
    check_conf = check_config()
    if check_conf == 1:
        create_app()
    elif check_conf == 2:
        create_session()
    else:
        3
    """