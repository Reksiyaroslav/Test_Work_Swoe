import socket
import ssl
from hhtp.myhttp import HTTPRequest, HTTPResponse
import base64
import logging

logging.basicConfig(
    filename="sms_client.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",)
def create_numbers_and_message(url, port, username, password) -> HTTPResponse:
    
    while True:
        
        number_sender = input("Введите номер отправителя: ")
        number_recipient = input("Введите номер получателя: ")

        if number_sender.isdigit() and number_recipient.isdigit():

            if (11 <= len(number_sender) <= 18) and (11 <= len(number_recipient) <= 18):
                message = input("Введите сообщение: ")

                # Формирование тела запроса
                body = f"from={number_sender}&to={number_recipient}&text={message}"

                # Создание HTTP-запроса
                request = HTTPRequest(
                    method="POST",
                    url=url,
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded",
                        "Content-Length": str(len(body)),
                    },
                    body=body,
                )

                # Добавляем авторизацию
                auth = base64.b64encode(f"{username}:{password}".encode()).decode()
                request.headers["Authorization"] = f"Basic {auth}"

                try:
                    # Подключение с учетом HTTPS
                    with socket.create_connection((url,port)) as sock:
                        if url.scheme == "https":
                            context = ssl.create_default_context()
                            sock = context.wrap_socket(
                        sock, server_hostname=url
                            )
                        # Чтение ответа
                        response = b""
                        while True:
                            chunk = sock.recv(4096)
                            if not chunk:
                                break
                            response += chunk
                            print(response)
                        return HTTPResponse.from_bytes(response)

                except Exception as e:
                    logging.error(f"Ошибка: {e}")
                    return None

            else:
                logging.error("Некорректная длина номера")
        else:
           logging.error("Номера должны быть только из цифар")
