import json
from typing import Optional

import loguru
import openai

from src.config.config import settings
from src.modules.base.models.schemas.base import BaseSchemaModel, BaseAnyModel


class ChatMessage(BaseSchemaModel):
    role: str
    name: str | None = None
    content: Optional[str] = None
    function_call: dict | None = None


class ChatRequest(BaseSchemaModel):
    messages: list[ChatMessage]
    functions: list[dict] | None = None
    temperature: float | None = None


class OpenAiModel(BaseSchemaModel):
    name: str
    max_tokens: int
    max_reply_tokens: int
    engine: str | None = None

    def get_engine(self):
        if self.engine is not None:
            return self.engine
        self.engine = self.name.replace(".", "")
        return self.engine


models: dict[str, OpenAiModel] = {}


def append_model(model: OpenAiModel):
    models[model.name] = model


append_model(OpenAiModel(name="gpt-3.5-turbo", max_tokens=4096, max_reply_tokens=1024))
append_model(OpenAiModel(name="gpt-3.5-turbo-0613", max_tokens=4096, max_reply_tokens=1024))
append_model(OpenAiModel(name="gpt-3.5-turbo-32k", max_tokens=32768, max_reply_tokens=2048))

import tiktoken


class OpenAiClient:
    def __init__(self, model: str = "gpt-3.5-turbo", retain_tokens: int = 0, max_reply_tokens: int = None):
        openai.api_key = settings.openai.api_key
        openai.api_base = settings.openai.api_base
        openai.api_version = settings.openai.api_version
        openai.api_type = settings.openai.api_type
        model = models[model]
        self.model_name = model.name
        self.max_tokens = model.max_tokens
        self.retain_tokens = retain_tokens
        self.max_reply_tokens = max_reply_tokens if max_reply_tokens is not None else model.max_reply_tokens
        self.engine = model.get_engine()

    def chat_send(self, req: ChatRequest):
        # create a chat completion
        engine = self.engine
        messages = list()
        for message in req.messages:
            messages.append(message.model_dump(exclude_none=True, exclude_unset=True))
        loguru.logger.debug("chat_send,engine:{},messages:{}", engine, messages)
        chat_completion = openai.ChatCompletion.create(messages=messages, functions=req.functions,
                                                       function_call="auto", engine=self.engine,
                                                       temperature=req.temperature)
        loguru.logger.debug("chat_send,response:{}", chat_completion)
        return chat_completion.choices[0].message

    def build_chat_messages(self, system_message: ChatMessage, chat_history: list[ChatMessage]):
        """
        Build a list of chat messages that can be sent to OpenAI.
        chat_history: list[ChatMessage] 要求是倒序的
        """
        system_tokens = self.count_tokens([system_message])
        messages = list()
        for i, message in enumerate(chat_history):
            messages.insert(0, message)
            tokens = self.count_tokens(messages)
            if system_tokens + tokens + self.max_reply_tokens + self.retain_tokens > self.max_tokens:
                messages.pop(0)
                break

        messages.insert(0, system_message)
        return messages

    def count_tokens(self, messages: list[ChatMessage]):
        text = ""
        for message in messages:
            text += message.role + ":"
            text += message.content + "\n"
        return self.count_text_tokens(text)

    def count_text_tokens(self, text: str):
        enc = tiktoken.encoding_for_model(self.model_name)
        encoded = enc.encode(text)
        return len(encoded)
