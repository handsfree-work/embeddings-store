from typing import Optional

import loguru
import openai
from openai import InvalidRequestError

from src.config.config import settings
from src.modules.base.models.schemas.base import BaseSchemaModel, BaseAnyModel
from src.utilities.exceptions.biz.biz_common import client_error


class ChatMessage(BaseSchemaModel):
    role: str
    name: str | None = None
    content: Optional[str] = None
    function_call: dict | None = None


class ChatRequest(BaseSchemaModel):
    messages: list[ChatMessage]
    functions: list[dict] | None = None
    temperature: float | None = None


class EmbeddingRequest(BaseSchemaModel):
    input: str


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


class ModelRegistry(BaseAnyModel):
    gpt_35_turbo: OpenAiModel = OpenAiModel(name="gpt-3.5-turbo", max_tokens=4096, max_reply_tokens=1024)
    gpt_35_turbo_0613: OpenAiModel = OpenAiModel(name="gpt-3.5-turbo-0613", max_tokens=4096, max_reply_tokens=1024)
    gpt_35_turbo_32k: OpenAiModel = OpenAiModel(name="gpt-3.5-turbo-32k", max_tokens=32768, max_reply_tokens=2048)
    gpt_35_turbo_16k: OpenAiModel = OpenAiModel(name="gpt-3.5-turbo-16k", max_tokens=16384, max_reply_tokens=2048)
    text_embedding_ada_002: OpenAiModel = OpenAiModel(name="text-embedding-ada-002", max_tokens=32768,
                                                      max_reply_tokens=2048)

    def get(self, name: str):
        for k, v in self.__dict__.items():
            if v.name == name:
                return v


model_registry = ModelRegistry()

import tiktoken


class OpenAiClient:
    def __init__(self, model: str | OpenAiModel = "gpt-3.5-turbo", retain_tokens: int = 0,
                 max_reply_tokens: int = None):
        openai.api_key = settings.openai.api_key
        openai.api_base = settings.openai.api_base
        openai.api_version = settings.openai.api_version
        openai.api_type = settings.openai.api_type
        if isinstance(model, str):
            model = model_registry.get(model)
        self.model_name = model.name
        self.max_tokens = model.max_tokens
        self.retain_tokens = retain_tokens
        self.max_reply_tokens = max_reply_tokens if max_reply_tokens is not None else model.max_reply_tokens
        self.engine = model.get_engine()

    async def chat_send(self, req: ChatRequest):
        # create a chat completion
        engine = self.engine
        messages = list()
        for message in req.messages:
            messages.append(message.model_dump(exclude_none=True, exclude_unset=True))
        loguru.logger.debug("chat_send,engine:{},messages:{}", engine, messages)
        try:
            chat_completion = await openai.ChatCompletion.acreate(messages=messages, functions=req.functions,
                                                                  function_call="auto", engine=self.engine,
                                                                  temperature=req.temperature, timeout=120)
            loguru.logger.debug("chat_send,response:{}", chat_completion)
            return chat_completion.choices[0].message
        except InvalidRequestError as e:
            loguru.logger.error("chat_send error:{}", e)
            raise client_error(message=e.user_message)

    async def embedding(self, req: EmbeddingRequest):
        try:
            res = await openai.Embedding.acreate(input=[req.input], model=self.model_name, timeout=30)
            return res['data'][0]['embedding']
        except InvalidRequestError as e:
            loguru.logger.error("embedding error:{}", e)
            raise client_error(message=e.user_message)

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
