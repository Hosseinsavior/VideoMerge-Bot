import asyncio
from helpers.database.access_db import db
from pyrogram.errors import MessageNotModified, FloodWait
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


async def get_upload_mode_button(user_id: int):
    """Create the upload mode button based on user settings."""
    upload_as_doc = await db.get_upload_as_doc(id=user_id)
    return InlineKeyboardButton(f"Upload as {'Video' if not upload_as_doc else 'Document'} ✅", callback_data="triggerUploadMode")


async def get_generate_sample_video_button(user_id: int):
    """Create the generate sample video button based on user settings."""
    generate_sample_video = await db.get_generate_sample_video(id=user_id)
    return InlineKeyboardButton(f"Generate Sample Video {'✅' if generate_sample_video else '❌'}", callback_data="triggerGenSample")


async def get_generate_ss_button(user_id: int):
    """Create the generate screenshots button based on user settings."""
    generate_ss = await db.get_generate_ss(id=user_id)
    return InlineKeyboardButton(f"Generate Screenshots {'✅' if generate_ss else '❌'}", callback_data="triggerGenSS")


async def open_settings(m: Message, user_id: int):
    """Open the settings menu for the user."""
    try:
        markup = InlineKeyboardMarkup(
            [
                [await get_upload_mode_button(user_id)],
                [await get_generate_sample_video_button(user_id)],
                [await get_generate_ss_button(user_id)],
                [InlineKeyboardButton("Show Thumbnail", callback_data="showThumbnail")],
                [InlineKeyboardButton("Show Queue Files", callback_data="showQueueFiles")],
                [InlineKeyboardButton("Close", callback_data="closeMeh")]
            ]
        )

        await m.edit(text="Here You Can Change or Configure Your Settings:", reply_markup=markup)
    except MessageNotModified:
        pass
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await m.edit("You Are Spamming!")
    except Exception as err:
        print(f"An error occurred while opening settings: {err}")
        await m.edit("An error occurred while trying to open settings. Please try again later.")
```

### نکات نهایی
- **مدیریت خطا**: با بهبود مدیریت خطا و ارائه اطلاعات بیشتر به کاربر، می‌توانید از بروز مشکلات بیشتر جلوگیری کنید.
- **کد تمیزتر**: با استفاده از توابع کمکی، کد شما خواناتر و قابل نگهداری‌تر می‌شود.
- **مستندسازی بهتر**: با اضافه کردن مستندات، فهم بهتر عملکرد توابع امکان‌پذیر می‌شود.

این تغییرات می‌تواند به بهبود کد شما کمک کند و آن را برای نگهداری و به‌روزرسانی آسان‌تر کند. موفق باشید!
