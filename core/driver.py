"""core/driver.py."""

import os
import sys

from core.logger import setup_logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logger = setup_logger("driver")
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


def find_brave_path():
    """Find brave path in common os directories."""
    if sys.platform.startswith("win"):
        path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
        if os.path.isfile(path):
            return path
        raise FileNotFoundError(f"Brave browser not found at {path}")

    elif sys.platform.startswith("linux"):
        candidates = [
            "/usr/bin/brave-browser",
            "/usr/bin/brave",
            os.path.expanduser("~/.config/BraveSoftware/Brave-Browser/brave-browser"),
        ]
        for path in candidates:
            if os.path.isfile(path) and os.access(path, os.X_OK):
                return path
        raise FileNotFoundError(
            "Brave browser executable not found in common Linux locations."
        )

    elif sys.platform == "darwin":
        path = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path
        raise FileNotFoundError("Brave browser not found in macOS Applications folder.")

    else:
        raise OSError("Unsupported OS for Brave detection")


def setup_driver():
    """Set up and return a headless Chrome or Brave WebDriver based on env flag."""
    options = Options()

    use_brave = os.getenv("USE_BRAVE", "0") == "1"

    if use_brave:
        brave_path = find_brave_path()
        logger.info(f"Using Brave browser at: {brave_path}")
        options.binary_location = brave_path
    else:
        logger.info("Using default Chrome browser")

    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    return driver
