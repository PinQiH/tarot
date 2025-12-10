from threading import Event
import gradio as gr
from typing import List, Tuple, Any, Generator, Dict

from chat import ChatTarot
from tarot import TarotDeck
from personas import CURRENT_PERSONA
from spreads import SPREADS

class MeowTarotApp:
    def __init__(self):
        css = ReadText("asset/style.css")
        
        # Dark Mystic Theme
        theme = gr.themes.Soft(
            primary_hue=gr.themes.colors.purple,
            secondary_hue=gr.themes.colors.indigo,
            neutral_hue=gr.themes.colors.slate,
            font=[gr.themes.GoogleFont("Noto Sans Mono")]
        ).set(
            body_background_fill="*neutral_950",
            block_background_fill="*neutral_900",
            block_border_width="1px",
            block_title_text_weight="600",
            block_label_text_weight="600",
            block_label_text_size="*text_md"
        )

        self.persona = CURRENT_PERSONA

        # js to force dark mode
        js_func = """
        function refresh() {
            const url = new URL(window.location);
            if (url.searchParams.get('__theme') !== 'dark') {
                url.searchParams.set('__theme', 'dark');
                window.location.href = url.href;
            }
        }
        """

        with gr.Blocks(css=css, theme=theme, title=self.persona.title, js=js_func) as self.app:
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
        self.app.queue().launch(share=True)

    def InitLeftColumn(self):
        with gr.Group():
            self.spread_dropdown = gr.Dropdown(
                choices=[(s.name, s.key) for s in SPREADS.values()],
                value="single",
                label="選擇牌陣",
                interactive=True
            )
            
            self.welcome = [{"role": "assistant", "content": self.persona.welcome}]
            self.chat = gr.Chatbot(label=self.persona.title, value=self.welcome, height=600)
            self.msg = gr.Textbox(label="問題", placeholder="請輸入你想問的問題...", interactive=True)
            with gr.Row():
                self.send = gr.Button("🌙  抽牌", variant="primary")
                self.clear = gr.Button("🗑️  清除")
                self.stop = gr.Button("🛑 停止", variant="stop")
            with gr.Accordion("完整提示", open=False) as self.fold:
                self.debug_msg = gr.TextArea(show_label=False, lines=14)

    def InitRightColumn(self):
        with gr.Group():
            # Gallery for multiple cards
            self.gallery = gr.Gallery(
                label="塔羅牌", 
                show_label=True, 
                elem_id="gallery", 
                columns=[2], 
                rows=[2], 
                object_fit="contain", 
                height="auto"
            )
            self.info = gr.TextArea(label="塔羅牌資訊", lines=20)

    def RegisterEvents(self):
        inn_send = [self.msg, self.spread_dropdown, self.chat, self.deck, self.chat_tarot]
        out_send = [
            self.msg,
            self.chat,
            self.gallery,
            self.info,
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

        out_clear = [self.chat, self.gallery, self.info]
        self.clear.click(self.Clear, None, out_clear)
        self.stop.click(self.TriggerStop, self.stop_event, queue=False)

    def SendMessage(self, msg: str, spread_key: str, chat: List[Dict[str, str]], deck: TarotDeck, tarot: ChatTarot):
        if not msg:
            return gr.update(), chat, gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), Event()
            
        spread = SPREADS[spread_key]
        picked_cards = deck.Pick(spread.card_count)
        
        # Prepare gallery data: list of (image_path, label)
        gallery_data = []
        info_text = ""
        
        for i, (path, info, name) in enumerate(picked_cards):
            position = spread.positions[i] if i < len(spread.positions) else f"位置{i+1}"
            label = f"{position}: {name}"
            gallery_data.append((path, label))
            info_text += f"【{position}】{name}\n{info}\n\n"

        chat.append({"role": "user", "content": msg})
        chat.append({"role": "assistant", "content": ""})
        
        sys_prompt, user_prompt = tarot.BuildPrompt(msg, picked_cards, spread.positions)
        
        resp_generator = tarot.Chat(user_prompt)
        
        prompt = f"System: {sys_prompt}\n\nUser: {user_prompt}"
        
        return "", chat, gallery_data, info_text, resp_generator, prompt, Event()

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
