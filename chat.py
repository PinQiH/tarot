from openai import OpenAI
import os
from typing import Generator, Optional

class ChatTarot:
    def __init__(self, system_prompt: str):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.sys_prompt = system_prompt
        self.response = None
        self._client: Optional[OpenAI] = None

    @property
    def client(self) -> OpenAI:
        if self._client is None:
            self._client = OpenAI(api_key=self.api_key)
        return self._client

    def BuildPrompt(self, problem: str, tarot_name: str, tarot_info: str) -> tuple[str, str]:
        user_prompt = f"問題：{problem}\n塔羅牌：{tarot_name}\n相關詞：{tarot_info}\n解牌開始："
        return self.sys_prompt, user_prompt

    def Chat(self, user_prompt: str) -> Generator[str, None, None]:
        try:
            self.response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": self.sys_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                stream=True,
            )

            res = ""
            for chunk in self.response:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    res += content
                    yield res
        except Exception as e:
            yield f"發生錯誤: {str(e)}"

    def Stop(self):
        if self.response:
            self.response.close()
            
    def __getstate__(self):
        state = self.__dict__.copy()
        state['_client'] = None
        state['response'] = None
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
