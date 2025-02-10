import subprocess
from pathlib import Path

from app_paths import app_icon
from sys_info import System
from omega_logger import OmegaLogger, global_logger


if System.is_linux():
    from pydbus.bus import SessionBus, Bus
elif System.is_windows():
    from win10toast import ToastNotifier  # type: ignore
else:
    pass  # TODO: MacOS with no subprocesses?


notifier_logger = OmegaLogger(name=__name__, verbosity=global_logger.verbosity)


class Notifier:
    def __init__(self, app_name: str, app_icon: str | Path):
        self.app_name = app_name
        self.app_icon = Path(app_icon) if isinstance(app_icon, str) else app_icon
        
        if System.is_linux():
            self.bus: Bus = SessionBus()
            self._bus_obj = self.bus.get(".Notifications")
        else:
            self.bus = None
            self._bus_obj = None

    def notify(self, title: str, message: str):
        if System.is_linux():
            self._notify_linux(title, message)
        elif System.is_windows():
            self._notify_windows(title, message)
        elif System.is_macos():  # MacOS
            self._notify_macos(title, message)
        else:
            raise NotImplementedError(f"Notifications are not supported on {System.get()}")

    def _notify_linux(self, title: str, message: str):
        try:
            self._bus_obj.Notify(
                self.app_name,                  # app_name
                0,                              # replaces_id
                str(self.app_icon.absolute()),  # app_icon
                title,                          # summary
                message,                        # body
                [],                             # actions
                {},                             # hints
                -1                              # expire_timeout (milliseconds)
            )
        except Exception as e:
            notifier_logger.warning(f'Dbus notifications failed: {e}')
            subprocess.run(
                ["notify-send", title, message, "-i", str(self.app_icon.absolute())]
                    if self.app_icon.exists()
                    else ["notify-send", title, message],
                check=False
            )
    
    def _notify_windows(self, title: str, message: str):
        try:
            toaster = ToastNotifier()
            toaster.show_toast(title, message, duration=5)
        except Exception as e:
            notifier_logger.error(f'Failed to send toast: {e}')
    
    def _notify_macos(self, title: str, message: str):
        try:
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(["osascript", "-e", script], check=False)
        except Exception as e:
            notifier_logger.error(f'Failed to send notification: {e}')



app_notifier = Notifier(app_name="Monika's Trick!", app_icon=app_icon)
