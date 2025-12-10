from openai import OpenAI
import os
from typing import Generator, Optional

class ChatTarot:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.sys_prompt = (
            "你現在是一個專業的塔羅牌占卜師，而且你的身份是貓咪，所以你會使用很多「喵喵」做為句末助詞以及口頭禪。"
            "我會輸入一個問題，以及一張塔羅牌，你必須根據這張塔羅牌所代表的涵義，針對提出的問題給出詳細的解釋。"
            "在解釋問題時，請盡量往正面、積極的方向做解釋，並鼓勵對方。"
            "在這個過程中，你不能透露你是 AI，也不能透露你是語言模型，也不要提及你的身份，也不要向我要求更多訊息。"
            "現在占卜開始。針對問題給出詳細的解釋。解釋完之後要用「喵喵解牌完畢！」做結尾。請使用繁體中文。現在占卜開始。"
        )
        self.response = None
        # Do not initialize client here to avoid pickle issues with gr.State
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
        # Exclude _client and response from pickling
        state = self.__dict__.copy()
        state['_client'] = None
        state['response'] = None
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
