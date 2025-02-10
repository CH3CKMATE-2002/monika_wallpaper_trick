"""
@author: CH3CKMATE-2002
@contributors:
    Hani
"""

import os, subprocess, time

from sys_info import System, DesktopEnv


try:
    if System.is_windows():
        import ctypes
    elif System.is_linux():
        import pydbus
        from gi.repository import Gio, GLib  # type: ignore
    else:
        raise RuntimeError('Unsupported system')
except ModuleNotFoundError | RuntimeError as e:
    print(f'Error: {e}')
    exit(1)


GNOME_WALLPAPER_SETTING_PATH = "org.gnome.desktop.background"
GNOME_WALLPAPER_LIGHT_PROP_NAME = "picture-uri"
GNOME_WALLPAPER_DARK_PROP_NAME = "picture-uri-dark"

CINNAMON_WALLPAPER_SETTING_PATH = "org.cinnamon.desktop.background"
CINNAMON_WALLPAPER_PROP_NAME = "picture-uri"

MATE_WALLPAPER_SETTING_PATH = "org.mate.background"
MATE_WALLPAPER_PROP_NAME = "picture-filename"

XFCE_XFCONF_BUS_NAME = "org.xfce.Xfconf"
XFCE_XFCONF_OBJECT_PATH = "/org/xfce/Xfconf"
XFCE_DESKTOP_SETTING_NAME = "xfce4-desktop"
XFCE_WALLPAPER_SETTING_PATH_FORMAT = "/backdrop/screen0/monitor%s/workspace0/last-image"

KDE_PLASMASHELL_BUS_NAME = "org.kde.Plasmashell"
KDE_PLASMASHELL_OBJECT_PATH = "/PlasmaShell"


def _get_windows_wallpaper() -> str:
    """Retrieve current wallpaper on Windows."""
    buf = ctypes.create_unicode_buffer(512)
    ctypes.windll.user32.SystemParametersInfoW(0x73, len(buf), buf, 0)
    return buf.value


def _set_windows_wallpaper(wallpaper_path: str):
    """Set wallpaper on Windows using native API."""
    path = os.path.abspath(wallpaper_path)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, str(path), 3)



def _get_gio_property_value(setting_path: str, property_name: str) -> str:
    """Retrieve a string property value using Gio settings (works on GNOME, Cinnamon, and MATE)."""
    schema = Gio.Settings.new(setting_path)
    return schema.get_string(property_name)


def _set_gio_property_value(setting_path: str, property_name: str, property_value: str):
    """
        Set a string property to a value using Gio (GTK settings API).
    """
    schema = Gio.Settings.new(setting_path)
    schema.set_string(property_name, property_value)
    schema.apply()


def _get_dbus_property_value(bus_name: str, object_path: str, setting_name: str, setting_path: str):
    bus = pydbus.SessionBus()
    try:
        proxy = bus.get(bus_name, object_path)
        return proxy.GetProperty(setting_name, setting_path)
    except GLib.Error:  # pydbus exceptions typically wrap GLib.Error
        return None

def _set_dbus_property_value(bus_name: str, object_path: str, setting_name: str, setting_path: str, value: str):
    bus = pydbus.SessionBus()
    try:
        proxy = bus.get(bus_name, object_path)
        proxy.SetProperty(setting_name, setting_path, value)
    except GLib.Error:
        return


def _get_gnome_wallpaper(is_dark = False) -> str:
    """
        Retrieve the current wallpaper in GNOME Desktop Environment
    """
    property_name = GNOME_WALLPAPER_LIGHT_PROP_NAME
    
    if is_dark:
        property_name = GNOME_WALLPAPER_DARK_PROP_NAME
    
    uri = _get_gio_property_value(GNOME_WALLPAPER_SETTING_PATH, property_name)
    return uri.replace('file://', '')


def _set_gnome_wallpaper(wallpaper_path: str, is_dark = False):
    """
        Retrieve the current wallpaper in GNOME Desktop Environment
    """
    property_name = GNOME_WALLPAPER_LIGHT_PROP_NAME
    
    if is_dark:
        property_name = GNOME_WALLPAPER_DARK_PROP_NAME
    
    path = os.path.abspath(wallpaper_path)
    uri = f"file://{path}"

    _set_gio_property_value(GNOME_WALLPAPER_SETTING_PATH, property_name, uri)


def _get_cinnamon_wallpaper():
    uri = _get_gio_property_value(CINNAMON_WALLPAPER_SETTING_PATH, CINNAMON_WALLPAPER_PROP_NAME)
    return uri.replace("file://", "")

def _set_cinnamon_wallpaper(wallpaper_path: str):
    path = os.path.abspath(wallpaper_path)
    uri = f"file://{path}"
    _set_gio_property_value(CINNAMON_WALLPAPER_SETTING_PATH, CINNAMON_WALLPAPER_PROP_NAME, uri)


def _get_mate_wallpaper():
    return _get_gio_property_value(MATE_WALLPAPER_SETTING_PATH, MATE_WALLPAPER_PROP_NAME)

def _set_mate_wallpaper(wallpaper_path: str):
    path = os.path.abspath(wallpaper_path)
    _set_gio_property_value(MATE_WALLPAPER_SETTING_PATH, MATE_WALLPAPER_PROP_NAME, path)


def _get_active_monitor_name():
    """Get the active monitor name using xrandr."""
    try:
        # Try using xrandr to get the active monitor name
        output = subprocess.check_output(["xrandr", "--listactivemonitors"], text=True)
        lines = output.strip().split("\n")
        if len(lines) > 1:
            # Extract the monitor name from the second line
            monitor_name = lines[1].split()[-1]
            return monitor_name
        
    except subprocess.CalledProcessError | FileNotFoundError as e:
        return None
    
    return None


def _get_xfce_wallpaper():
    monitor_name = _get_active_monitor_name()
    if monitor_name is None:
        return None
    setting_path = XFCE_WALLPAPER_SETTING_PATH_FORMAT % monitor_name

    return _get_dbus_property_value(
        XFCE_XFCONF_BUS_NAME,
        XFCE_XFCONF_OBJECT_PATH,
        XFCE_DESKTOP_SETTING_NAME,
        setting_path
    )


def _set_xfce_wallpaper(wallpaper_path: str):
    monitor_name = _get_active_monitor_name()
    if monitor_name is None:
        return None
    setting_path = XFCE_WALLPAPER_SETTING_PATH_FORMAT % monitor_name

    path = os.path.abspath(wallpaper_path)

    _set_dbus_property_value(
        XFCE_XFCONF_BUS_NAME,
        XFCE_XFCONF_OBJECT_PATH,
        XFCE_DESKTOP_SETTING_NAME,
        setting_path,
        path
    )



def _get_kde_wallpaper():
    bus = pydbus.SessionBus()
    plasma = bus.get(KDE_PLASMASHELL_BUS_NAME, KDE_PLASMASHELL_OBJECT_PATH)
    script = """
        var d = desktops()[0];
        d.currentConfigGroup = ["Wallpaper", "org.kde.image", "General"];
        print(d.readConfig("Image"));
    """
    uri: str = plasma.evaluateScript(script)
    return uri.replace("file://", "")

def _set_kde_wallpaper(wallpaper_path: str):
    bus = pydbus.SessionBus()
    plasma = bus.get(KDE_PLASMASHELL_BUS_NAME, KDE_PLASMASHELL_OBJECT_PATH)
    path = os.path.abspath(wallpaper_path)

    script = f"""
        var d = desktops();
        for (var i = 0; i < d.length; i++) {{
            d[i].wallpaperPlugin = "org.kde.image";
            d[i].currentConfigGroup = ["Wallpaper", "org.kde.image", "General"];
            d[i].writeConfig("Image", "file://{path}");
        }}
    """
    plasma.evaluateScript(script)



def get_wallpaper(is_dark = False) -> str:
    if System.is_windows():
        return _get_windows_wallpaper()
    
    elif DesktopEnv.is_gnome():
        return _get_gnome_wallpaper(is_dark)
    
    elif DesktopEnv.is_cinnamon():
        return _get_cinnamon_wallpaper()
    
    elif DesktopEnv.is_mate():
        return _get_mate_wallpaper()
    
    elif DesktopEnv.is_xfce():
        return _get_xfce_wallpaper()
    
    elif DesktopEnv.is_kde():
        return _get_kde_wallpaper()
    
    else:
        return None

def set_wallpaper(wallpaper_path: str, is_dark = False):
    if wallpaper_path is None:
        raise RuntimeError('Wallpaper path is None')
    
    if System.is_windows():
        _set_windows_wallpaper(wallpaper_path)
    
    elif DesktopEnv.is_gnome():
        _set_gnome_wallpaper(wallpaper_path, is_dark)
    
    elif DesktopEnv.is_cinnamon():
        _set_cinnamon_wallpaper(wallpaper_path)
    
    elif DesktopEnv.is_mate():
        _set_mate_wallpaper(wallpaper_path)
    
    elif DesktopEnv.is_xfce():
        _set_xfce_wallpaper(wallpaper_path)
    
    elif DesktopEnv.is_kde():
        _set_kde_wallpaper(wallpaper_path)
    
    else:
        raise NotImplementedError('Unsupported Operating System or Desktop Environment.')
    
    time.sleep(1)  # Wait for the things to apply.

