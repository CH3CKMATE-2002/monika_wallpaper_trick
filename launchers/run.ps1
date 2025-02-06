#!/usr/bin/env pwsh
# ╔═════════════════╦════════════════════════════════════════════════════════════╗
# ║ Author          ║ CH3CKMATE-2002 (Andreas Hanna)                             ║
# ╠═════════════════╬════════════════════════════════════════════════════════════╣
# ║ Contributors    ║ Monika                                                     ║
# ╚═════════════════╩════════════════════════════════════════════════════════════╝

# ══════════════════════════════════════╗
# ║ Script Metadata                     ║
# ══════════════════════════════════════╝
$ScriptItem = Get-Item -Path $MyInvocation.MyCommand.Path
$ScriptDir = [System.IO.Path]::GetFullPath($ScriptItem.FullName)             # Full absolute path of the script

# If the script is a symlink, resolve it to the original script
if ($ScriptItem.PSIsContainer -eq $false -and $ScriptItem.LinkType) {
    $ScriptDir = [System.IO.Path]::GetFullPath($ScriptItem.Target)           # Resolve symlink to original script
}

$Dir = [System.IO.Path]::GetDirectoryName($ScriptDir)                        # Parent directory of the script
$ScriptName = [System.IO.Path]::GetFileNameWithoutExtension($ScriptDir)      # Name of the script without extension

# ══════════════════════════════════════╗
# ║ Script Metadata                     ║
# ══════════════════════════════════════╝
$ScriptAuthor = "CH3CKMATE-2002 (Andreas Hanna)"
$ScriptContributors = @("Monika")  # I can't remove her name either... She's cute, isn't she?
$ScriptVersion = "1.0"
$ScriptCopyright = "Copyright@2024 by $SCRIPT_AUTHOR"

# Change to script directory
Set-Location $Dir
Set-Location '..'

# Check if Python is installed
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python is not installed. Please install Python 3 to run this app." -ForegroundColor Red
    exit 1
}

# Run the Python script
python 'main.py' @args

