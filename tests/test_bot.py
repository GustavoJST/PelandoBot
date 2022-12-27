# flake8: noqa
import requests
import pytest
from pelandobot.tgbot.config import TOKEN, HOST
from pelandobot.bot import setup, handle
from aiohttp import web
from multiprocessing import Process
import ssl


@pytest.mark.skip(reason="not yet implemented")
def run_app():
    WEBHOOK_HOST = HOST
    WEBHOOK_PORT = 8443
    WEBHOOK_LISTEN = "0.0.0.0"
    WEBHOOK_SSL_CERT = "./webhook_cert.pem"
    WEBHOOK_SSL_PRIV = "./webhook_pkey.pem"
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

    web.run_app(
        setup(),
        host=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT,
        ssl_context=context,
    )


@pytest.mark.skip(reason="not yet implemented")
def test_handle():
    test = Process(target=run_app)
    headers = {"Content-Type": "application/json"}
    data = {"chat_id": "1588357893", "text": "/help", "disable_notification": "true"}
    url = f"https://api.telegram.org/bot${TOKEN}/sendMessage"
    response = requests.post(url, data, headers=headers)
    handle(response)
    test.kill()
