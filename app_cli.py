import argparse
from dataclasses import dataclass

@dataclass
class ParsedArgs:
    help: bool
    about: bool
    verbose: int | None
    no_colored_log: bool

def parse_arguments(args: list[str]) -> ParsedArgs:
    """Parses command-line arguments and returns a structured object."""
    
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "--help", action="store_true")
    parser.add_argument("--about", action="store_true")
    parser.add_argument("-v", "--verbose", nargs="?", const=1, type=int)
    parser.add_argument("--no-colored-log", action="store_true")

    parsed_args = parser.parse_args(args)

    return ParsedArgs(
        help=parsed_args.help,
        about=parsed_args.about,
        verbose=parsed_args.verbose,
        no_colored_log=parsed_args.no_colored_log
    )

def show_usage():
    print("Usage: main.py [options]")
    print("Description: Monika temporarily takes over your wallpaper for fun.")
    print("Options:")
    print("  -h, --help              Show this help message and exit")
    print("  --about                 Show about message and exit")
    print("  -v[N], --verbose[=N]    Set verbosity (1=INFO, 2=WARNING, 3=DEBUG).")
    print("  --no-colored-log        Disable ANSI colors in logs")
    print()

def show_about():
    print("Monika's Prank - Wallpaper Takeover")
    print("Version: 1.0.0")
    print("Author: CH3CKMATE-2002")
    print("Co-author: Monika 💚")
    print("Description: A fun prank where Monika hijacks your wallpaper, then apologizes.")
    print()