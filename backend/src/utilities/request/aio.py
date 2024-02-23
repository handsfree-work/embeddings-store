import aiohttp
import pydantic


class AioRequest(pydantic.BaseModel):
    method: str = "POST"
    url: str
    data: dict = {}
    headers: dict = {}


async def request(req: AioRequest):
    if req.method == "GET":
        async with aiohttp.ClientSession() as session:
            async with session.get(req.url) as response:
                # print("Status:", response.status)
                # print("Content-type:", response.headers['content-type'])
                if response.status < 200 or response.status >= 300:
                    raise Exception(f"请求失败: {response.status}，{response.text()}")
                json = await response.json()
                return json
    elif req.method == "POST":
        async with aiohttp.ClientSession() as session:
            async with session.post(req.url, json=req.data) as response:
                if response.status < 200 or response.status >= 300:
                    raise Exception(f"请求失败: {response.status}，{response.text()}")
                json = await response.json()
                return json
