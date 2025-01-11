"""Logging methods used exclusively in management commands."""

from colorama import Fore


def log_ok() -> str:
    """Return a green `[ OK ]` string."""
    return "[" + Fore.GREEN + " OK " + Fore.RESET + "]"


def log_warning() -> str:
    """Return a yellow `[ WARNING ]` string."""
    return "[" + Fore.YELLOW + " WARNING " + Fore.RESET + "]"
