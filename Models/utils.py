import os

def ensure_save_directory(filepath):
    """Ensures the directory for a file exists before saving.
    
    Args:
        filepath (str): The full path where the file will be saved
        
    Returns:
        None
    """
    directory = os.path.dirname(filepath)
    if directory:
        os.makedirs(directory, exist_ok=True)
