# Main Plugin For Sender
from logging import info
import os
import asyncio
import random
import time

from pyrogram import (
    Client,
    filters
)
from pyrogram.errors.exceptions.unauthorized_401 import UserDeactivated

from pyrogram.types import (
    Message
)

from pyrogram.raw import functions

from pyrogram.errors import (
    PeerFlood,
    FloodWait,
    UsernameNotOccupied,
    RPCError,
    UserDeactivatedBan,
)

from .functions import (
    verify_sudo,
    generate_string,
    calc_banner
)

from .keyboards import (
    sudo_keyboard,
    confirm
)
from config import r


# Client placeholder
async def ___Client(creds: list = None, usernames: list = None, banners: list = None, banner_id: str = None, sleep_between: int = None):
    credentials = creds.split('||')
    temp = Client(credentials[0], api_id=credentials[1], api_hash=credentials[2])
    try:
        await temp.start()
    except UserDeactivatedBan:
        calc_banner(banner_id, 3)
        r.srem('accounts', creds)
        return
    except UserDeactivated:
        calc_banner(banner_id, 3)
        r.srem('accounts', creds)
        return
    
    for user in usernames:
        if user in r.smembers('temp_sent'):
            continue
        else:
            try:
                await temp.send(
                    functions.contacts.ResolveUsername(username=user)
                )
                await temp.send_message(
                    chat_id=user, text=random.choice(banners)
                )
                calc_banner(banner_id, 1)
                r.sadd('temp_sent', user)
                await asyncio.sleep(sleep_between)
            except PeerFlood:
                r.srem('accounts', creds)
                r.sadd('rep_accounts', creds)
                calc_banner(banner_id, 3)
            except FloodWait as ex:
                calc_banner(banner_id, 1)
                await asyncio.sleep(ex.x)
            except UsernameNotOccupied:
                calc_banner(banner_id, 2)
            except RPCError as e:
                with open('unk_errors.txt', 'w') as f:
                    f.write(f'[#] {type(e).__name__} {type(e)} {e}\n\n')
                    print(f'[#] {type(e).__name__} {type(e)} {e}\n\n')

    await temp.stop()
    return


@Client.on_message(filters.private & filters.regex('^🚀 شروع ارسال به پیوی$'))
async def _sender(api: Client, msg: Message):
    if not verify_sudo(msg.from_user.id):
        return

    user_file: Message = await api.ask(msg.from_user.id, '📂 لطفا فایل آیدی ( یوزرنیم ) برای ارسال به پیوی را ارسال کنید.')

    if not user_file.media:
        await msg.reply('⚠️ فایلی در پیام ارسالی توسط شما تشخیص داده نشد! لغو پروسه ...')
        return

    if not user_file.document:
        await user_file.reply('⚠️ فایل ارسالی توسط شما به عنوان فایل یوزرنیم تشخیص داده نشد! لغو پروسه ...')
        return

    user_file = await user_file.download()

    accounts = list(r.smembers('accounts'))
    accounts_index = 0
    banners = []

    f = open(user_file, 'r')
    usernames = [user.strip() for user in f.readlines()][:-1]
    f.close()
    os.remove(user_file)

    banner_count = await api.ask(msg.from_user.id, '⚙️ تعداد بنر های این سفارش را تنها با ارسال اعداد انگلیسی مشخص کنید.')

    for count in range(int(banner_count.text)):
        temp_banner = await api.ask(msg.from_user.id, f'📥 بنر شماره {count + 1} را ارسال کنید.')
        banners.append(temp_banner.text)

    sleeps = await api.ask(msg.from_user.id,  '⚙️ وقفه زمانی بین هر ارسال را تنها با ارسال عدد انگلیسی مشخص کنید.')

    banner_id = await generate_string(8)

    # Success, fail, reported.
    r.set(banner_id, f'0//0//0//{int(time.time())}')

    if len(accounts) > len(usernames):
        send_per_acc = int(len(accounts) / len(usernames))
    else:
        send_per_acc = int(len(usernames) / len(accounts))

    confirmation = await api.ask(msg.from_user.id, '❓ از انجام این سفارش مطمئن هستید؟', reply_markup=confirm)
    
    if confirmation.text == '❌ لغو':
        await msg.reply('🔰 سفارش با موفقیت لغو شد!', reply_markup=sudo_keyboard)
        return
    
    r.sadd(f'{msg.from_user.id}PROCS', banner_id)
    r.set('last_proc', banner_id)
    
    infomsg = await msg.reply('**ℹ️ دستور ارسال به پیوی به اکانت ها ارسال شد، پروسه تا لحظاتی دیگر شروع میشود...**', reply_markup=sudo_keyboard)
    await asyncio.sleep(0.5)
    await infomsg.delete()

    estimated = send_per_acc * int(sleeps.text)
    estimated += (estimated * .01)
    
    await msg.reply(f'**ℹ️ پروسه ارسال به پیوی شروع شد.**\nشناسه این سفارش `{banner_id}` میباشد، شما میتوانید از قسمت "مشاهده اطلاعات سفارش" این سفارش را پیگیری کنید.\n⏰ زمان تقریبی اتمام : `{int(estimated)}` ثانیه به ازای هر اکانت.', reply_markup=sudo_keyboard)

    for x in range(0, len(usernames), send_per_acc):
        pass_to_client = usernames[x:x+send_per_acc]
        creds = accounts[accounts_index]

        asyncio.create_task(___Client(
            creds=creds, usernames=pass_to_client, banners=banners, banner_id=banner_id, sleep_between=int(sleeps.text)))
        await asyncio.sleep(1)

        if accounts_index >= len(accounts) - 1:
            accounts_index = 0
        else:
            accounts_index += 1
