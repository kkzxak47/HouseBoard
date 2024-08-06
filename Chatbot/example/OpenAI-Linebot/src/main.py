import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from src.llm import LLM

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
working_status = os.getenv("DEFALUT_TALKING", default="true").lower() == "true"

app = Flask(__name__)
llm = LLM()


# domain root
@app.route("/")
def home():
    return llm.prompt.generate_prompt()


@app.route("/webhook", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)    
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global working_status

    try:
        if event.message.type != "text":
            return

        user_text = event.message.text

        commands = {
            "呼叫小小汪": ("幹嘛 >_<", True),
            "睡吧小小汪": ("我滾去睡囉zzZ", False),
            "查看記憶": (llm.show_memory(), None),
            "小小汪指令集": (
                    "開機：'呼叫小小汪'\n" + 
                    "睡眠：'睡吧小小汪'\n" + 
                    "更新系統記憶：'輸入記憶'\n" + 
                    "查看目前記憶：'查看記憶'", None)
        }

        if user_text in commands:
            reply_text, status = commands[user_text]
            if status is not None:
                working_status = status
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
            return

        if user_text.startswith('輸入記憶'):
            new_memory = user_text[4:].strip()
            llm.update_memory(new_memory)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="記憶已更新"))
            return

        if working_status:
            llm.add_msg(user_text, "user")
            reply_msg = llm.get_response()
            llm.add_msg(reply_msg, "ai")
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_msg))

    except Exception as e:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str(e)))


if __name__ == "__main__":
    app.run()
