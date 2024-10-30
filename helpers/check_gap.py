import time
from configs import Config

GAP = {}


async def check_time_gap(user_id: int):
    """Check the time gap for a user.
    
    Args:
        user_id (int): The Telegram user ID.

    Returns:
        tuple: A tuple containing:
            - bool: Whether a gap is present.
            - int or None: Remaining time to wait or None if no gap.
    """
    
    current_time = time.time()
    user_id_str = str(user_id)

    if user_id_str in GAP:
        previous_time = GAP[user_id_str]
        elapsed_time = current_time - previous_time

        if elapsed_time < Config.TIME_GAP:
            return True, round(Config.TIME_GAP - elapsed_time)  # Time left
        else:
            del GAP[user_id_str]  # Remove user from GAP dictionary if enough time has passed
            return False, None
    else:
        GAP[user_id_str] = current_time  # Set current time for the user
        return False, None
