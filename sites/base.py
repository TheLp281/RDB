"""sites/base.py."""


class SiteParser:
    """Base parser class with placeholder methods."""

    def __init__(self, driver):
        """Initialize with a Selenium WebDriver instance."""
        self.driver = driver

    def extract_image_urls(self):
        """Return a set of image URLs (to be implemented by subclasses)."""
        return set()

    def extract_post_hrefs(self):
        """Return a set of post URLs (to be implemented by subclasses)."""
        return set()
