""" Handles system level operations"""

from os.path import join, exists,isfile, isdir, basename
from os import getcwd, mkdir, listdir, remove
from os import environ, getenv


def cwd():
    """
    get the users current working directory

    Returns:
        str : current working directory
    """
    current_dir = getcwd()
    return current_dir

def download_dir():
    """
    gets the user's download folder

    Returns:
        str: downloads dir
    """
    home = user_home()
    download = join(home,"Downloads")
    
    return download

def user_home():
    """
    gets the user's home folder

    Returns:
        str: home dir
    """
    try:
        home =  environ.get("HOME")
    except Exception as e:
        try:
            home = getenv("USERPROFILE")
        except Exception as e:
            home = environ.get("USERPROFILE")
    return home

DOWNLOADS = download_dir()
CWD = cwd()
HOME = user_home()


