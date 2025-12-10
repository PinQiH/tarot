from threading import Event
import gradio as gr
from typing import List, Tuple, Any, Generator, Dict

from chat import ChatTarot
from tarot import TarotDeck
from personas import CURRENT_PERSONA

class MeowTarotApp:
    def __init__(self):
        css = ReadText("asset/style.css")
        font = [gr.themes.GoogleFont("Noto Sans Mono")]
        theme = gr.themes.Soft(font=font)

        self.persona = CURRENT_PERSONA

        with gr.Blocks(css=css, theme=theme, title=self.persona.title) as self.app:
            self.stop_event = gr.State(None)
            self.resp = gr.State("")
            self.deck = gr.State(TarotDeck())
            self.chat_tarot = gr.State(ChatTarot(self.persona.system_prompt))
            
            gr.Markdown(f"# {self.persona.title}", elem_id="title")
            
            with gr.Row():
                with gr.Column():
                    self.InitLeftColumn()

                with gr.Column():
                    self.InitRightColumn()

            self.RegisterEvents()

    def Launch(self):
        # Removed favicon_path="asset/RoundCat.png" as it's no longer a cat theme
        self.app.queue().launch(share=True)

    def InitLeftColumn(self):
        with gr.Group():
            self.welcome = [{"role": "assistant", "content": self.persona.welcome}]
            self.chat = gr.Chatbot(label=self.persona.title, value=self.welcome, height=600)
            self.msg = gr.Textbox(label="問題", placeholder="請輸入你想問的問題...", interactive=True)
            with gr.Row():
                self.send = gr.Button("🌙  抽牌")
                self.clear = gr.Button("🗑️  清除")
                self.stop = gr.Button("🛑 停止")
            with gr.Accordion("完整提示", open=False) as self.fold:
                self.debug_msg = gr.TextArea(show_label=False, lines=14)

    def InitRightColumn(self):
        with gr.Group():
            self.tarot_name = gr.Textbox(label="塔羅牌名稱")
            self.image = gr.Image(label="塔羅牌", interactive=False, height=400)
            self.info = gr.TextArea(label="塔羅牌資訊", lines=20)

    def RegisterEvents(self):
        inn_send = [self.msg, self.chat, self.deck, self.chat_tarot]
        out_send = [
            self.msg,
            self.chat,
            self.image,
            self.info,
            self.tarot_name,
            self.resp,
            self.debug_msg,
            self.stop_event,
        ]
        
        submit_event = self.msg.submit(self.SendMessage, inn_send, out_send)
        click_event = self.send.click(self.SendMessage, inn_send, out_send)
        
        inn_show = [self.chat, self.resp, self.chat_tarot, self.stop_event]
        out_show = [self.chat]
        
        submit_event.then(self.ShowResponse, inn_show, out_show)
        click_event.then(self.ShowResponse, inn_show, out_show)

        out_clear = [self.chat, self.tarot_name, self.image, self.info]
        self.clear.click(self.Clear, None, out_clear)
        self.stop.click(self.TriggerStop, self.stop_event, queue=False)

    def SendMessage(self, msg: str, chat: List[Dict[str, str]], deck: TarotDeck, tarot: ChatTarot):
        if not msg:
            return gr.update(), chat, gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), Event()
            
        tarot_path, tarot_info, tarot_name = deck.Pick()
        
        chat.append({"role": "user", "content": msg})
        chat.append({"role": "assistant", "content": ""})
        
        sys_prompt, user_prompt = tarot.BuildPrompt(msg, tarot_name, tarot_info)
        
        resp_generator = tarot.Chat(user_prompt)
        
        prompt = f"System: {sys_prompt}\n\nUser: {user_prompt}"
        
        return "", chat, tarot_path, tarot_info, tarot_name, resp_generator, prompt, Event()

    def ShowResponse(self, history: List[Dict[str, str]], resp_generator: Generator, tarot: ChatTarot, stop_event: Event):
        if not resp_generator or isinstance(resp_generator, str):
            return

        try:
            for r in resp_generator:
                if stop_event.is_set():
                    tarot.Stop()
                    break
                history[-1]["content"] = r
                yield history
        except Exception as e:
            history[-1]["content"] = f"Error: {str(e)}"
            yield history

    def Clear(self):
        welcome = [{"role": "assistant", "content": self.persona.welcome}]
        return welcome, None, None, None

    def TriggerStop(self, stop_event):
        if isinstance(stop_event, Event):
            stop_event.set()


def ReadText(fp: str) -> str:
    try:
        with open(fp, "rt", encoding="UTF-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""
