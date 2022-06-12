from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
  return 'Hello, world'

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('BMqpLfPosojbQAL533c6DZWxMSQ0KvDGOBYf1kInSDw0p1V0BAaLjhMoRaIaqVi/qqYZqOMYKKbSYdHZhkUGX96D10Sc8sjWyXro6qcZcAU0mPzqtzWQuAdyPwhtelpFvexhDq9RIIQ+4FQJl8pchAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('869127243db84fc5cd002093801194ef')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == '__main__':
  host = '0.0.0.0'
  port = 8000
  app.run(host, port)