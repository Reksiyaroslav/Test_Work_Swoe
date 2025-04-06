import toml
import func.func as fun
import logging

logging.basicConfig(
    filename="run_client.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def main():
    with open("config.toml", "r") as f:
        config = toml.load(f)

    url_server = config["server"]["host"]
    port_server = config["server"]["port"]
    user_server = config["user"]["USER_NAME"]
    password_server = config["user"]["PASSWORD_USER"]

    response = fun.create_numbers_and_message(
        url=url_server, port=port_server, username=user_server, password=password_server
    )

    if response is not None:
        print(f"Код ответа: {response.status_code}")
        print(f"Тело ответа: {response.body}")
    else:
        logging.error("Ошибка при отправке запроса. Проверьте лог ошибок.")


if __name__ == "__main__":
    main()
