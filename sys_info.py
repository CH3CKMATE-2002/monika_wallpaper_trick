import platform, os

CURRENT_OS = platform.system().lower()
DESKTOP_ENV = os.environ.get('XDG_SESSION_DESKTOP', '').lower()


class System:
    @staticmethod
    def is_linux():
        return CURRENT_OS == 'linux'
    
    @staticmethod
    def is_windows():
        return CURRENT_OS == 'windows'
    
    @staticmethod
    def is_macos():
        return CURRENT_OS == 'darwin'
    
    def get():
        return CURRENT_OS


class DesktopEnv:
    @staticmethod
    def is_gnome():
        return DESKTOP_ENV == 'ubuntu' or DESKTOP_ENV == 'gnome'
    
    @staticmethod
    def is_kde():
        return DESKTOP_ENV == 'kde'
    
    @staticmethod
    def is_xfce():
        return DESKTOP_ENV == 'xfce'
    
    @staticmethod
    def is_cinnamon():
        return DESKTOP_ENV == 'cinnamon'
    
    @staticmethod
    def is_mate():
        return DESKTOP_ENV == 'mate'
    
    def get():
        return DESKTOP_ENV


if __name__ == '__main__':
    print(f"I am your {System.get().capitalize()} device.")
    if System.is_linux():
        print(f"You're running the {DesktopEnv.get().capitalize()} desktop environment.")