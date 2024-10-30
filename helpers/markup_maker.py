from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, Message

async def make_buttons(bot: Client, m: Message, db: dict):
    """
    Create inline buttons based on the media files in the chat.

    Args:
        bot (Client): The Pyrogram Client instance.
        m (Message): The message object from which to get chat information.
        db (dict): A dictionary containing message IDs.

    Returns:
        list: A list of inline keyboard button rows.
    """
    
    markup = []
    try:
        messages = await bot.get_messages(chat_id=m.chat.id, message_ids=db.get(m.chat.id))
        for i in messages:
            media = i.video or i.document
            if media:
                markup.append([
                    InlineKeyboardButton(f"{media.file_name}", callback_data=f"showFileName_{i.message_id}")
                ])
        
        markup.append([InlineKeyboardButton("Merge Now", callback_data="mergeNow")])
        markup.append([InlineKeyboardButton("Clear Files", callback_data="cancelProcess")])
    
    except Exception as e:
        print(f"Error while creating buttons: {e}")
        # You can also inform the user about the error if needed

    return markup
