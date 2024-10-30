import os
import shutil

async def delete_all(root: str) -> bool:
    """
    Delete a folder and all its contents.

    Args:
        root (str): The path of the folder to delete.

    Returns:
        bool: True if the folder was deleted successfully, False otherwise.
    """
    
    if not os.path.exists(root):
        print(f"Folder '{root}' does not exist.")
        return False

    try:
        shutil.rmtree(root)
        return True
    except Exception as e:
        print(f"An error occurred while deleting the folder '{root}': {e}")
        return False
