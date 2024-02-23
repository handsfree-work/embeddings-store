from src.config.config import LocalAiSettings
from src.modules.ai.models.ai_model import EmbeddingRequest

from src.utilities.request import aio
from src.utilities.request.aio import AioRequest


class LocalAIClient:
    def __init__(self, setting: LocalAiSettings):
        self.setting: LocalAiSettings = setting

    async def embedding(self, req: EmbeddingRequest):
        data = {
            "input": req.input
        }
        req = AioRequest(url=self.setting.embedding_url, data=data, method="POST")
        res = await aio.request(req)
        return res['data']['embeddings'][0]
