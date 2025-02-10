import os

script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, 'assets')
wallpapers_dir = os.path.join(assets_dir, 'wallpapers')
icons_dir = os.path.join(assets_dir, 'icons')

payload = os.path.join(wallpapers_dir, 'monika-missing-linux.png')

app_icon = os.path.join(icons_dir, 'heart.svg')