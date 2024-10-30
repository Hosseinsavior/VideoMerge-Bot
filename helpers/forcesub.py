import asyncio
from configs import Config
from pyrogram import Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

async def get_invite_link(bot: Client):
    """Create a chat invite link."""
    try:
        return await bot.create_chat_invite_link(chat_id=(int(Config.UPDATES_CHANNEL) if Config.UPDATES_CHANNEL.startswith("-100") else Config.UPDATES_CHANNEL))
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await bot.create_chat_invite_link(chat_id=(int(Config.UPDATES_CHANNEL) if Config.UPDATES_CHANNEL.startswith("-100") else Config.UPDATES_CHANNEL))

async def check_user_subscription(bot: Client, user_id: int):
    """Check if the user is a participant of the updates channel."""
    return await bot.get_chat_member(chat_id=(int(Config.UPDATES_CHANNEL) if Config.UPDATES_CHANNEL.startswith("-100") else Config.UPDATES_CHANNEL), user_id=user_id)

async def send_subscription_message(cmd: Message, invite_link):
    """Send a message asking the user to join the updates channel."""
    await cmd.reply_to_message.reply(
        chat_id=cmd.from_user.id,
        text="**Please Join My Updates Channel to use this Bot!**\n\nDue to Overload, Only Channel Subscribers can use the Bot!",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link.invite_link)
                ],
                [
                    InlineKeyboardButton("🔄 Refresh 🔄", callback_data="refreshFsub")
                ]
            ]
        ),
        parse_mode="markdown"
    )

async def ForceSub(bot: Client, cmd: Message):
    """Force users to subscribe to the updates channel."""
    invite_link = await get_invite_link(bot)

    try:
        user = await check_user_subscription(bot, cmd.from_user.id)
        if user.status == "kicked":
            await bot.send_message(
                chat_id=cmd.from_user.id,
                text="Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/linux_repo).",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return 400
    except UserNotParticipant:
        await send_subscription_message(cmd, invite_link)
        return 400
    except Exception as err:
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text=f"Something went wrong: {err}\nContact my [Support Group](https://t.me/linux_repo).",
            parse_mode="markdown",
            disable_web_page_preview=True
        )
        return 400

    return 200
