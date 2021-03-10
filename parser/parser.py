import os
from time import sleep

from selenium import webdriver
from urllib.request import urlretrieve


class Parser:
    def __init__(self, driver_path="chromedriver", colab=False):
        """Initialize main class variables.

        :param driver_path: Path to chromedriver.
        :type driver_path: str
        :param colab: Is the code running on google colaboratory?
        :type colab: bool
        """

        if colab:
          options = webdriver.ChromeOptions()
          options.add_argument('--headless')
          options.add_argument('--no-sandbox')
          options.add_argument('--disable-dev-shm-usage')
          self.wb = webdriver.Chrome(driver_path,options=options)
        else:
          self.wb = webdriver.Chrome(driver_path)

    def parse_images(self, base_url, page_url, images_dir):
        """Download images from url.

        :param base_url: Page url.
        :type base_url: str
        :param page_url: Url to open several pages.
        :type page_url: str
        :param images_dir: Dir to save images.
        :type images_dir: str

        :return: True when everything is downloaded
        """

        # Create home images dir
        if not os.path.exists(images_dir):
            os.mkdir(images_dir)

        # Create class images dir
        images_dir = os.path.join(images_dir, base_url.split("/")[-1])
        if not os.path.exists(images_dir):
            os.mkdir(images_dir)

        # Run main script
        page_id = 1
        while True:
            # Make url for each page
            if page_url:
                url = base_url + page_url + str(page_id)
                page_id += 1
            else:
                url = base_url

            # Download site
            self.wb.get(url)
            page_state = False
            while not page_state:
                page_state = self._page_has_loaded()

            # Slow scroll to download all images
            self._slow_scroll()

            # Get images from site
            images = self.wb.find_elements_by_class_name("thumbnail")
            if not images:
                return True  # TODO: Normal exit

            # Save images
            for image in images:
                image_url = image.get_attribute("src")
                if image_url.endswith(".jpg"):
                    image_name = "-".join(image_url.split("/")[-2:])
                    image_path = os.path.join(images_dir, image_name)
                    if not os.path.exists(image_path):
                        urlretrieve(image_url, image_path)
                else:
                    print("Image not downloaded from website")

    def _page_has_loaded(self):
        """Check if the page is loaded.

        :return: Boolean, True if page is loaded.
        """

        page_state = self.wb.execute_script('return document.readyState;')
        return page_state == 'complete'

    def _slow_scroll(self, delta=500, time_delta=0.1):
        """Scroll the page.

        :param delta: Pixel delta to scroll each time.
        :type delta: int
        :param time_delta: Time delta to wait between scrolls.
        :type time_delta: int
        """

        max_height = self.wb.execute_script('return document.body.scrollHeight;')
        for i in range(0, max_height, delta):
            self.wb.execute_script(f"window.scrollTo(0, {i})")
            sleep(time_delta)
