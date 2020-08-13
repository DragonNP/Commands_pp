from telethon import TelegramClient, events
import logging

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

api_id = '1466003'
api_hash = 'b343987a4f9a7504aa955c34481e671b'

client = TelegramClient('commands_pp', api_id, api_hash)


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
