from pyrogram import (
    Client,
    filters
)

from pyrogram.types import (
    Message,
)

from .functions import (
    verify_admin,
    verify_sudo
)
from config import r


@Client.on_message(filters.private & filters.regex('^👤 مشاهده اطلاعات حساب کاربری$'))
async def __all_keyboard(_, msg: Message):
    if verify_sudo(msg.from_user.id) | verify_admin(msg.from_user.id):
        return
    await msg.reply(f'🔢 موجودی حساب شما `{r.get(msg.from_user.id)}` اکانت می باشد!\nID : `{msg.from_user.id}`')
