"""run.py."""

import os
from urllib.parse import urlparse

from core.logger import setup_logger
from core.runner import save_results
from dotenv import load_dotenv

logger = setup_logger("main")
load_dotenv()


def detect_site_from_url(url: str) -> str:
    """Parses the domain from a URL and returns a normalized site name."""
    try:
        hostname = urlparse(url).hostname
        if not hostname:
            return "unknown"

        known_sites = {"kemono.su": "kemono"}

        return known_sites.get(hostname.lower(), hostname.split(".")[-2])

    except Exception as e:
        logger.error(f"Failed to detect site from URL: {e}")
        return "unknown"


if __name__ == "__main__":
    load_dotenv()

    url = os.getenv("TARGET_URL")
    if not url:
        logger.error("Error: TARGET_URL not set in .env")
        exit(1)

    site = detect_site_from_url(url)
    logger.info(f"Detected site: {site}")

    image_file = f"{site}_images.txt"
    href_file = f"{site}_hrefs.txt"

    save_results(url, site, image_file, href_file)
