import math
import time
from configs import Config


async def progress_for_pyrogram(current: int, total: int, ud_type: str, message, start: float) -> bool:
    """
    Update the progress of an upload or download.

    Args:
        current (int): Current bytes uploaded or downloaded.
        total (int): Total bytes to upload or download.
        ud_type (str): Type of upload/download (e.g., "Uploading", "Downloading").
        message: Message object to update.
        start (float): Start time of the operation.

    Returns:
        bool: True if the message was updated successfully, False otherwise.
    """
    
    if current >= total:  # No need to calculate if done
        return True

    now = time.time()
    diff = now - start

    if round(diff % 10.00) == 0:  # Update every 10 seconds
        percentage = (current * 100) / total
        speed = current / diff if diff > 0 else 0
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed * 1000) if speed > 0 else 0
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time_str = time_formatter(milliseconds=elapsed_time)
        estimated_total_time_str = time_formatter(milliseconds=estimated_total_time)

        progress = "[{0}{1}] \n".format(
            ''.join(["●" for _ in range(math.floor(percentage / 5))]),
            ''.join(["○" for _ in range(20 - math.floor(percentage / 5))])
        )

        progress_message = Config.PROGRESS.format(
            round(percentage, 2),
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            estimated_total_time_str if estimated_total_time_str else "0 s"
        )

        try:
            await message.edit(
                text="**{}**\n\n {}".format(ud_type, progress + progress_message),
                parse_mode='markdown'
            )
            return True
        except Exception as e:
            print(f"Error updating message: {e}")
            return False


def humanbytes(size: int) -> str:
    """Convert bytes to a human-readable format."""
    if size == 0:
        return "0 B"
    
    power = 2 ** 10
    n = 0
    dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    
    while size > power:
        size /= power
        n += 1
    
    return f"{round(size, 2)} {dic_powerN[n]}B"


def time_formatter(milliseconds: int) -> str:
    """Convert milliseconds to a human-readable time format."""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    time_components = []
    if days:
        time_components.append(f"{days}d")
    if hours:
        time_components.append(f"{hours}h")
    if minutes:
        time_components.append(f"{minutes}m")
    if seconds:
        time_components.append(f"{seconds}s")
    if milliseconds:
        time_components.append(f"{milliseconds}ms")

    return ", ".join(time_components)
