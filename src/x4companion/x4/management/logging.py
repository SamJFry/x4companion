"""Logging methods used exclusively in management commands."""

from colorama import Fore


def log_ok() -> str:
    """Return a green `[ OK ]` string."""
    return "[" + Fore.GREEN + " OK " + Fore.RESET + "]"
