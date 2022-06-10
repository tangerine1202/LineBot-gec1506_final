from audioop import add
from typing import Text
from linebot.models import (
    QuickReply, QuickReplyButton, LocationAction,
    TextSendMessage, LocationSendMessage
)


def greeting(data):
    name = data['name']
    title = f'Hi, your line id is "{name}"'
    line_msg = TextSendMessage(
        text=title
    )
    return line_msg


def google(data):
    place_id = data['place_id']
    name = data['name']
    address = data['address']
    text = f'place_id: {place_id}\nname: {name}\naddress: {address}'
    line_msg = TextSendMessage(
        text=text,
    )
    return line_msg


def add_user(data):
    title = 'Successfully add user.\nPlease set your location first.'

    quick_replay = QuickReply(
        items=[
            QuickReplyButton(action=LocationAction(label='Set location'))
        ]
    )
    line_msg = TextSendMessage(
        text=title,
        quick_reply=quick_replay
    )
    return line_msg


def set_location(data):
    title = 'Successfully set location'
    lat = data['lat']
    lng = data['lng']
    address = f'{lat}, {lng}'

    line_msg = LocationSendMessage(
        title=title,
        address=address,
        latitude=lat,
        longitude=lng
    )
    return line_msg

def remove_place(data):
    if data == True:
        text = f'Remove successfully'
    else:
        text = f'Fail to remove. This place has not been added'
    line_msg = TextSendMessage(
        text = text
    )
    return line_msg