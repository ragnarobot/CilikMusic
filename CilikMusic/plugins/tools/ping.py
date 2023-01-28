#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.
import asyncio
from random import shuffle
from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS, MUSIC_BOT_NAME, PING_IMG_URL
from strings import get_command
from CilikMusic import app
from CilikMusic.core.call import Cilik
from CilikMusic.utils import bot_sys_stats
from CilikMusic.utils.decorators.language import language

### Commands
PING_COMMAND = get_command("PING_COMMAND")


@app.on_message(
    filters.command(PING_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@language
async def ping_com(client, message: Message, _):
    response = await message.reply_photo(
        photo=PING_IMG_URL,
        caption=_["ping_1"],
    )
    start = datetime.now()
    pytgping = await Cilik.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    await response.edit_text(
        _["ping_2"].format(
            MUSIC_BOT_NAME, resp, UP, DISK, CPU, RAM, pytgping
        )
    )

def get_arg(message: Message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])

spam_chats = []

@app.on_message(
    filters.command("all", "/")
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
async def tag_com(client, message: Message):
    await message.delete()
    chat_id = message.chat.id
    rep = message.reply_to_message
    text = get_arg(message)
    if not rep and not text:
        return await message.reply("**Berikan Sebuah Teks atau Reply**")

    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ''
    async for usr in client.iter_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}), "
        if usrnum == 5:
            if text:
                txt = f"{text}\n{usrtxt}"
                await app.send_message(chat_id, txt)
            elif rep:
                await rep.reply(usrtxt)
            await sleep(2)
            usrnum = 0
            usrtxt = ''
    try:
        spam_chats.remove(chat_id)
    except:
        pass
    
    
@app.on_message(
    filters.command("cancel", "/")
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
async def tag_cancel(client, message: Message):
    if not message.chat.id in spam_chats:
        return await message.reply("__Not Tagall.__")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("__Stopped Mention.__")    
    
