from selenium import webdriver
import requests
import io
from PIL import Image
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time


def get_images_from_google(wd, delay, max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollBy(0, document.body.scrollHeight);")
        time.sleep(delay)

    url = "https://www.google.com/search?sca_esv=cdf2793c44a7e080&rlz=1C1PNJJ_frTN1069TN1069&q=meyer+lemons+lemon+on+table&uds=ABqPDvztZD_Nu18FR6tNPw2cK_RRgTc7n8IPBVhFYlxFFMaqzjOkqu3fJnBTz0dFfqrjcYug16cnJOHyOLb8lIrWepC7DE37G0yK6_Pk7oJlzTFFNfkCBdqi1I_XAdjjFF-GQGne3GoIo5XADUi7uQC2opwWo3xxxw&udm=2&sa=X&ved=2ahUKEwj2wYbB1_uMAxUiF2IAHSMIMWkQxKsJegQIDhAB&ictx=0&biw=1036&bih=651&dpr=1.25"
    wd.get(url)

    image_urls = set()
    skips = 0

    while len(image_urls) + skips < max_images:
        thumbnails = wd.find_elements(By.CLASS_NAME, "F0uyec")

        for thumb in thumbnails[len(image_urls) + skips:max_images]:
            try:
                wd.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center', inline: 'center'});", thumb)
                time.sleep(0.5)

                if thumb.is_displayed() and thumb.is_enabled():
                    thumb.click()
                    time.sleep(delay)
                else:
                    skips += 1
                    continue

            except Exception as e:
                print(e)
                skips += 1
                continue

            images = wd.find_elements(By.CSS_SELECTOR,"img.sFlh5c.FyHeAf.iPVvYb")
            
            found_valid_image = False
            for image in images:
                if image.get_attribute('src') in image_urls:
                    max_images += 1
                    skips += 1
                    break

                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(f"Found {len(image_urls)}")
                    found_valid_image = True
            if not found_valid_image:
                skips += 1
                continue
        scroll_down(wd)
    return list(image_urls)

