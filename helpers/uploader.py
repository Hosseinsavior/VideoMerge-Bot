import asyncio
import time
from configs import Config
from helpers.database.access_db import db
from helpers.display_progress import progress_for_pyrogram, humanbytes
from humanfriendly import format_timespan
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

async def create_reply_markup():
    """Create the reply markup for the uploaded video."""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Developer - @AbirHasan2005", url="https://t.me/AbirHasan2005")],
            [InlineKeyboardButton("Support Group", url="https://t.me/linux_repo"),
             InlineKeyboardButton("Bots Channel", url="https://t.me/Discovery_Updates")]
        ]
    )

async def upload_video(bot: Client, cb: CallbackQuery, merged_vid_path: str, width: int, height: int, duration: int, video_thumbnail: str, file_size: int):
    """
    Upload a video or document to Telegram based on user settings.

    Args:
        bot (Client): The Pyrogram Client instance.
        cb (CallbackQuery): The callback query object.
        merged_vid_path (str): The path to the merged video.
        width (int): Width of the video.
        height (int): Height of the video.
        duration (int): Duration of the video in seconds.
        video_thumbnail (str): Path to the video thumbnail.
        file_size (int): Size of the file in bytes.

    Returns:
        None
    """
    try:
        sent_ = None
        is_upload_as_doc = await db.get_upload_as_doc(cb.from_user.id)
        c_time = time.time()
        
        caption = Config.CAPTION.format((await bot.get_me()).username) + f"\n\n**File Name:** `{merged_vid_path.rsplit('/', 1)[-1]}`\n**Duration:** `{format_timespan(duration)}`\n**File Size:** `{humanbytes(file_size)}`"

        if not is_upload_as_doc:
            sent_ = await bot.send_video(
                chat_id=cb.message.chat.id,
                video=merged_vid_path,
                width=width,
                height=height,
                duration=duration,
                thumb=video_thumbnail,
                caption=caption,
                progress=progress_for_pyrogram,
                progress_args=("Uploading Video ...", cb.message, c_time),
                reply_markup=await create_reply_markup()
            )
        else:
            sent_ = await bot.send_document(
                chat_id=cb.message.chat.id,
                document=merged_vid_path,
                caption=caption,
                thumb=video_thumbnail,
                progress=progress_for_pyrogram,
                progress_args=("Uploading Video ...", cb.message, c_time),
                reply_markup=await create_reply_markup()
            )

        await asyncio.sleep(Config.TIME_GAP)
        forward_ = await sent_.forward(chat_id=Config.LOG_CHANNEL)
        await forward_.reply_text(
            text=f"**User:** [{cb.from_user.first_name}](tg://user?id={str(cb.from_user.id)})\n**Username:** `{cb.from_user.username}`\n**UserID:** `{cb.from_user.id}`",
            disable_web_page_preview=True,
            quote=True
        )
    except Exception as err:
        print(f"Failed to Upload Video!\nError: {err}")
        try:
            await cb.message.edit(f"Failed to Upload Video!\n**Error:**\n`{err}`")
        except Exception as edit_err:
            print(f"Failed to edit message: {edit_err}")
