from openai import OpenAI
import os
from typing import Generator, Optional, List, Tuple

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

    def BuildPrompt(self, problem: str, cards: List[Tuple[str, str, str]], positions: List[str]) -> tuple[str, str]:
        # cards: List of (path, info, name)
        
        cards_desc = ""
        for i, (path, info, name) in enumerate(cards):
            position = positions[i] if i < len(positions) else f"位置{i+1}"
            cards_desc += f"\n[{position}] {name}\n涵義：{info}\n"

        user_prompt = f"問題：{problem}\n\n抽出的牌陣：\n{cards_desc}\n解牌開始："
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
