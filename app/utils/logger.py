from termcolor import colored
from typing import Any

def log_info(message: Any) -> None:
    """Print info messages in yellow"""
    print(colored(f"[INFO] {message}", "yellow"))

def log_success(message: Any) -> None:
    """Print success messages in green"""
    print(colored(f"[SUCCESS] {message}", "green"))

def log_error(message: Any) -> None:
    """Print error messages in red"""
    print(colored(f"[ERROR] {message}", "red")) 