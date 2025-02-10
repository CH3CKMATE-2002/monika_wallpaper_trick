"""
@author: CH3CKMATE-2002
"""

#### 🚨 A Rant About the Windows Native API 🚨 ####
# WHY, MICROSOFT?!
# Why do you keep creating things that could be great,
# only to mess them up later?! Why do you insist on hiding
# information from users and effectively lying to them?
# Take this ridiculous mess, for example:
# You'd think retrieving a user's real name would be simple, right?
# Well, it kinda works - until the user changes their username. 
# That's when everything falls apart.
# See, Windows maintains two different names:
# - The original username (the one used internally for system paths, permissions, and authentication).
# - The display name (the one you see on the login screen).
# When a user changes their username in Settings, Windows only updates the display name,
# not the real one. So when a program (like this one) tries to
# retrieve the system username, it gets the original name instead of the one the user expects.
# This is why, in Doki Doki Literature Club!, Monika - thinking she’s clever - reads
# the system username, assuming it's your real name.
# But if your original username was "Admin" or "Bob",
# well... guess what? That's what Monika calls you.
# And now she just looks dumb.
# It's a missed opportunity - the effect could have been way cooler
# if Windows actually returned the correct name.
# Instead, Microsoft decided to gaslight both Monika and the player.
# Now contrast this with Unix/Linux, where everything is beautifully simple:
# Your system username is stored in /etc/passwd, a plain text file.
# Programs can just read it, split a line by ':',
# and grab the real user name - no syscalls, no nonsense.
# Compare that to Windows, where you need to import ctypes, handle DWORDs, manage buffers,
# and pray to the Microsoft gods that it returns the right value.
# Windows, you could have made this simple… but you just had to make it complicated.
# Sigh...
# Thanks for yet again not trusting your users, Microsoft! 🙃
#### Rant End ####

import os
import platform
from sys_info import System

def get_real_name() -> str:
    if System.is_windows():
        try:
            import ctypes
            from ctypes import wintypes, windll, byref

            name_display = 3  # NameDisplay format
            size = wintypes.DWORD(0)  # DWORD... DWORD everywhere!
            secur32 = windll.secur32

            # First call to get buffer size
            if not secur32.GetUserNameExW(name_display, None, byref(size)):
                buffer = ctypes.create_unicode_buffer(size.value)
                # Second call to get actual name
                if secur32.GetUserNameExW(name_display, buffer, byref(size)):
                    return buffer.value.strip()
            return None
        
        except Exception:
            return None
    else:  # Witness how simple Unix it is!!
        # Your system username will be stored inside
        # one of these environment variables. (if not both!)
        username = os.environ.get('USER') or os.environ.get('USERNAME')
        etc_passwd = '/etc/passwd'  # Information about all the system's user is there.

        # Sometimes, the env vars might not be set for various rare reasons
        if username is None:
            return None  # Oh, well... At least better than getting 'ctypes' errors.

        try:
            # Read the damn file...
            with open(etc_passwd, 'r') as passwd:
                # Move on each entry (line by line)
                for entry in passwd:
                    # If the line starts with your username, congratulations!
                    if entry.startswith(f"{username}:"):
                        # The fields are separated with ':'
                        parts = entry.split(':')
                        # There should be more than five fields if it is
                        # a user field.
                        if len(parts) >= 5:
                            # Get the fifth field, trim ',' and ensure it
                            # is stripped.
                            real_name = parts[4].split(',')[0].strip()
                            # Poof! No native API or sys call shit!
                            return real_name if real_name else None
                return None
        except FileNotFoundError:
            return None