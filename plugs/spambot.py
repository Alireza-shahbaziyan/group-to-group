import asyncio
import re
import os

from pyrogram import (
    Client,
    filters
)

from pyrogram.types import (
    Message
)

from pyrogram.errors import (
    RPCError,
    UserDeactivated,
    UserDeactivatedBan,
    SessionRevoked,
)

from .functions import (
    verify_sudo,
)

from .keyboards import (
    sudo_keyboard,
    spambot_text,
    confirm,
)

from config import r


@Client.on_message(filters.private & filters.regex('^♻️ پروسه اسپم بات$'))
async def spambot(api: Client, msg: Message):
    if not verify_sudo(msg.from_user.id):
        return

    reports = list(r.smembers('rep_accounts'))

    respo = await api.ask(msg.from_user.id, spambot_text.format(len(reports)), reply_markup=confirm)

    if respo.text == '❌ لغو':
        await msg.reply('❌ لغو پروسه اسپم بات ...', reply_markup=sudo_keyboard)
        return

    if respo.text != '✅ ادامه':
        await msg.reply('❌ لغو پروسه اسپم بات ... لطفا از دکمه ها استفاده کنید!', reply_markup=sudo_keyboard)
        return

    log = '#uid1337\n\n'
    healthy, reported, spamsent, deleted = 0, 0, 0, 0

    await msg.reply('✅ دستور شروع پروسه ارسال شد!', reply_markup=sudo_keyboard)

    base_text = '♻️ پروسه اسپم بات در حال اجرا است...\n\n🟢 اکانت های سالم : `{}`\n🟡 اکانت های ریپورت : `{}`\n🟣 ارسال پیام خروج از ریپورت به اسپم بات : `{}`\n🔴 دیلیت اکانت/لاگ اوت ها : `{}`'

    info_message = await msg.reply(base_text.format(healthy, reported, spamsent, deleted))

    for client in reports:
        creds = client.split('||')
        temp = Client(creds[0], api_id=creds[1], api_hash=creds[2])
        try:
            await temp.start()
            me = await temp.get_me()
            await temp.unblock_user('@spambot')
            await temp.send_message('@spambot', '/start')
            await asyncio.sleep(1)

            history = await temp.get_history('@spambot', limit=1)
            text = history[0].text

            if re.search(r'^Good news', text) or re.search(r"^مژده", text):
                log += f'[ID: {me.id}][PHONE: {me.phone_number}] Is Not Reported, Adding To Main Database.\n'
                r.srem('rep_accounts', client)
                r.sadd('accounts', client)
                healthy += 1
                await temp.stop()
                pass

            elif re.search(r"limited until(.*)\.", text):
                date = re.search(r"limited until(.*)\.", text).group(0)
                log += f'[ID: {me.id}][PHONE: {me.phone_number}] Is {date.title()}\n'
                reported += 1
                await temp.stop()
                pass

            elif re.search(r"Unfortunately", text):
                log += f'[ID: {me.id}][PHONE: {me.phone_number}] Is Permanently Reported, Sent Message To SpamBot.\n'
                # Send message to spam bot
                spamsent += 1
                await temp.stop()
                pass

            else:
                await temp.stop()
                pass

        except UserDeactivated:
            log += f'[UnKnown] Banned !\n'
            r.srem('rep_accounts', client)
            deleted += 1

        except UserDeactivatedBan:
            log += f'[UnKnown] Banned !\n'
            r.srem('rep_accounts', client)
            deleted += 1

        except SessionRevoked:
            log += f'[UnKnown] Logged Out !\n'
            r.srem('rep_accounts', client)
            deleted += 1

        except RPCError as e:
            log += f'[!!!!] {type(e).__name__} {type(e)} {e}\n'

        await info_message.edit(base_text.format(healthy, reported, spamsent, deleted))
        await asyncio.sleep(0.5)

    with open('spambot_log.txt', 'w') as f:
        f.write(log)

    await info_message.delete()
    await msg.reply_document('spambot_log.txt', caption='♻️ اتمام پروسه اسپم بات ( خروج از ریپورتی )...\n\n🟢 اکانت های سالم : `{}`\n🟡 اکانت های ریپورت : `{}`\n🟣 ارسال پیام خروج از ریپورت به اسپم بات : `{}`\n🔴 دیلیت اکانت/لاگ اوت ها : `{}`'.format(healthy, reported, spamsent, deleted))

    os.remove('spambot_log.txt')
