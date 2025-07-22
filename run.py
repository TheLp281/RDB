"""run.py."""

import os
from urllib.parse import urlparse

from core.logger import setup_logger
from core.runner import save_results
from dotenv import load_dotenv

logger = setup_logger("main")
load_dotenv()


def detect_site_from_url(url: str) -> str:
    """Extracts and returns the domain (hostname) from a URL."""
    try:
        hostname = urlparse(url).hostname
        return hostname.lower() if hostname else "unknown"
    except Exception as e:
        logger.error(f"Failed to detect site from URL: {e}")
        return "unknown"


if __name__ == "__main__":
    load_dotenv()

    urls_string = os.getenv("TARGET_URLS")
    if not urls_string:
        logger.error("Error: TARGET_URLS not set in .env")
        exit(1)

    urls = [u.strip() for u in urls_string.split(",") if u.strip()]
    if not urls:
        logger.error("Error: No valid URLs found in TARGET_URLS")
        exit(1)

    for url in urls:
        site = detect_site_from_url(url)
        logger.info(f"Processing URL: {url}")
        logger.info(f"Detected site: {site}")

        image_file = f"{site}_images.txt"
        href_file = f"{site}_hrefs.txt"

        save_results(url, site, image_file, href_file)
