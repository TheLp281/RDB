"""Core runner module to fetch and process site data using Selenium and parsers."""

import time

from core.driver import setup_driver
from core.logger import setup_logger
from core.utils import notify_new_posts, read_saved, write_new_entries
from sites.kemono import KemonoParser

logger = setup_logger("runner")


def save_results(url, site_name, image_file, href_file):
    """Load URL, parse with site parser, find new images and post links,.

    and send paired Discord notifications per post.
    """
    from selenium.common.exceptions import WebDriverException

    try:
        driver = setup_driver()
        driver.get(url)
        time.sleep(5)
        parser = None
        if site_name == "kemono.su":
            parser = KemonoParser(driver)
        else:
            logger.error(f"Parser not found for site: {site_name}")
            return
        img_urls = parser.extract_image_urls()
        hrefs = parser.extract_post_hrefs()
        driver.quit()

        saved_imgs = read_saved(image_file)
        saved_hrefs = read_saved(href_file)

        new_imgs = img_urls - saved_imgs
        new_hrefs = hrefs - saved_hrefs

        new_imgs = sorted(new_imgs, reverse=True)
        new_hrefs = sorted(new_hrefs, reverse=True)

        if new_imgs or new_hrefs:
            logger.info(
                f"Discovered {len(new_imgs)} new images and "
                f"{len(new_hrefs)} new post links"
            )

        notify_new_posts(new_imgs, new_hrefs)

        if new_imgs:
            write_new_entries(image_file, new_imgs)
        if new_hrefs:
            write_new_entries(href_file, new_hrefs)

    except WebDriverException as e:
        print(f"WebDriver error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
