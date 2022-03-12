from pyrogram.methods import auth
from pyromod import listen

import os
import asyncio
import re
from pyrogram import (
    Client,
    filters
)

from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

from pyrogram.raw import functions

from pyrogram.errors import (
    RPCError,
    ApiIdInvalid,
    ApiIdPublishedFlood,
    SessionPasswordNeeded,
    PasswordHashInvalid,
    PeerFlood,
    UserDeactivated,
    UserDeactivatedBan,
    SessionRevoked,
)

from config import r

from .functions import (
    add_to_user,
    generate_bio,
    generate_pfp,
    generate_info,
    all_check,
    generate_string,
    generate_username,
    add_to_user,
    verify_sudo
)

from .keyboards import (
    sudo_keyboard,
    all_keyboard,
    cancel,
    accounts_panel,
    accounts_panel_text,
)


# Message Handlers
@Client.on_message(
    filters.private & (filters.regex('^➕ اهدای اکانت$') |
                       filters.command(['addaccount', 'ادد اکانت'], ['', '/']))
)
async def _account_reciever(api: Client, msg: Message):
    if not all_check(msg.from_user.id):
        return

    # Ask credentials
    try:
        phone = await api.ask(msg.from_user.id, '📱 شماره تلفن مورد نظر خود را ارسال کنید :\nنمونه :\n `+989330001111`', reply_markup=cancel)
    except asyncio.exceptions.TimeoutError:
        if verify_sudo(msg.from_user.id):
            await msg.reply('❌ کاربر گرامی، زمان پاسخگویی شما به ربات به اتمام رسیده است، برای ادامه لطفا مجددا از دکمه ها برای ارتباط با ربات استفاده کنید.', reply_markup=sudo_keyboard)
        else:
            await msg.reply('❌ کاربر گرامی، زمان پاسخگویی شما به ربات به اتمام رسیده است، برای ادامه لطفا مجددا از دکمه ها برای ارتباط با ربات استفاده کنید.', reply_markup=all_keyboard)
        return

    if phone.text == '❌ لغو':
        if verify_sudo(msg.from_user.id):
            await msg.reply('🔰 پروسه اهدای اکانت لغو شد!', reply_markup=sudo_keyboard)
            return
        else:
            await msg.reply('🔰 پروسه اهدای اکانت لغو شد!', reply_markup=all_keyboard)
            return

    match = re.findall(r'\d+', phone.text)
    phone.text = ''.join(match)
    phone.text = f'+{phone.text}'

    if phone.text in r.smembers('phones'):
        if verify_sudo(msg.from_user.id):
            await msg.reply('🚫 شماره ارسال شده توسط شما از قبل به ربات اهدا شده است، لطفا اقدام به ارسال شماره دیگری بکنید...', reply_markup=sudo_keyboard)
            return
        else:
            await msg.reply('🚫 شماره ارسال شده توسط شما از قبل به ربات اهدا شده است، لطفا اقدام به ارسال شماره دیگری بکنید...', reply_markup=all_keyboard)
            return

    await msg.reply(f'📱 شماره دریافت شده : `{phone.text}`')

    try:
        api__id = await api.ask(msg.from_user.id, '🧰 لطفا **Api ID** اکانت مورد نظر را ارسال کنید.', reply_markup=cancel)
    except asyncio.exceptions.TimeoutError:
        if verify_sudo(msg.from_user.id):
            await msg.reply('❌ کاربر گرامی، زمان پاسخگویی شما به ربات به اتمام رسیده است، برای ادامه لطفا مجددا از دکمه ها برای ارتباط با ربات استفاده کنید.', reply_markup=sudo_keyboard)
        else:
            await msg.reply('❌ کاربر گرامی، زمان پاسخگویی شما به ربات به اتمام رسیده است، برای ادامه لطفا مجددا از دکمه ها برای ارتباط با ربات استفاده کنید.', reply_markup=all_keyboard)
        return

    if api__id.text == '❌ لغو':
        if verify_sudo(msg.from_user.id):
            await msg.reply('🔰 پروسه اهدای اکانت لغو شد!', reply_markup=sudo_keyboard)
            return
        else:
            await msg.reply('🔰 پروسه اهدای اکانت لغو شد!', reply_markup=all_keyboard)
            return

    try:
        int(api__id.text)
    except ValueError:
        if verify_sudo(msg.from_user.id):
            await msg.reply('⚠️ شناسه **Api-ID** باید فقط به صورت عدد انگلیسی ارسال شود!', reply_markup=sudo_keyboard)
            return
        else:
            await msg.reply('⚠️ شناسه **Api-ID** باید فقط به صورت عدد انگلیسی ارسال شود!', reply_markup=all_keyboard)
            return

    try:
        api__hash = await api.ask(msg.from_user.id, '🧰 لطفا **Api Hash** اکانت مورد نظر را ارسال کنید.', reply_markup=cancel)
    except asyncio.exceptions.TimeoutError:
        if verify_sudo(msg.from_user.id):
            await msg.reply('❌ کاربر گرامی، زمان پاسخگویی شما به ربات به اتمام رسیده است، برای ادامه لطفا مجددا از دکمه ها برای ارتباط با ربات استفاده کنید.', reply_markup=sudo_keyboard)
        else:
            await msg.reply('❌ کاربر گرامی، زمان پاسخگویی شما به ربات به اتمام رسیده است، برای ادامه لطفا مجددا از دکمه ها برای ارتباط با ربات استفاده کنید.', reply_markup=all_keyboard)
        return

    if api__hash.text == '❌ لغو':
        if verify_sudo(msg.from_user.id):
            await msg.reply('🔰 پروسه اهدای اکانت لغو شد!', reply_markup=sudo_keyboard)
            return
        else:
            await msg.reply('🔰 پروسه اهدای اکانت لغو شد!', reply_markup=all_keyboard)
            return

    # Start Temp Client And Process.
    try:
        temp_client = Client(
            ':memory:', api_id=api__id.text, api_hash=api__hash.text)
        await temp_client.connect()
        creds = await temp_client.send_code(phone_number=phone.text)
    except ApiIdInvalid:
        await msg.reply('⚠️ خطا! **Api ID** و یا **Api Hash** ارسالی توسط شما اشتباه میباشد.')
        return
    except ApiIdPublishedFlood:
        await msg.reply('⚠️ خطا! Api ID / Hash ارسالی توسط شما از سمت سرور تلگرام بلاک شده. لطفا از مشخصات دیگری استفاده کنید.')
        return
    try:
        auth_code = await api.ask(msg.from_user.id, '🔢 کد ارسال شده برای اکانت را وارد کنید :', reply_markup=cancel)
    except asyncio.exceptions.TimeoutError:
        await temp_client.disconnect()
        if verify_sudo(msg.from_user.id):
            await msg.reply('❌ کاربر گرامی، زمان پاسخگویی شما به ربات به اتمام رسیده است، برای ادامه لطفا مجددا از دکمه ها برای ارتباط با ربات استفاده کنید.', reply_markup=sudo_keyboard)
        else:
            await msg.reply('❌ کاربر گرامی، زمان پاسخگویی شما به ربات به اتمام رسیده است، برای ادامه لطفا مجددا از دکمه ها برای ارتباط با ربات استفاده کنید.', reply_markup=all_keyboard)
        return

    if auth_code.text == '❌ لغو':
        if verify_sudo(msg.from_user.id):
            await msg.reply('🔰 پروسه اهدای اکانت لغو شد!', reply_markup=sudo_keyboard)
            return
        else:
            await msg.reply('🔰 پروسه اهدای اکانت لغو شد!', reply_markup=all_keyboard)
            return
    try:

        await temp_client.sign_in(
            phone_number=phone.text,
            phone_code=auth_code.text,
            phone_code_hash=creds.phone_code_hash
        )

        # timer = await msg.reply('✅ ربات با موفقیت وارد اکانت شد، لطفا تا 120 ثانیه دیگر همه نشست های اکانت را بجز ربات از اکانت خارج کنید، همچنین خودتان از اکانت لاگ اوت کنید تا اکانت به موجودی شما اضافه شود.\n⏳ زمان باقیمانده : ')
        #
        # for i in range(60):
        #     await asyncio.sleep(1)
        #     await timer.edit(f'✅ ربات با موفقیت وارد اکانت شد، لطفا تا 120 ثانیه دیگر همه نشست های اکانت را بجز ربات از اکانت خارج کنید، همچنین خودتان از اکانت لاگ اوت کنید تا اکانت به موجودی شما اضافه شود.\n⏳ زمان باقیمانده : `{60 - i}`')
        #
        # auths = await temp_client.send(functions.account.GetAuthorizations())
        # s = [1 for a in auths.authorizations]
        # if not len(s) == 1:
        #     await timer.delete()
        #     if verify_sudo(msg.from_user.id):
        #         await msg.reply('ℹ️ اکانت وارد شده توسط شما دارای نشست های فعال میباشد و به ربات اضافه نمیشود، لطفا مجددا اقدام به اضافه کردن اکانت کنید.', reply_markup=sudo_keyboard)
        #     else:
        #         await msg.reply('ℹ️ اکانت وارد شده توسط شما دارای نشست های فعال میباشد و به ربات اضافه نمیشود، لطفا مجددا اقدام به اضافه کردن اکانت کنید.', reply_markup=all_keyboard)
        #     await temp_client.log_out()
        #     return
        #
        # await timer.delete()

        temp_user = await temp_client.get_me()

        await temp_client.unblock_user('@spambot')
        await temp_client.send_message('@spambot', '/start')
        await asyncio.sleep(0.5)
        resp = await temp_client.get_history('@spambot', limit=1)
        text = resp[0].text

        if re.search(r'^Good news', text) or re.search(r"^مژده", text):
            try:
                try:
                    await temp_client.set_profile_photo(photo=await generate_pfp())
                except Exception as err:
                    print(
                        f'[PROFILE PIC ERROR] {type(err).__name__} {type(err)} {err}')
                    pass
                try:
                    await temp_client.update_profile(first_name=await generate_info(), bio=await generate_bio())
                except Exception as err:
                    print(
                        f'[NAME OR BIO ERROR] {type(err).__name__} {type(err)} {err}')
                    pass
                try:
                    await temp_client.update_username(username=await generate_username(12))
                except Exception as err:
                    print(
                        f'[USERNAME ERROR] {type(err).__name__} {type(err)} {err}')
                    pass

                passwd = await generate_string(16)
                print(
                    f'[ID: {temp_user.id}][PHONE : {phone.text}] PASSWORD : {passwd}')
                await temp_client.enable_cloud_password(password=passwd, hint='dev. uid1337')

            except Exception as e:
                print(f'{type(e).__name__} {type(e)} {e}')
                pass

            ses = await temp_client.export_session_string()
            add_to_user(msg.from_user.id)

            r.sadd('phones', phone.text)

            r.sadd(
                'accounts', f'{ses}||{api__id.text}||{api__hash.text}||{passwd}')

            if verify_sudo(msg.from_user.id):
                await msg.reply(f'✅ اکانت با موفقیت به دیتابیس ربات اضافه شد. اطلاعات اکانت:\n📱 Phone Number: `{phone.text}`\n⚙️ User ID : `{temp_user.id}`\n{"🆔 Username: " + f"`{temp_user.username}`" if temp_user.username else ""}', reply_markup=sudo_keyboard)
            else:
                await msg.reply(f'✅ اکانت با موفقیت به دیتابیس ربات اضافه شد. اطلاعات اکانت:\n📱 Phone Number: `{phone.text}`\n⚙️ User ID : `{temp_user.id}`\n{"🆔 Username: " + f"`{temp_user.username}`" if temp_user.username else ""}', reply_markup=all_keyboard)
            await temp_client.join_chat('@iMat1n')
            await temp_client.disconnect()

        # else:
        #
        #     await msg.reply('⚠️ اکانت وارد شده توسط شما ریپورت است. ربات از اکانت خارج میشود و این اکانت به تعداد اکانت های اضافه شده توسط شما اضافه نمیشود.')
        #     await temp_client.log_out()

    except SessionPasswordNeeded:
        try:
            two_factor = await api.ask(msg.from_user.id, '🔐 اکانت وارد شده دارای تایید دومرحله ای میباشد. لطفا گذرواژه دوم اکانت را ارسال کنید :')
        except asyncio.exceptions.TimeoutError:
            await temp_client.disconnect()
            if verify_sudo(msg.from_user.id):
                await msg.reply('❌ کاربر گرامی، زمان پاسخگویی شما به ربات به اتمام رسیده است، برای ادامه لطفا مجددا از دکمه ها برای ارتباط با ربات استفاده کنید.', reply_markup=sudo_keyboard)
            else:
                await msg.reply('❌ کاربر گرامی، زمان پاسخگویی شما به ربات به اتمام رسیده است، برای ادامه لطفا مجددا از دکمه ها برای ارتباط با ربات استفاده کنید.', reply_markup=all_keyboard)
            return

        try:

            await temp_client.check_password(two_factor.text)

            # timer = await msg.reply('✅ ربات با موفقیت وارد اکانت شد، لطفا تا 120 ثانیه دیگر همه نشست های اکانت را بجز ربات از اکانت خارج کنید، همچنین خودتان از اکانت لاگ اوت کنید تا اکانت به موجودی شما اضافه شود.\n⏳ زمان باقیمانده : ')
            #
            # for i in range(20):
            #     await asyncio.sleep(1)
            #     await timer.edit(f'✅ ربات با موفقیت وارد اکانت شد، لطفا تا 120 ثانیه دیگر همه نشست های اکانت را بجز ربات از اکانت خارج کنید، همچنین خودتان از اکانت لاگ اوت کنید تا اکانت به موجودی شما اضافه شود.\n⏳ زمان باقیمانده : `{20 - i}`')
            #
            # auths = await temp_client.send(functions.account.GetAuthorizations())
            # s = [1 for a in auths.authorizations]
            # if not len(s) == 1:
            #     await timer.delete()
            #     if verify_sudo(msg.from_user.id):
            #         await msg.reply('ℹ️ اکانت وارد شده توسط شما دارای نشست های فعال میباشد و به ربات اضافه نمیشود، لطفا مجددا اقدام به اضافه کردن اکانت کنید.', reply_markup=sudo_keyboard)
            #     else:
            #         await msg.reply('ℹ️ اکانت وارد شده توسط شما دارای نشست های فعال میباشد و به ربات اضافه نمیشود، لطفا مجددا اقدام به اضافه کردن اکانت کنید.', reply_markup=all_keyboard)
            #     await temp_client.log_out()
            #     return

            temp_user = await temp_client.get_me()

            await temp_client.unblock_user('@spambot')
            await temp_client.send_message('@spambot', '/start')
            await asyncio.sleep(0.5)
            resp = await temp_client.get_history('@spambot', limit=1)
            text = resp[0].text

            if re.search(r'^Good news', text) or re.search(r"^مژده", text):

                try:
                    try:
                        await temp_client.set_profile_photo(photo=await generate_pfp())
                    except Exception as err:
                        print(
                            f'[PROFILE PIC ERROR] {type(err).__name__} {type(err)} {err}')
                        pass
                    try:
                        await temp_client.update_profile(first_name=await generate_info(), bio=await generate_bio())
                    except Exception as err:
                        print(
                            f'[NAME OR BIO ERROR] {type(err).__name__} {type(err)} {err}')
                        pass
                    try:
                        await temp_client.update_username(username=await generate_username(12))
                    except Exception as err:
                        print(
                            f'[USERNAME ERROR] {type(err).__name__} {type(err)} {err}')
                        pass
                    try:
                        passwd = await generate_string(16)
                        print(
                            f'[ID: {temp_user.id}][PHONE : {phone.text}] PASSWORD : {passwd}')
                        await temp_client.change_cloud_password(current_password=two_factor.text, new_password=passwd, new_hint='dev. uid1337')
                    except:
                        print('2fa problem')
                        pass

                except Exception as e:
                    print(f'{type(e).__name__} {type(e)} {e}')
                    pass

                ses = await temp_client.export_session_string()
                add_to_user(msg.from_user.id)

                r.sadd('phones', phone.text)

                r.sadd(
                    'accounts', f'{ses}||{api__id.text}||{api__hash.text}||{passwd}')

                if verify_sudo(msg.from_user.id):
                    await msg.reply(f'✅ اکانت با موفقیت به دیتابیس ربات اضافه شد. اطلاعات اکانت:\n📱 Phone Number: `{phone.text}`\n⚙️ User ID : `{temp_user.id}`\n{"🆔 Username: " + f"`{temp_user.username}`" if temp_user.username else ""}', reply_markup=sudo_keyboard)
                else:
                    await msg.reply(f'✅ اکانت با موفقیت به دیتابیس ربات اضافه شد. اطلاعات اکانت:\n📱 Phone Number: `{phone.text}`\n⚙️ User ID : `{temp_user.id}`\n{"🆔 Username: " + f"`{temp_user.username}`" if temp_user.username else ""}', reply_markup=all_keyboard)
                await temp_client.join_chat('@iMat1n')
                await temp_client.disconnect()

            # else:
            #
            #     await msg.reply('⚠️ اکانت وارد شده توسط شما ریپورت است. ربات از اکانت خارج میشود و این اکانت به تعداد اکانت های اضافه شده توسط شما اضافه نمیشود.')
            #     await temp_client.log_out()
            #     return

        except PasswordHashInvalid:
            await msg.reply('❌ گذرواژه تایید دومرحله ای اشتباه است. لطفا دوباره برای اضافه کردن اکانت اقدام کنید.')
            await temp_client.disconnect()
            return

        except RPCError as e:
            await msg.reply(f'⚠️ Error!\n`{type(e).__name__} {type(e)} {e}`')
            await temp_client.stop()
            return


@Client.on_message(filters.private & filters.regex('^🔘 مدیریت اکانت ها$'))
async def _accounts_panel(api: Client, msg: Message):
    if not verify_sudo(msg.from_user.id):
        return

    await msg.reply(accounts_panel_text, reply_markup=accounts_panel)


@Client.on_callback_query()
async def detect_process(c: Client, q: CallbackQuery):
    data = q.data
    msg = q.message

    if data == 'first_proc':
        await q.answer()
        information = await msg.edit('ℹ️ پروسه شروع شد. پس از اتمام کار گزارش به صورت فایل به پیوی شما ارسال میشود.')
        log = 'FIRST_PROCESS # uid1337\n\n'

        salem = 0
        report = 0
        deleted = 0
        msg_counter = 0

        accounts = list(r.smembers('accounts'))

        for account in accounts:

            creds = account.split('||')
            tempcli = Client(creds[0], api_id=creds[1], api_hash=creds[2])

            try:
                await tempcli.start()
                me = await tempcli.get_me()

                await tempcli.send(functions.contacts.ResolveUsername(username='iPyDev'))
                sent = await tempcli.send_message('@iPyDev', 'test')
                await sent.delete()
                await tempcli.stop()

                log += f'[{me.id}][{me.phone_number}] Is Not Reported!\n'
                salem += 1

            except PeerFlood:
                log += f'[{me.id}][{me.phone_number}] Is Reported! <=== Added To Reported Database\n'
                r.srem('accounts', account)
                r.sadd('rep_accounts', account)
                await tempcli.stop()
                report += 1

            except UserDeactivated:
                log += f'[UnKnown] Banned !\n'
                r.srem('accounts', account)
                deleted += 1

            except UserDeactivatedBan:
                log += f'[UnKnown] Banned !\n'
                r.srem('accounts', account)
                deleted += 1

            except SessionRevoked:
                log += f'[UnKnown] Logged Out !\n'
                r.srem('accounts', account)
                deleted += 1

            except RPCError as e:
                try:
                    await tempcli.stop()
                except:
                    continue

                log += f'[UnKnown] {type(e).__name__} {type(e)} {e}'
                r.srem('accounts', account)
                deleted += 1

            await information.edit(f'{information.text}\n\n♻️ Current : `{msg_counter} / {len(accounts)}`')
            msg_counter += 1
            await asyncio.sleep(0.5)

        with open('log.txt', 'w') as f:
            f.write(log)

        await c.send_document(msg.chat.id, document='log.txt', caption=f'📯 تکمیل پروسه جدا سازی اکانت ها\n🔰 گزارش : \n🔻 تعداد کل اکانت ها : {len(accounts)}\n✅ اکانت های سالم‌: {salem}\n⚠️ اکانت های ریپورت: {report}\n❌ دیلیت/لاگ اوت ها : {deleted}')
        await information.delete()
        os.remove('log.txt')

    elif data == 'second_proc':
        await q.answer()
        information = await msg.edit('ℹ️ پروسه شروع شد. پس از اتمام کار گزارش به صورت فایل به پیوی شما ارسال میشود.')
        log = 'SECOND_PROCESS # uid1337\n\n'

        salem = 0
        report = 0
        deleted = 0
        msg_counter = 1
        accounts = list(r.smembers('rep_accounts'))

        for account in accounts:

            creds = account.split('||')
            tempcli = Client(creds[0], api_id=creds[1], api_hash=creds[2])

            try:
                await tempcli.start()
                me = await tempcli.get_me()

                await tempcli.send(functions.contacts.ResolveUsername(username='iPyDev'))
                sent = await tempcli.send_message('@iPyDev', 'test')
                await sent.delete()
                await tempcli.stop()

                log += f'[{me.id}][{me.phone_number}] Is Not Reported!\n'
                r.srem('rep_accounts', account)
                r.sadd('accounts', account)
                salem += 1

            except PeerFlood:
                log += f'[{me.id}][{me.phone_number}] Is Reported! <=== Stay In Reported Database\n'
                r.srem('accounts', account)
                r.sadd('rep_accounts', account)
                await tempcli.stop()
                report += 1

            except UserDeactivated:
                log += f'[UnKnown] Banned !\n'
                r.srem('rep_accounts', account)
                deleted += 1

            except UserDeactivatedBan:
                log += f'[UnKnown] Banned !\n'
                r.srem('rep_accounts', account)
                deleted += 1

            except SessionRevoked:
                log += f'[UnKnown] Logged Out !\n'
                r.srem('rep_accounts', account)
                deleted += 1

            except RPCError as e:
                try:
                    await tempcli.stop()
                except:
                    continue

                log += f'[UnKnown] {type(e).__name__} {type(e)} {e}'
                r.srem('rep_accounts', account)
                deleted += 1

            await information.edit(f'{information.text}\n\n♻️ Current : `{msg_counter} / {len(accounts)}`')
            msg_counter += 1
            await asyncio.sleep(0.5)

        with open('log.txt', 'w') as f:
            f.write(log)

        string = f'📯 تکمیل پروسه جدا سازی اکانت ها\n🔰 گزارش : \n🔻 تعداد کل اکانت های ریپورتی قبل پروسه : {len(accounts)}\n✅ اکانت های سالم‌ : {salem}\n⚠️ اکانت های ریپورت: {report}\n❌ دیلیت/لاگ اوت ها : {deleted}'
        if salem > 0:
            string += '\n\n*نکته :‌اکانت های سالم به دیتابیس اصلی ربات اضافه شدند.'
        await c.send_document(msg.chat.id, document='log.txt', caption=string)

        await information.delete()
        os.remove('log.txt')
    else:
        pass
