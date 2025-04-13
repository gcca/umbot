import json
from abc import ABC, abstractmethod
from typing import NamedTuple, override

import aiohttp
from sanic.log import logger


class SendReport(NamedTuple):
    req_body: dict
    res_status: int
    res_text: str


class Chat(ABC):

    @abstractmethod
    async def Send(self) -> SendReport: ...


class ChatSupport(Chat):

    _url: str
    _chat_id: int

    __slots__ = ("_url", "_chat_id")

    def __init__(self, url: str, chat_id: int) -> None:
        self._url = url
        self._chat_id = chat_id

    @property
    @abstractmethod
    def _path(self) -> str: ...

    @abstractmethod
    async def _MakeBody(self) -> dict: ...

    @override
    async def Send(self) -> SendReport:
        url = f"{self._url}/{self._path}"
        body = await self._MakeBody()

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body) as res:
                res_status = res.status
                res_text = await res.text()
                if res_status != 200:
                    logger.error(
                        "Error sending message: data=%s resp=%s",
                        json.dumps(body),
                        res_text,
                    )

        return SendReport(body, res_status, res_text)


class MessageChat(ChatSupport):

    _text: str

    __slots__ = ("_text",)

    def __init__(self, url: str, chat_id: int, text: str) -> None:
        super().__init__(url, chat_id)
        self._text = text

    @property
    @override
    def _path(self) -> str:
        return "sendMessage"

    @override
    async def _MakeBody(self) -> dict:
        return {
            "chat_id": self._chat_id,
            "text": self._text,
        }


class PollChat(ChatSupport):

    _question: str
    _options: list

    __slots__ = ("_question", "_options")

    def __init__(
        self, url: str, chat_id: int, question: str, options: list
    ) -> None:
        super().__init__(url, chat_id)
        self._question = question
        self._options = options

    @property
    @override
    def _path(self) -> str:
        return "sendPoll"

    @override
    async def _MakeBody(self) -> dict:
        return {
            "chat_id": self._chat_id,
            "question": self._question,
            "options": self._options,
            "is_anonymous": True,
            "type": "regular",
        }


class QuestionChat(ChatSupport):

    _question: str
    _options: list
    _correct_option_id: int

    __slots__ = ("_question", "_options", "_correct_option_id")

    def __init__(
        self,
        url: str,
        chat_id: int,
        question: str,
        options: list,
        correct_option_id: int,
    ) -> None:
        super().__init__(url, chat_id)
        self._question = question
        self._options = options
        self._correct_option_id = correct_option_id

    @property
    @override
    def _path(self) -> str:
        return "sendPoll"

    @override
    async def _MakeBody(self) -> dict:
        return {
            "chat_id": self._chat_id,
            "question": self._question,
            "options": self._options,
            "is_anonymous": True,
            "type": "quiz",
            "correct_option_id": self._correct_option_id,
        }


class LocationChat(ChatSupport):

    _latitude: float
    _longitude: float
    _live_period: int

    __slots__ = ("_latitude", "_longitude", "_live_period")

    def __init__(
        self,
        url: str,
        chat_id: int,
        latitude: float,
        longitude: float,
        live_period: int,
    ) -> None:
        super().__init__(url, chat_id)
        self._latitude = latitude
        self._longitude = longitude
        self._live_period = live_period

    @property
    @override
    def _path(self) -> str:
        return "sendLocation"

    @override
    async def _MakeBody(self) -> dict:
        return {
            "chat_id": self._chat_id,
            "latitude": self._latitude,
            "longitude": self._longitude,
            "live_period": self._live_period,
        }


class StickerChat(ChatSupport):

    _sticker: str

    __slots__ = ("_sticker",)

    def __init__(self, url: str, chat_id: int, sticker: str) -> None:
        super().__init__(url, chat_id)
        self._sticker = sticker

    @property
    @override
    def _path(self) -> str:
        return "sendSticker"

    @override
    async def _MakeBody(self) -> dict:
        return {
            "chat_id": self._chat_id,
            "sticker": self._sticker,
        }


class DocumentChat(ChatSupport):

    _document: str

    __slots__ = ("_document",)

    def __init__(self, url: str, chat_id: int, document: str) -> None:
        super().__init__(url, chat_id)
        self._document = document

    @property
    @override
    def _path(self) -> str:
        return "sendDocument"

    @override
    async def _MakeBody(self) -> dict:
        return {
            "chat_id": self._chat_id,
            "document": self._document,
        }
