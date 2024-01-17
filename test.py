import gradio as gr
import random
import time
from threading import Event

# 文字大小寫轉換
# with gr.Blocks() as demo:
    # inn = gr.Textbox(label="輸入")
    # out = gr.Textbox(label="輸出")

    # def foo(inn: str):
    #     return inn.swapcase() # 大小寫轉換

    # inn.change(foo, inn, out)

# 顯示圖片
# with gr.Blocks() as demo:
#     url = "https://i.imgur.com/4IWxkgs.png"
#     img = gr.Image(url, height=300)

# 聊天室元件
# with gr.Blocks() as demo:
#     chat = gr.Chatbot(label="喵星人", height=300)
#     msg = gr.Textbox(label="學貓叫")

#     def send_msg(msg: str, chat: list):
#         r1 = random.randint(1, 5)  # "喵" 的數量
#         r2 = random.randint(1, 3)  # "！" 的數量
#         resp = "喵" * r1 + "！" * r2

#         chat.append([msg, resp]) # 用戶的訊息/機器人回應內容

#         return None, chat

#     msg.submit(send_msg, [msg, chat], [msg, chat])  # 輸入訊息/初始訊息和回應/更新後的訊息和回應

# demo.launch()

# 串流訊息
def get_resp():
    r1 = random.randint(1, 5)  # "喵" 的數量
    r2 = random.randint(1, 3)  # "！" 的數量
    resp = "喵" * r1 + "！" * r2

    for ch in resp:
        time.sleep(0.5)  # 模擬文字傳遞間的延遲
        yield ch # 使用 yield 關鍵字進行串流輸出


with gr.Blocks() as demo:
    event = gr.State(None)
    resp = gr.State(None) # 用於存儲聊天機器人的回應
    chat = gr.Chatbot([[None, "喵！"]], label="喵星人", height=300)
    msg = gr.Textbox(label="學貓叫")
    stop = gr.Button("冷靜！")

    def send_msg(msg: str, chat: list):
        resp = get_resp() # 獲得聊天機器人的回應
        chat.append([msg, None]) # 將用戶的消息添加到聊天記錄中
        return None, chat, resp, Event()

    def show_resp(chat: list, resp, event: Event):
        chat[-1][1] = ""
        for ch in resp:
            if event.is_set():
                event.clear()
                chat[-1][1] += " ..."
                chat.append(["冷靜！", "好吧"])
                yield chat
                break
            chat[-1][1] += ch
            yield chat

    def stop_show(event: Event):
        event.set()

    msg.submit(
      send_msg, [msg, chat], [msg, chat, resp, event] # 輸入: 用戶輸入/聊天紀錄 # 輸出: 用戶輸入/聊天紀錄/機器人回覆
    ).then(show_resp, [chat, resp, event], chat) # 當用戶提交信息後，再調用 `show_resp

    stop.click(stop_show, event, queue=False)

demo.queue().launch()