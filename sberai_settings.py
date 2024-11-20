import json
import uuid
from os import getenv

from dotenv import load_dotenv
import httpx

load_dotenv()

SBER_SECRET_API_KEY = getenv("CLIENT_SECRET_GIGA_CHAT_API")
SBER_AUTHORIZATION_DATA = getenv("AUTHORIZATION_DATA_GIGA_CHAT_API")

url = "https://ngw.devices.sberbank.ru:9443/api/v2"
question_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
payload = f"scope={SBER_SECRET_API_KEY}"


def get_payload_message(text: str):
    payload = json.dumps(
        {
            "model": "GigaChat",
            "messages": [{"role": "user", "content": f"{text}"}],
            "temperature": 1,
            "top_p": 0.1,
            "n": 1,
            "stream": False,
            "max_tokens": 512,
            "repetition_penalty": 1,
        }
    )
    return payload


class AIClient:
    def __init__(
        self,
        base_url: str,
        secret_key: str,
        auth_data: str,
    ):
        self.__access_token = None
        self.base_url = base_url
        self.__secret_key = secret_key
        self.__auth_data = auth_data
        rq_uid = str(uuid.uuid4())
        self.__headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": rq_uid,
            "Authorization": f"Basic {self.__auth_data}",
        }

    async def authorization(self):
        """Метод для авторизации AI клента"""
        try:
            async with httpx.AsyncClient(verify=False) as cl:
                data = await cl.post(
                    url=self.base_url + "/oauth",
                    headers=self.__headers,
                    data=f"scope=GIGACHAT_API_PERS",
                )
                data = data.json()
                self.__access_token = data["access_token"]
                self.__headers.pop("RqUID")
                self.__headers["Authorization"] = f"Bearer {self.__access_token}"

        except httpx.HTTPError as err:
            print(err)
            print("Не получилось авторизоваться")

    async def ask_a_question(self, text: str) -> dict:
        """Метод для обращения к AI"""
        payload = get_payload_message(text=text)
        async with httpx.AsyncClient(verify=False) as cl:
            data = await cl.post(url=question_url, headers=self.__headers, data=payload)
            response_data = data.json()

            return response_data["choices"][0]["message"]["content"]


ai_client = AIClient(
    base_url=url, secret_key=SBER_SECRET_API_KEY, auth_data=SBER_AUTHORIZATION_DATA
)
