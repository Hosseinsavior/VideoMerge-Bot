import aiohttp
from configs import Config
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from helpers.display_progress import humanbytes


async def upload_to_streamtape(file: str, editable: Message, file_size: int):
    """
    Upload a file to Streamtape and return the download link.

    Args:
        file (str): The path to the file to upload.
        editable (Message): The message object to edit with the upload status.
        file_size (int): The size of the file being uploaded.

    Returns:
        None
    """
    try:
        async with aiohttp.ClientSession() as session:
            main_api = "https://api.streamtape.com/file/ul?login={}&key={}"
            hit_api = await session.get(main_api.format(Config.STREAMTAPE_API_USERNAME, Config.STREAMTAPE_API_PASS))
            json_data = await hit_api.json()

            if json_data.get("result") and json_data["result"].get("url"):
                temp_api = json_data["result"]["url"]
                
                # Use async with to ensure the file is properly closed after upload
                async with aiofiles.open(file, 'rb') as f:
                    response = await session.post(temp_api, data={'file1': f})
                    data_f = await response.json(content_type=None)

                    if "result" in data_f and "url" in data_f["result"]:
                        download_link = data_f["result"]["url"]
                        filename = file.split("/")[-1].replace("_", " ")
                        text_edit = (
                            f"File Uploaded to Streamtape!\n\n"
                            f"**File Name:** `{filename}`\n"
                            f"**Size:** `{humanbytes(file_size)}`\n"
                            f"**Link:** `{download_link}`"
                        )
                        await editable.edit(
                            text_edit, 
                            parse_mode="Markdown", 
                            disable_web_page_preview=True, 
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Open Link", url=download_link)]])
                        )
                    else:
                        raise ValueError("Failed to retrieve download link from Streamtape.")
            else:
                raise ValueError("Failed to authenticate with Streamtape API.")
    except Exception as e:
        print(f"Error: {e}")
        await editable.edit("Sorry, Something went wrong!\n\nCan't Upload to Streamtape. You can report at [Support Group](https://t.me/linux_repo).")
