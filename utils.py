from pathlib import Path
import os


# Function to find project root, adjust based on your project structure
def find_project_root():
    return os.path.dirname(os.path.abspath(__file__))


def get_filename(filepath):
    """
    :param filepath: some file path
    :return: filename without path or extension
    """
    return Path(filepath).stem