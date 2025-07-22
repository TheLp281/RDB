"""core/utils.py."""

import os
import time

import requests
from core.logger import setup_logger

DATA_FOLDER = "data"

logger = setup_logger("utils")


def is_valid_img_url(url):
    """Return True if URL is a valid image link to process."""
    if not url:
        return False
    url = url.lower()
    return not url.endswith((".svg", ".ico", ".gif")) and not any(
        keyword in url
        for keyword in [
            "smartpop",
            "tracking",
            "pixel",
            "adserver",
            "ad.",
            "/ads/",
            "analytics",
            "campaignid",
            "usertracking",
            "icons",
            "favicon",
            "fanbox",
        ]
    )


MAX_RETRIES = 3
RETRY_DELAY = 2
def notify_new_posts(new_imgs, new_hrefs):
    """Send Discord notifications pairing each new image URL with a new post link."""
    webhook_url = os.getenv("DISCORD_WEBHOOK")
    if not webhook_url:
        logger.warning("No webhook URL found in .env.")
        return

    img_list = sorted(new_imgs, reverse=True)
    href_list = sorted(new_hrefs, reverse=True)

    paired_posts = list(zip(img_list, href_list, strict=False))
    if not paired_posts:
        logger.info("No new posts to notify.")
        return

    for index, (img_url, post_url) in enumerate(paired_posts, 1):
        payload = {
            "embeds": [
                {
                    "title": "New post found",
                    "description": f"[Click here to view the post]({post_url})",
                    "image": {"url": img_url},
                }
            ]
        }

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = requests.post(webhook_url, json=payload)

                if response.status_code == 204:
                    logger.info(f"Sent post {index}/{len(paired_posts)} to Discord.")
                    break
                elif response.status_code == 429:
                    retry_after = response.json().get("retry_after", 1000) / 1000
                    logger.warning(
                        f"Rate limited. Retrying in {retry_after:.2f} seconds..."
                    )
                    time.sleep(retry_after + 0.5)
                else:
                    logger.error(
                        f"Attempt {attempt}: Failed ({response.status_code}) {response.text}"
                    )
                    time.sleep(RETRY_DELAY)

            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt}: Exception while sending: {e}")
                time.sleep(RETRY_DELAY)

        else:
            logger.error(f"All attempts failed to send post {index}/{len(paired_posts)}.")
            

def ensure_data_folder():
    """Create data folder if it does not exist."""
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)


def get_data_file_path(filename: str) -> str:
    """Return full path to data file inside the data folder."""
    ensure_data_folder()
    return os.path.join(DATA_FOLDER, filename)


def read_saved(filename: str):
    """Read saved entries from file, return as a set of lines."""
    file_path = get_data_file_path(filename)
    if os.path.exists(file_path):
        with open(file_path, encoding="utf-8") as f:
            return {line.strip() for line in f if line.strip()}
    return set()


def write_new_entries(filename: str, new_entries):
    """Append new entries to the given file."""
    file_path = get_data_file_path(filename)
    with open(file_path, "a", encoding="utf-8") as f:
        for entry in new_entries:
            f.write(entry + "\n")
