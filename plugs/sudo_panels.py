import os
import psutil
import time
import datetime
import jdatetime
import asyncio
import re
import random
from pyrogram import errors

from pyrogram import (
    Client,
    client,
    filters
)

from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

from .functions import (
    verify_sudo,
)

from config import r

from .keyboards import (
    temp_del_text,
    sudo_keyboard,
    cancel,
    confirm,
    stop
)

@Client.on_message(filters.private & filters.regex('^🚀 اد گروه$'))
async def add_group(api: Client, msg: Message):
    if not verify_sudo(msg.from_user.id):
        return

    chat_id = msg.chat.id
    origin_link = await api.ask(chat_id, "لینک گروه مبدا را ارسال کنید !", reply_markup=stop)
    if origin_link.text == "برگشت":
        await msg.reply('🔰 عملیات لغو شد !', reply_markup=sudo_keyboard)
        return
    destination_link = await api.ask(chat_id, "لینک گروه مقصد را ارسال کنید !", reply_markup=stop)
    if destination_link.text == "برگشت":
        await msg.reply('🔰 عملیات لغو شد !', reply_markup=sudo_keyboard)
        return

    matchs_origin = re.findall(
        r"([Hh][Tt][Tt][Pp][Ss]|[Hh][Tt][Tt][Pp]):\/\/([Tt][Ee][Ll][Ee][Gg][Rr][Aa][Mm]|[Tt]).[Mm][Ee]\/([a-zA-Z0-9_\-\+\/]+)",
        origin_link.text
    )
    matchs_des = re.findall(
        r"([Hh][Tt][Tt][Pp][Ss]|[Hh][Tt][Tt][Pp]):\/\/([Tt][Ee][Ll][Ee][Gg][Rr][Aa][Mm]|[Tt]).[Mm][Ee]\/([a-zA-Z0-9_\-\+\/]+)",
        destination_link.text
    )

    if len(matchs_origin) != 0:
        origin_link = matchs_origin[0][2]
        if origin_link.startswith("+"):
            origin_link = f"https://t.me/joinchat/{origin_link[1:]}"
        else:
            origin_link = f"https://t.me/{origin_link}"
    else:
        await msg.reply('🔰 لینک یافت نشد !', reply_markup=sudo_keyboard)
        return

    if len(matchs_des) != 0:
        destination_link = matchs_des[0][2]
        if destination_link.startswith("+"):
            destination_link = f"https://t.me/joinchat/{destination_link[1:]}"
        else:
            destination_link = f"https://t.me/{destination_link}"
    else:
        await msg.reply('🔰 لینک یافت نشد !', reply_markup=sudo_keyboard)
        return

    phones = list(r.smembers("accounts"))
    user_ids = []
    account_counter, current, account_counter, privacy, channels, invalid, mutual, now = 0, 0, 0, 0, 0, 0, 0, 0

    txt = f"✅ عملیات اد گروه به گروه با **{len(phones)}** اکانت استارت شد !"
    x = await msg.reply_text(txt)
    print("\n\n")

    for phone in r.smembers("accounts"):
        peer_flood, channel_private = 0, False
        account_counter += 1
        account_current = 0
        is_limit = False

        info = phone.split('||')
        account = Client(info[0], api_id=info[1], api_hash=info[2])
        await account.start()
        print(f"{account_counter} - client started ! >>", info[0])
        try:
            og = await account.join_chat(origin_link)
            print("   - joined origin group !")
            await asyncio.sleep(3)
        except errors.UserAlreadyParticipant:
            og = await account.get_chat(origin_link)
        except Exception as e:
            print(e)
            continue
        try:
            dg = await account.join_chat(destination_link)
            print("   - joined destination group !")
            if account_counter == 1:
                chat = await account.get_chat(destination_link)
                if chat.permissions.can_invite_users is False:
                    await msg.reply_text("افزودن اعضا در گروه مقصد قفل می باشد ❌", quote=False)
                    await account.leave_chat(dg.id, delete=True)
                    await account.leave_chat(og.id, delete=True)
                    break
        except errors.UserAlreadyParticipant:
            dg = await account.get_chat(destination_link)
        except Exception as e:
            print(e)
            continue

        try:
            async for member in account.iter_chat_members(og.id, filter="all"):
                if peer_flood == 10:
                    is_limit = True
                    break
                if member.user.is_bot is False and not member.user.id in user_ids:
                    user_ids.append(member.user.id)
                    try:
                        await account.add_chat_members(dg.id, member.user.id)
                        account_current += 1
                        peer_flood = 0
                    except errors.PeerFlood:
                        peer_flood += 1
                    except errors.UserKicked:
                        continue
                    except errors.UserNotMutualContact:
                        mutual += 1
                    except errors.UserChannelsTooMuch:
                        channels += 1
                    except errors.UserIdInvalid:
                        invalid += 1
                    except errors.UserPrivacyRestricted:
                        privacy += 1
                    except errors.UserBannedInChannel:
                        is_limit = True
                        break
                    except Exception as e:
                        print("inside", phone, e)

        except errors.ChannelPrivate:
            channel_private = True
        except Exception as e:
            pass
        finally:
            print("   - Total added >>", account_current)
            print("   - PeerFlood >>", peer_flood)
            print("   - UserNotMutualContact >>", mutual)
            print("   - UserChannelsTooMuch >>", channels)
            print("   - UserIdInvalid >>", invalid)
            print("   - UserPrivacyRestricted >>", privacy)
            if channel_private:
                await account.leave_chat(dg.id, delete=True)
                print("   - left from destination group !")
                await msg.reply_text(f"Supergroup is private ❌")
                return
            else:
                await account.leave_chat(dg.id, delete=True)
                print("   - left from destination group !")
                await account.leave_chat(og.id, delete=True)
                print("   - left from origin group !")
            e = int((await account.get_chat(destination_link)).members_count)
            if e >= now or is_limit is False: break
    if len(phones) != 0:
        txt += f"\n\n✅ تعداد اعضای گروه بعد از پایان : **{e}**"
    try:
        await api.edit_message_text(x.chat.id, x.message_id, txt)
    except: pass
    await msg.reply_text(f"""
♻ Checked users : **{len(user_ids)}**

🔆 Number of accounts : **{account_counter}**
✅ Number of additions : **{current}**

⚠ Privacy : **{privacy}**
⚠ Channels too much : **{channels}**
⚠ User id invalid : **{invalid}**
⚠ User not mutual contact : **{mutual}**
""", reply_markup=sudo_keyboard)

@Client.on_message(filters.private & filters.regex('^🏷 وضعیت ربات$'))
async def _bot_status(api: Client, msg: Message):
    if not verify_sudo(msg.from_user.id):
        return

    # OS Vars
    pid = os.getpid()
    cpu = psutil.cpu_percent()
    py = psutil.Process(pid)
    used = round(py.memory_info()[0] / 1024 / 1024, 1)
    available = round(psutil.virtual_memory().available *
                      100 / psutil.virtual_memory().total, 1)
    sys_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    me = await api.get_me()
    await msg.reply(f'🌡 **CPU Usage** : `{cpu}%`\n💾 **RAM Usage** : `{used}MB`\n⚙️ **Available RAM** : `{available}%`\n🕔 **System Time** : `{sys_time}`\n**👑 [{me.first_name}](https://t.me/{me.username})**', disable_web_page_preview=True, reply_markup=sudo_keyboard)


@Client.on_message(filters.private & filters.regex('^🧮 آمار ربات$'))
async def _bot_stats(_, msg: Message):
    if not verify_sudo(msg.from_user.id):
        return

    # Stats Vars
    healthy_accounts = len(list(r.smembers('accounts')))
    reported_accounts = len(list(r.smembers('rep_accounts')))
    all_accounts = healthy_accounts + reported_accounts
    admins = len(list(r.smembers('admins')))
    sudos = len(list(r.smembers('sudos')))

    x = await msg.reply('🏷 در حال تهیه گزارش از ربات ...', reply_markup=sudo_keyboard)
    await asyncio.sleep(0.5)
    await x.delete()
    await msg.reply(f'🏷 گزارش از ربات تهیه شد!\n\n🔰 تعداد اکانت ها : `{all_accounts}` ( `{healthy_accounts}` سالم / `{reported_accounts}` ریپورت )\n👮🏻‍♂️ تعداد ادمین ها : `{admins}`\n💻 تعداد سودو ها : `{sudos}`', reply_markup=sudo_keyboard)


@Client.on_message(filters.private & filters.regex('^👀 مشاهده اطلاعات سفارش$'))
async def _banner_info(api: Client, msg: Message):
    if not verify_sudo(msg.from_user.id):
        return

    banner_id = await api.ask(msg.from_user.id, '🆔 آیدی ( شناسه ) سفارش را ارسال کنید', reply_markup=cancel)

    if banner_id.text == '❌ لغو':
        await msg.reply('🔰 پروسه مشاهده اطلاعات سفارش لغو شد!', reply_markup=sudo_keyboard)
        return

    database_info = r.get(banner_id.text)

    if not database_info:
        await msg.reply('⚠️ شناسه ارسالی توسط شما در دیتابیس ربات وجود ندارد!', reply_markup=sudo_keyboard)
        return

    vals = database_info.split('//')

    start_time = jdatetime.datetime.fromtimestamp(int(vals[3]))
    myTime = start_time.strftime('%d, %B, %Y - %X')

    await msg.reply(f'💬 اطلاعات بنر ( `{banner_id.text}` )\n🟢 ارسال موفق : `{vals[0]}`\n🔴 ارسال ناموفق : `{vals[1]}`\n⚠️ اکانت های ریپورت/فلود شده در این سفارش : `{vals[2]}`\n⏰ زمان ثبت سفارش :\n`{myTime}`', reply_markup=sudo_keyboard)


@Client.on_message(filters.private & filters.regex('^👤 مشاهده موجودی کاربر$'))
async def _user_info(api: Client, msg: Message):
    if not verify_sudo(msg.from_user.id):
        return

    user_id = await api.ask(msg.from_user.id, '🆔 آیدی عددی کاربر مورد نظر را ارسال کنید', reply_markup=cancel)

    if user_id.text == '❌ لغو':
        await msg.reply('🔰 پروسه مشاهده موجودی کاربر لغو شد!', reply_markup=sudo_keyboard)
        return

    database_info = r.get(user_id.text)

    if not database_info:
        await msg.reply('⚠️ کاربر ارسالی توسط شما در دیتابیس ربات وجود ندارد و یا موجودی این کاربر صفر است!', reply_markup=sudo_keyboard)
        return

    zero = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('❌ صفر کردن موجودی کاربر',
                                 'zero_%s' % user_id.text)
        ]
    ])
    await msg.reply('✅', reply_markup=sudo_keyboard)
    await msg.reply(f'🗄 اطلاعات ( `{user_id.text}` ) :\n📲 اکانت های غیر ریپورت اضافه شده به ربات توسط این کاربر `{database_info}` عدد می باشد.', reply_markup=zero)


@Client.on_message(filters.private & filters.regex('^👀 مشاهده اطلاعات سفارش زنده$'))
async def live_report(api: Client, msg: Message):
    if not verify_sudo(msg.from_user.id):
        return

    banner_id = await api.ask(msg.from_user.id, '🆔 آیدی ( شناسه ) سفارش را ارسال کنید', reply_markup=cancel)

    if banner_id.text == '❌ لغو':
        await msg.reply('🔰 پروسه مشاهده اطلاعات سفارش لغو شد!', reply_markup=sudo_keyboard)
        return

    ttl = await api.ask(msg.from_user.id, '⏰ زمان مورد نظر برای مشاهده وضعیت را به صورت عدد انگلیسی ارسال کنید ( زمان بر حسب ثانیه )', reply_markup=cancel)

    if ttl.text == '❌ لغو':
        await msg.reply('🔰 پروسه مشاهده اطلاعات سفارش لغو شد!', reply_markup=sudo_keyboard)
        return

    database_info = r.get(banner_id.text)

    if not database_info:
        await msg.reply('⚠️ شناسه ارسالی توسط شما در دیتابیس ربات وجود ندارد!', reply_markup=sudo_keyboard)
        return

    vals = database_info.split('//')
    start_time = jdatetime.datetime.fromtimestamp(int(vals[3]))
    myTime = start_time.strftime('%d, %B, %Y - %X')

    await msg.reply('ℹ️ وضعیت زنده سفارش تا لحظاتی دیگر برای شما ارسال میشود...', reply_markup=sudo_keyboard)

    base_text = '💬 اطلاعات بنر ( `{}` )\n🟢 ارسال موفق : `{}`\n🔴 ارسال ناموفق : `{}`\n⚠️ اکانت های ریپورت/فلود شده در این سفارش : `{}`\n⏰ زمان ثبت سفارش :\n`{}`\n* اتمام مشاهده وظعیت زنده در `{}` ثانیه دیگر'
    base = await msg.reply(base_text.format(
        banner_id.text,
        vals[0],
        vals[1],
        vals[2],
        myTime,
        ttl.text
    ))

    dec = int(ttl.text)

    for i in range(int(ttl.text)):
        dec = dec - 1
        database_info = r.get(banner_id.text)
        new_vals = database_info.split('//')
        await base.edit(base_text.format(
            banner_id.text,
            new_vals[0],
            new_vals[1],
            new_vals[2],
            myTime,
            dec
        ))
        await asyncio.sleep(1)


@Client.on_message(filters.private & filters.regex('^♻️ تهیه بکاپ$'))
async def make_db_backup(api: Client, msg: Message):
    if not verify_sudo(msg.from_user.id):
        return

    accounts = list(r.smembers('accounts'))
    rep_accounts = list(r.smembers('rep_accounts'))
    file = ''
    rep_file = ''

    x = await msg.reply('♻️ در حال تهیه نسخه پشتیبان از دیتابیس ربات...')

    for account in accounts:
        file += f'{account}\n'

    with open('accounts.txt', 'w') as f:
        f.write(file)

    await msg.reply_document('accounts.txt', caption=f'✅ نسخه پشتیبان اکانت های سالم ربات\n🟢تعداد : {len(accounts)}')

    os.remove('accounts.txt')

    if len(rep_accounts) > 1:
        for account in rep_accounts:
            rep_file += f'{account}\n'

        with open('rep_accounts.txt', 'w') as f:
            f.write(rep_file)

        await msg.reply_document('rep_accounts.txt', caption=f'✅ نسخه پشتیبان اکانت های ریپورت ربات\n🟠تعداد : {len(rep_accounts)}')

        os.remove('rep_accounts.txt')

    await x.delete()


@Client.on_message(filters.private & filters.regex('^🗑 پاکسازی لیست موقت کاربران$'))
async def clean_temp(api: Client, msg: Message):
    if not verify_sudo(msg.from_user.id):
        return
    temp_users = len(r.smembers('temp_sent'))
    conf = await api.ask(msg.from_user.id, temp_del_text.format(temp_users), reply_markup=confirm)

    if conf.text == '❌ لغو':
        await msg.reply('❌ پاکسازی لیست موقتی لغو شد', reply_markup=sudo_keyboard)
        return

    r.delete('temp_sent')

    await msg.reply('✅ لیست موقت کاربران با موفقیت حذف شد.', reply_markup=sudo_keyboard)


@Client.on_message(filters.private & filters.regex('^ℹ️ مشاهده سفارش های کاربر$'))
async def user_procs(api: Client, msg: Message):
    if not verify_sudo(msg.from_user.id):
        return

    user_id = await api.ask(msg.from_user.id, 'ℹ️ آیدی عددی کاربر مورد نظر را ارسال کنید.', reply_markup=cancel)

    if user_id.text == '❌ لغو':
        await msg.reply('❌ مشاهده سفارش های کاربر لغو شد', reply_markup=sudo_keyboard)
        return
    
    procs_list = list(r.smembers(f'{user_id.text}PROCS'))
    
    text = f'ℹ️ سفارش های ثبت شده توسط کاربر `{user_id.text}` :\n\n'

    if len(procs_list) < 0:
        await msg.reply('⚠️ کاربر مورد نظر تابحال سفارشی ثبت نکرده است...', reply_markup=sudo_keyboard)
        return
    
    for sef in procs_list:
        text += f'`{sef}` • '

    await msg.reply(text, reply_markup=sudo_keyboard)


@Client.on_message(filters.private & filters.regex('^ℹ️ مشاهده آخرین سفارش$'))
async def last_proc(_, msg: Message):
    if not verify_sudo(msg.from_user.id):
        return
    
    await msg.reply(f'✅ شناسه آخرین سفارش ثبت شده در ربات » {r.get("last_proc")}')


@Client.on_message(filters.private & filters.regex('🔄 راه اندازی مجدد ربات'))
async def reboot(_, msg: Message):
    if not verify_sudo(msg.from_user.id):
        return
    
    await msg.reply('**🔄 ربات با موفقیت راه اندازی مجدد شد!**')
    os.system('screen -X -S sender quit && screen -AmdS sender python3 main.py')


@Client.on_callback_query(group=-1)
async def _sudo_callbacks(_, query: CallbackQuery):
    if query.data.startswith('zero_'):
        user_id = query.data.split('_')[1]
        r.delete(user_id)

        await query.answer(f'✅ موجودی کاربر {user_id} صفر شد!', show_alert=True)
        await query.message.edit(query.message.text + '\n\n* **موجودی این کاربر صفر شده، برای داشتن گزارش، اطلاعات قبلی این پیام ادیت نخواهد شد.**', reply_markup=sudo_keyboard)

    else:
        pass
