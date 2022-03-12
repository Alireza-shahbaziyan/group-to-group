import os
import random
from pyrogram import (
    Client,
    filters
)
from pyrogram.types import (
    Message,
)
from config import r
from .functions import verify_sudo
from .keyboards import (
    cancel,
    sudo_keyboard
)


@Client.on_message(filters.private & filters.regex('^👥 استخراج اعضای گروه$'))
async def scraper(c: Client, msg: Message):
    if not verify_sudo(msg.from_user.id):
        return

    link = await c.ask(msg.chat.id, '⚙️ لطفا لینک/آیدی گروه مورد نظر را ارسال کنید :\n*برای جمع آوری آیدی از گروه های عمومی، لینک را با @ ارسال کنید.', reply_markup=cancel)

    if link.text == '❌ لغو':
        await msg.reply('🔰 پروسه استخراج اعضای گروه لغو شد!', reply_markup=sudo_keyboard)
        return

    try:
        rnd = random.choice(list(r.smembers('accounts')))
        info = rnd.split('||')
        tempcli = Client(info[0], api_id=info[1], api_hash=info[2])
        await tempcli.start()
    except:
        r.srem('accounts', rnd)
        new_rnd = random.choice(list(r.smembers('accounts')))
        info = new_rnd.split('||')
        tempcli = Client(info[0], api_id=info[1], api_hash=info[2])
        await tempcli.start()

    if link.text.startswith('https://t.me/'):
        group = await tempcli.join_chat(link.text)
    elif link.text.startswith('https://telegram.me/'):
        group = await tempcli.join_chat(link.text)
    elif link.text.startswith('@'):
        group = await tempcli.get_chat(link.text)
    else:
        await msg.reply('❌ لینک اشتباه است! ', reply_markup=sudo_keyboard)
        await tempcli.stop()
        return

    members = []
    inform = await msg.reply('در حال جمع آوری آیدی از گروه مورد نظر ...', reply_markup=sudo_keyboard)
    async for member in tempcli.iter_chat_members(group.id):
        if member.status in ['creator', 'administrator']:
            continue
        elif member.user.is_bot:
            continue
        else:
            if member.user.status in ['within_week', 'within_month', 'long_time_ago']:
                continue
            else:
                if member.user.username:
                    members.append(member.user.username)
                else:
                    continue

    await tempcli.stop()

    with open('user_ids.txt', 'w') as f:
        for member in members:
            f.write(f'{member}\n')

    await msg.reply_document(document='user_ids.txt', caption=f'🆔 `{group.id}`\n👥 `{len(members)}`\n⚙️ {link.text}', reply_markup=sudo_keyboard)
    await inform.delete()
    os.remove('user_ids.txt')
