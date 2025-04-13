from pydantic import BaseModel, Field


class TelegramChat(BaseModel):
    first_name: str
    id: int
    last_name: str
    type: str
    username: str


class TelegramFrom(BaseModel):
    first_name: str
    id: int
    is_bot: bool
    language_code: str
    last_name: str
    username: str


class TelegramMessage(BaseModel):
    chat: TelegramChat
    date: int
    from_: TelegramFrom = Field(alias="from")
    message_id: int
    text: str


class TelegramUpdate(BaseModel):
    message: TelegramMessage
    update_id: int
