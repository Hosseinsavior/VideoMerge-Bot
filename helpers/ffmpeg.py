import asyncio
import os
import time
from configs import Config
from pyrogram.types import Message


async def run_ffmpeg_command(command):
    """Run an FFmpeg command asynchronously and return the output."""
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    return stdout.decode().strip(), stderr.decode().strip()


async def merge_video(input_file: str, user_id: int, message: Message, format_: str):
    """
    Merge videos together.

    Args:
        input_file (str): The path to the input.txt file.
        user_id (int): User ID to create output path.
        message (Message): Editable message for showing progress.
        format_ (str): Output file extension.

    Returns:
        str or None: Path to the merged video file or None if failed.
    """
    
    output_vid = f"{Config.DOWN_PATH}/{user_id}/[@AbirHasan2005]_Merged.{format_.lower()}"
    file_generator_command = [
        "ffmpeg",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        input_file,
        "-c",
        "copy",
        output_vid
    ]

    try:
        await message.edit("Merging Video Now ...\n\nPlease Keep Patience ...")
        stdout, stderr = await run_ffmpeg_command(file_generator_command)
        print(stdout)
        print(stderr)
        
        if os.path.lexists(output_vid):
            return output_vid
        else:
            print("Merged video file does not exist.")
            return None
    except Exception as e:
        await message.edit(f"An error occurred while merging videos: {e}")
        return None


async def cut_small_video(video_file: str, output_directory: str, start_time: int, end_time: int, format_: str):
    """
    Cut a small portion from the video.

    Args:
        video_file (str): Path to the video file.
        output_directory (str): Directory to save the cut video.
        start_time (int): Start time in seconds.
        end_time (int): End time in seconds.
        format_ (str): Output file extension.

    Returns:
        str or None: Path to the cut video file or None if failed.
    """
    
    output_file_name = os.path.join(output_directory, f"{round(time.time())}.{format_.lower()}")
    file_generator_command = [
        "ffmpeg",
        "-i",
        video_file,
        "-ss",
        str(start_time),
        "-to",
        str(end_time),
        "-async",
        "1",
        "-strict",
        "-2",
        output_file_name
    ]
    
    stdout, stderr = await run_ffmpeg_command(file_generator_command)
    print(stdout)
    print(stderr)

    if os.path.lexists(output_file_name):
        return output_file_name
    else:
        print("Cut video file does not exist.")
        return None


async def generate_screenshots(video_file: str, output_directory: str, no_of_photos: int, duration: int):
    """
    Generate screenshots from the video at equal intervals.

    Args:
        video_file (str): Path to the video file.
        output_directory (str): Directory to save screenshots.
        no_of_photos (int): Number of screenshots to take.
        duration (int): Duration of the video in seconds.

    Returns:
        list: List of paths to generated screenshots.
    """
    
    if duration <= 0 or no_of_photos <= 0:
        print("Invalid duration or number of photos.")
        return []

    images = []
    ttl_step = duration // no_of_photos
    current_ttl = ttl_step

    for _ in range(no_of_photos):
        await asyncio.sleep(1)  # Optional: delay for better processing
        video_thumbnail = os.path.join(output_directory, f"{str(time.time())}.jpg")
        file_generator_command = [
            "ffmpeg",
            "-ss",
            str(round(current_ttl)),
            "-i",
            video_file,
            "-vframes",
            "1",
            video_thumbnail
        ]

        stdout, stderr = await run_ffmpeg_command(file_generator_command)
        print(stdout)
        print(stderr)
        
        if os.path.lexists(video_thumbnail):
            images.append(video_thumbnail)
        current_ttl += ttl_step

    return images
