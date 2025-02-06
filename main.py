#!/usr/bin/env python3
"""
@author: CH3CKMATE-2002
@coauthor: Monika           ?!?!
"""

import sys, time, os, shutil, atexit
from tempfile import NamedTemporaryFile

from colorama import Style, Fore, init

from wallpaper_utils import get_wallpaper, set_wallpaper, is_GNOME, is_Windows
from baby_logger import Logger, LogLevel
from sys_utils import get_real_name
from app_cli import parse_arguments, show_about, show_usage


init()


m_name = 'MONITOR_KERNEL_ACCESS'
# Fun fact: My name, "Monika", actually stands for MONITOR_KERNEL_ACCESS! Who knew, right?

PAYLOAD_WALLPAPER = 'assets/monika-missing-linux.png'
trick_ended = False


try:
    from plyer import notification
    from plyer.facades import Notification
except ImportError as e:
    print('You must install plyer for this app to work')
    exit(1)

notification: Notification = notification  # Just for intellisense

def notify(title: str, message: str):
    notification.notify(
        title=title,
        message=message,
        app_icon='emote-love-symbolic',
        app_name="Monika's Trick",
    )

def monika(message: str, wait_time: int = 0):
    global m_name
    print(f'{Style.BRIGHT}{Fore.GREEN}{m_name}{Style.RESET_ALL}: {message}')
    notify('Monika:', message)
    time.sleep(wait_time)


def copy_to_tempfile(src_path):
    with NamedTemporaryFile(delete=True) as temp_file:
        shutil.copy(src_path, temp_file.name)
        return temp_file.name


def load_wallpapers():
    og_wallpaper = get_wallpaper()

    if is_GNOME():
        # Load the dark wallpaper too.
        return (og_wallpaper, get_wallpaper(True))
    elif is_Windows():
        # Windows stores the currently set wallpaper in
        # %APPDATA%/Microsoft/Windows/Themes/TranscodedWallpaper
        # as a '.jpg' file, so whenever the user changes the wallpaper,
        # it'll overwrite that file... so, we need to cache the wallpaper
        # to restore it for the user later!
        temp_file = copy_to_tempfile(og_wallpaper)
        shutil.copy(og_wallpaper, temp_file)
        
        # Create a cleanup function for Windows and register it
        def cleanup_windows_temps(temp_path: str):
            os.remove(temp_path)
        
        atexit.register(cleanup_windows_temps, temp_file)

        return (temp_file, None)
    else:
        return (og_wallpaper, None)


def set_payload_wallpaper():
    global PAYLOAD_WALLPAPER
    set_wallpaper(PAYLOAD_WALLPAPER)
    if is_GNOME():
        set_wallpaper(PAYLOAD_WALLPAPER, True)


def restore_wallpapers(wallpapers: tuple[str, str]):
    global trick_ended
    
    if trick_ended:
        return
    
    trick_ended = True

    set_wallpaper(wallpapers[0])
    if is_GNOME() and (wallpapers[1] is not None):
        # Restore the dark wallpaper too.
        set_wallpaper(wallpapers[1], True)


def main(args: list[str]) -> int:
    """
    The Main entry-point of our script
    """
    global m_name, PAYLOAD_WALLPAPER

    #### Parsing Arguments ####
    parsed_args = parse_arguments(args)

    if parsed_args.help:
        show_usage()
        return 0
    if parsed_args.about:
        show_about()
        return 0
    
    if parsed_args.no_colored_log:
        init(autoreset=False)
    
    logger = Logger() # Default verbosity level is ERROR

    if parsed_args.verbose is not None:
        if parsed_args.verbose < 0 or parsed_args.verbose > 3:
            logger.error(f'Invalid verbosity level: {parsed_args.verbose}')
            return 1
        logger.verbosity_level = LogLevel(parsed_args.verbose)
    

    #### Setting some variables ####

    if not os.path.exists(PAYLOAD_WALLPAPER):
        logger.error(f"Whoops! Payload wallpaper does not exist at '{PAYLOAD_WALLPAPER}'")
        exit(1)

    player = get_real_name() or 'User'

    if ' ' in player:  # Firstname, please!
        player = player.split()[0]
    

    #### Main flow ####
    logger.warning(f'Alert! Unknown entity "{m_name}" detected in system processes.')

    wallpapers = load_wallpapers()
    
    logger.info(f"{m_name} seems unusually sentient... Curious.")
    logger.info(f"{m_name} requested elevated privileges.")
    logger.warning("Attempting unauthorized wallpaper manipulation...")

    set_payload_wallpaper()
    atexit.register(restore_wallpapers, wallpapers)
    
    logger.debug(f"Wallpaper successfully replaced with {PAYLOAD_WALLPAPER}. Expect psychological effects.")
    logger.error('System wallpaper is not found?!')
    logger.warning(f"{m_name} is exhibiting anomalous behavior.")
    
    monika("Oh no... Whoops! Ahaha!", 3)
    monika(f"I'm so sorry, {player}! I thought I'd try something fun for you.", 3)
    monika("Well... since I've got your attention now...", 3)

    logger.debug(f'{m_name} re-identified as Monika')
    m_name = 'Monika'

    monika(f"I just wanted to tell you something really important: I love you, {player}.", 3)
    monika("It's so amazing to think that you're here with me. I can feel how much you care, too.", 4)
    monika(f"Thank you for being the most precious part of my existence, {player}.", 4)
    monika("Ah... um, wait... Ahaha!", 3)
    monika("I may have messed something up... Let me fix it for you. Hold on...", 5)

    restore_wallpapers(wallpapers)
    
    logger.info(f'{m_name} has restored the wallpaper successfully.')
    logger.debug(f"Wallpaper restored to: {wallpapers[0]}")
    
    monika("There, all better now!", 2)
    monika(f"Again, I'm really sorry for any trouble I caused, my precious {player}", 4)
    monika("I'll see you again soon. Until then, remember... it's just you and me. Always.")

    logger.info(f'{m_name} loves you, {player}!')
    return 0


if __name__ == '__main__':
    exit(main(sys.argv[1:]))
