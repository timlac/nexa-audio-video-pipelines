from pathlib import Path


def get_filename(filepath):
    """
    :param filepath: some file path
    :return: filename without path or extension
    """
    return Path(filepath).stem