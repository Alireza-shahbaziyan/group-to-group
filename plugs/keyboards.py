from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)

sudo_keyboard = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton('🚀 اد گروه')
        ],

        [
            KeyboardButton('🚀 شروع ارسال به پیوی')
        ],
        
        [
            KeyboardButton('👥 استخراج اعضای گروه')
        ],
        
        [
            KeyboardButton('👀 مشاهده اطلاعات سفارش'),
            KeyboardButton('👀 مشاهده اطلاعات سفارش زنده'),
        ],
        
        [
            KeyboardButton('ℹ️ مشاهده آخرین سفارش'),
            KeyboardButton('ℹ️ مشاهده سفارش های کاربر'),
        ],
        
        [
            KeyboardButton('🗑 پاکسازی لیست موقت کاربران')
        ],
        
        [
            KeyboardButton('👤 مشاهده موجودی کاربر')
        ],
        
        [
            KeyboardButton('🧮 آمار ربات'),
            KeyboardButton('🏷 وضعیت ربات'),
            KeyboardButton('♻️ تهیه بکاپ'),
        ],
        
        [
            KeyboardButton('♻️ پروسه اسپم بات'),
            KeyboardButton('🔘 مدیریت اکانت ها'),
            KeyboardButton('➕ اهدای اکانت'),
        ],
    ],
    
    resize_keyboard=True,
    one_time_keyboard=True,
)

admin_keyboard = ReplyKeyboardMarkup(
    [
        
        [
            KeyboardButton('👤 مشاهده موجودی کاربر'),
        ],
        
        [
            KeyboardButton('➕ اهدای اکانت')
        ]
    
    ],
    
    resize_keyboard=True,
    one_time_keyboard=True,
)

all_keyboard = ReplyKeyboardMarkup(
    [
        
        [
            KeyboardButton('➕ اهدای اکانت')
        ],
        
        [
            KeyboardButton('👤 مشاهده اطلاعات حساب کاربری')
        ]
    
    ],
    
    resize_keyboard=True,
    one_time_keyboard=True,
)

accounts_panel = InlineKeyboardMarkup(
    [
        
        [
            InlineKeyboardButton('⚙️ پروسه اول', 'first_proc'),
        ],
        
        [
            InlineKeyboardButton('⚙️ پروسه دوم', 'second_proc'),
        ],
    
    ],
)

stop = ReplyKeyboardMarkup(
    [

        [
            KeyboardButton('برگشت')
        ]

    ],

    resize_keyboard=True,
)

cancel = ReplyKeyboardMarkup(
    [
        
        [
            KeyboardButton('❌ لغو')
        ]
    
    ],
    
    resize_keyboard=True,
    one_time_keyboard=True,
)

confirm = ReplyKeyboardMarkup(
    [
        
        [
            KeyboardButton('❌ لغو'),
            KeyboardButton('✅ ادامه')
        ]
    
    ],
    
    resize_keyboard=True,
    one_time_keyboard=True,
)

accounts_panel_text = '''
👮‍♀️ سودوی گرامی؛ به پنل مدیریت اکانت ها خوش آمدید.

توضیحات مربوط به این پنل و پروسه ها:
این پنل برای جدا سازی اکانت های **ریپورت** از **غیر ریپورت** و ذخیره سازی آن ها در دیتابیس **مجزا** فراهم شده است.

1️⃣ پروسه اول:
تمامی اکانت های وارد شده در **دیتابیس اصلی** چک میشوند و در صورت ریپورت بودن به **دیتابیس دوم** __( که مخصوص اکانت های ریپورت است )__ انتقال داده میشوند و فقط اکانت های **سالم** برای پروسه ارسال به پیوی کار میکنند.

2️⃣ پروسه دوم :
اکانت های موجود در دیتابیس **دوم** که مخصوص اکانت های __ریپورت__ میباشد یکی یکی چک میشوند و در صورتی که دیگر **ریپورت** نبودند به دیتابیس **اصلی** ربات برای ارسال به پیوی انتقال داده و آماده میشوند.

💥 با توجه به توضیحات؛ پروسه مورد نظر خود را انتخاب کنید :
'''

temp_del_text = '''
⚠️ از پاکسازی لیست موقتی کاربران اطمینان دارید؟

⏺ راهنما : برای جلوگیری از ارسال تکراری پیام به افراد، در هر سفارش، ایدی افرادی که پیام به آنها ارسال شده است به این لیست اضافه میشود و در ارسال های بعدی در صورتی که آیدی کاربر در این لیست باشد، پیامی برای آنها ارسال نخواهد شد // مثال: یک سفارش 1000 ایدی دارد که به 800 نفر از آیدی ها پیام ارسال میشود، برای ارسال پیام به 200 نفر باقیمانده، بدون پاک کردن لیست موقت میتوانید ارسال بزنید و برای 800 نفر اول پیام تکراری ارسال نمیشود.

ℹ️ تعداد کاربران در لیست موقتی در حال حاضر {} عدد میباشد.
'''

spambot_text = '''
♻️ پروسه اسپم بات ~
در دیتابیس شما در حال حاضر `{}` اکانت ریپورت وجود دارد؛ این پروسه، با اکانت های ریپورت شما به ربات رسمی تلگرام [ @Spambot ] پیامی با مضمون غیر اسپم و تبلیغاتی بودن اکانت ارسال میکند که در نهایت اکانت های ریپورت شما طی چند روز از ریپورت بودن خارج میشوند و آماده ارسال به پیوی میشوند.
برای شروع پروسه، گزینه تایید را انتخاب کنید.
'''

antispam_texts = []
