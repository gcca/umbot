import os

from dotenv import load_dotenv
from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse, json

import umbot.infrastructure
import umbot.interface

load_dotenv()

app = Sanic("umbot", env_prefix="UMBOT_")

cert_path = app.config.get("SSL_CERT", "")
key_path = app.config.get("SSL_KEY", "")

if os.path.exists(cert_path) and os.path.exists(key_path):
    app.config["SSL"] = {"cert": cert_path, "key": key_path}


@app.before_server_start
async def setup_db(app: Sanic) -> None:
    pg_conn = app.config.get("PG_CONN")
    if not pg_conn:
        raise ValueError("PG_CONN not set in config")

    await umbot.infrastructure.StateSchema(pg_conn)


@app.post("/webhook")
async def webhook(request: Request) -> HTTPResponse:
    app.add_task(umbot.interface.ProcessMessage(app, request.json))
    return json("")


@app.get("/")
async def index(_: Request) -> HTTPResponse:
    return json("👍")
