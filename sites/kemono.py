"""sites/kemono.py."""

from core.utils import is_valid_img_url
from selenium.webdriver.common.by import By

from .base import SiteParser


class KemonoParser(SiteParser):
    """Parser for Kemono site to extract image URLs and post links."""

    def extract_image_urls(self):
        """Return a set of valid image URLs found on the page."""
        img_elements = self.driver.find_elements(By.TAG_NAME, "img")
        return {
            img.get_attribute("src")
            for img in img_elements
            if is_valid_img_url(img.get_attribute("src"))
        }

    def extract_post_hrefs(self):
        """Return a set of post URLs containing '/post/'."""
        link_elements = self.driver.find_elements(
            By.CSS_SELECTOR, "a.fancy-link--kemono"
        )
        return {
            link.get_attribute("href")
            for link in link_elements
            if link.get_attribute("href") and "/post/" in link.get_attribute("href")
        }
