import aiohttp
from app.utils.logger_config import logger

async def async_http_request(method, url, headers=None, params=None, data=None, json_data=None, http_proxy=None):
    """
    统一的异步 HTTP 请求方法
    :param method: HTTP 方法 (GET, POST, PUT, DELETE, etc.)
    :param url: 请求的 URL
    :param headers: 请求头
    :param params: URL 参数
    :param data: 表单数据
    :param json_data: JSON 数据
    :param http_proxy: 代理服务器地址 (可选)
    :return: 响应内容
    """
    connector = aiohttp.TCPConnector()
    if http_proxy:
        connector = aiohttp.ProxyConnector(proxy=http_proxy)

    async with aiohttp.ClientSession(connector=connector) as session:
        try:
            async with session.request(method, url, headers=headers, params=params, data=data, json=json_data) as response:
                if response.status == 200:
                    return await response.json() if response.content_type == 'application/json' else await response.text()
                else:
                    error_message = f"HTTP request failed with status code {response.status}: {await response.text()}"
                    logger.error(error_message)
                    return None
        except Exception as e:
            logger.error(f"Error occurred during HTTP request: {e}")
            raise e
