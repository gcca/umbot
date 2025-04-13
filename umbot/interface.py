import json

from sanic import Sanic
from sanic.log import logger

import umbot.domain.model
import umbot.infrastructure


async def ProcessMessage(app: Sanic, data: dict) -> None:
    url = app.config.get("TELEGRAM_URL")
    if not url:
        logger.error("TELEGRAM_URL not set in config")
        return

    message = data.get("message", {})
    text = message.get("text", "").strip().lower()
    chat_id = message.get("chat", {}).get("id", "")

    logger.info("[WH] Enviando mensaje: '%s'", text)
    if text == "encuesta":
        chat = umbot.domain.model.PollChat(
            url, chat_id, "¿Opciones?", ["Opción 1", "Opción 2", "Opción 3"]
        )
    elif text == "pregunta":
        chat = umbot.domain.model.PollChat(
            url, chat_id, "¿Opciones?", ["Opción 1", "Opción 2", "Opción 3"]
        )
    elif text == "ubicación":
        chat = umbot.domain.model.LocationChat(
            url, chat_id, -12.089497924977456, -77.05274842139869, 60
        )
    elif text == "pegatina":
        chat = umbot.domain.model.StickerChat(
            url, chat_id, "https://www.gstatic.com/webp/gallery/1.webp"
        )
    elif text == "documento":
        chat = umbot.domain.model.DocumentChat(
            url, chat_id, "https://www.gstatic.com/webp/gallery/1.webp"
        )
    else:
        chat = umbot.domain.model.MessageChat(url, chat_id, text)

    send_report = await chat.Send()

    await umbot.infrastructure.StoreRecord(
        app.config.get("PG_CONN"),
        json.dumps(data),
        json.dumps(send_report.req_body),
        send_report.res_status,
        send_report.res_text,
    )
