from mongoengine import connect
from telethon import TelegramClient, events
from telemongo import MongoSession
import logging
import os

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
HOST = os.getenv("HOST")

connect('telethon', host=HOST)
session = MongoSession('telethon', host=HOST)
client = TelegramClient(session,  API_ID, API_HASH)


@client.on(events.NewMessage(pattern='@all'))
async def my_event_handler(event):
    isFirst = True
    chat = event.chat
    users = await client.get_participants(chat)
    msg = ""

    for user in users:
        if user.username is None:
            return
        if not isFirst:
            msg += ", "
        isFirst = False
        msg += "@"
        msg += user.username

    msg += event.raw_text.replace("@all", "")
    await client.send_message(event.chat.id, msg)

client.start()
client.run_until_disconnected()
