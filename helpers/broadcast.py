import os
import time
import string
import random
import asyncio
import datetime
import aiofiles
import traceback
from configs import Config
from helpers.database.access_db import db
from pyrogram.types import Message
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid

BROADCAST_LOG_FILE = 'broadcast.txt'
broadcast_ids = {}

async def send_msg(user_id, message):
    try:
        if Config.BROADCAST_AS_COPY:
            await message.copy(chat_id=user_id)
        else:
            await message.forward(chat_id=user_id)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await send_msg(user_id, message)
    except (InputUserDeactivated, UserIsBlocked, PeerIdInvalid) as e:
        return 400, f"{user_id} : {str(e)}\n"
    except Exception as e:
        return 500, f"{user_id} : {traceback.format_exc()}\n"

async def broadcast_handler(m: Message):
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message

    broadcast_id = ''.join(random.choices(string.ascii_letters, k=3))
    while broadcast_id in broadcast_ids:
        broadcast_id = ''.join(random.choices(string.ascii_letters, k=3))

    out = await m.reply_text(text="Broadcast Started! You will be notified with log file when all the users are notified.")
    start_time = time.time()
    total_users = await db.total_users_count()
    done = failed = success = 0
    broadcast_ids[broadcast_id] = {'total': total_users, 'current': done, 'failed': failed, 'success': success}

    async with aiofiles.open(BROADCAST_LOG_FILE, 'w') as broadcast_log_file:
        async for user in all_users:
            sts, msg = await send_msg(user_id=int(user['id']), message=broadcast_msg)
            if msg:
                await broadcast_log_file.write(msg)
            if sts == 200:
                success += 1
            else:
                failed += 1
                if sts == 400:
                    await db.delete_user(user['id'])
            done += 1
            broadcast_ids[broadcast_id]['current'] = done
            broadcast_ids[broadcast_id]['failed'] = failed
            broadcast_ids[broadcast_id]['success'] = success

    broadcast_ids.pop(broadcast_id, None)
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await asyncio.sleep(3)
    await out.delete()

    if failed == 0:
        await m.reply_text(text=f"Broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.", quote=True)
    else:
        await m.reply_document(document=BROADCAST_LOG_FILE, caption=f"Broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.", quote=True)

    os.remove(BROADCAST_LOG_FILE)
