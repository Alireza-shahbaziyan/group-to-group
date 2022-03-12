# TODO:
#
from pyrogram import (
    Client,
    filters
)
from pyrogram.types import (
    Message,
)
from .keyboards import (
    sudo_keyboard,
    admin_keyboard,
    all_keyboard
)
from .functions import (
    verify_admin,
    verify_sudo,
    all_check
)


@Client.on_message(filters.private & filters.command('start'))
async def _send_start(_, msg: Message):
    if verify_sudo(msg.from_user.id):
        await msg.reply(f'[سودوی](tg://user?id={msg.from_user.id}) گرامی به ربات خوش آمدید 🌸', reply_markup=sudo_keyboard)
    elif verify_admin(msg.from_user.id):
        await msg.reply(f'[ادمین](tg://user?id={msg.from_user.id}) گرامی به ربات خوش آمدید 🌸', reply_markup=admin_keyboard)
    elif all_check(msg.from_user.id):
        await msg.reply(f'[کاربر](tg://user?id={msg.from_user.id}) گرامی به ربات خوش آمدید 🌸', reply_markup=all_keyboard)
    else:
        return
