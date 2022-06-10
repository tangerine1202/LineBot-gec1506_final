import os
from pprint import pprint
from dotenv import load_dotenv

import services
import format_output

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, FollowEvent, TextMessage, LocationMessage
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
def handle_text_message(event):
    text_message_handler(event)


@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    location_message_handler(event)


@handler.add(FollowEvent)
def handle_follow(event):
    follow_handler(event)


@app.route('/text')
def text_message_handler(event=None):
    line_id = event.source.user_id
    user = services.get_user_from_line_id(line_id)

    query = event.message.text
    if query.startswith('greeting'):
        data = services.greeting(user['id'])
        line_msg = format_output.greeting(data)
        line_bot_api.reply_message(event.reply_token, line_msg)
    elif query.startswith('google'):
        text = query.replace('google', '').strip()
        data = services.google(text, user['lat'], user['lng'])
        line_msg = format_output.google(data)
        line_bot_api.reply_message(event.reply_token, line_msg)
    elif query.startswith('remove'):
        text = query.replace('remove', '').strip()
        data = services.remove_place(text, user['id'], user['lat'],user['lng'])
        line_msg = format_output.remove_place(data)
        line_bot_api.reply_message(event.reply_token, line_msg)



@app.route('/follow')
def follow_handler(event=None):
    line_id = event.source.user_id
    data = services.get_user_from_line_id(line_id)
    if data == None:
        data = services.add_user(line_id)
    else:
        print('[info] User already exists, skip adding user')
    line_msg = format_output.add_user(data)
    line_bot_api.reply_message(event.reply_token, line_msg)


@app.route('/location')
def location_message_handler(event=None):
    line_id = event.source.user_id
    user = services.get_user_from_line_id(line_id)

    lat = event.message.latitude
    lng = event.message.longitude
    data = services.set_location(user['id'], lat, lng)
    line_msg = format_output.set_location(data)
    line_bot_api.reply_message(event.reply_token, line_msg)


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 8000
    app.run(host, port)
