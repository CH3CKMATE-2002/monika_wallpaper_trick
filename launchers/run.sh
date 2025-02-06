#!/usr/bin/env bash
# ╔═════════════════╦════════════════════════════════════════════════════════════╗
# ║ Author          ║ CH3CKMATE-2002 (Andreas Hanna)                             ║
# ╠═════════════════╬════════════════════════════════════════════════════════════╣
# ║ Contributors    ║ Monika                                                     ║
# ╚═════════════════╩════════════════════════════════════════════════════════════╝

# ══════════════════════════════════════╗
# ║ Script Metadata                     ║
# ══════════════════════════════════════╝
SCRIPT_PATH="$(readlink -f "$0")"                             # Full path of the script.
PARENT_DIR="$(dirname "${SCRIPT_PATH}")"                      # Parent directory of the script.
SCRIPT_NAME="$(basename "${SCRIPT_PATH}" | cut -d '.' -f 1)"  # Name of the script (without extension, regardless what it is).
SCRIPT_AUTHOR='CH3CKMATE-2002 (Andreas Hanna)'
SCRIPT_CONTRIBUTORS=(
    'Monika'            # I can't seemingly to remove her name... She's cute, isn't she?
)
SCRIPT_VERSION='1.0'
SCRIPT_COPYRIGHT="Copyright@2024 by ${SCRIPT_AUTHOR}"

# Tests if a command exists or not
function command_exists() {
    command -v "$@" &> '/dev/null'
}

cd "$PARENT_DIR" || { echo "Failed to change directory to: $PARENT_DIR" >&2 ; exit 1; }
cd '..'

#### Launcher code ####
if ! command_exists 'python3'; then
    echo "You must install python 3 to run this app." >&2
    exit 1
fi

python3 'main.py' "$@"  # This is better, since it ensures that the script will run using python3
