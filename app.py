import os
from pprint import pprint
from dotenv import load_dotenv

import placeApi

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

# load the environment variables from .env file
load_dotenv()

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('LINE_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_SECRET'))


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
    text = event.message.text
    # text: "add 7-11"
    if text.startswith('add'):
        data = add_place('7-11')

        res = format_add_place_output(data)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=res)
        )
    elif text.startswith('find'):
        data = get_place('7-11')

        res = format_get_place_output(data)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=res)
        )

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 8000
    app.run(host, port)
