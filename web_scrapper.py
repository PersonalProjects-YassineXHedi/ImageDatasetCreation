from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_images_from_google(search_type, query, wd, delay, max_images):
    match search_type:
        case 'images':
            get_images_from_google_images(query, wd, delay, max_images)
        case 'shoppings':
            get_images_from_google_shop(query, wd, delay, max_images)



def get_images_from_google_images(query, wd, delay, max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollBy(0, document.body.scrollHeight);")
        time.sleep(delay)

    url = f"https://www.google.com/search?q={query}&tbm=isch"
    wd.get(url)

    image_urls = set()
    skips = 0
    last_index = 0

    while len(image_urls) + skips < max_images:
        try:
            WebDriverWait(wd, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "F0uyec"))
            )
            thumbnails = wd.find_elements(By.CLASS_NAME, "F0uyec")
        except Exception as e:
            print(e)
            skips += 1
            max_images += 1
            continue
        for thumb in thumbnails[last_index:]:
            if(len(image_urls) + skips >= max_images):
                break
            last_index += 1
            try:
                wd.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center', inline: 'center'});", thumb)
                time.sleep(delay/2)
                if thumb.is_displayed() and thumb.is_enabled():
                    actions = ActionChains(wd)
                    actions.move_to_element(thumb).pause(0.3).click().perform()
                    time.sleep(delay)
                else:
                    skips += 1
                    max_images += 1
                    continue

            except Exception as e:
                print(e)
                skips += 1
                max_images += 1
                continue
            
            try:
                WebDriverWait(wd, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "img.sFlh5c.FyHeAf.iPVvYb"))
                )
            except Exception as e:
                print(e)
                skips += 1
                max_images += 1
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
                max_images += 1
                continue
        scroll_down(wd)

        
    return list(image_urls)

def get_images_from_google_shop(query, wd, delay, max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollBy(0, document.body.scrollHeight);")
        time.sleep(delay)

    url = f"https://www.google.com/search?q={query}&tbm=shop"
    wd.get(url)

    image_urls = set()
    skips = 0
    last_index = 0

    while len(image_urls) + skips < max_images:
        try:
            WebDriverWait(wd, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "njFjte"))
            )
            thumbnails = wd.find_elements(By.CLASS_NAME, "njFjte")
        except Exception as e:
            print(e)
            skips += 1
            max_images += 1
            continue
        for thumb in thumbnails[last_index:]:
            if(len(image_urls) + skips >= max_images):
                break
            last_index += 1
            try:
                wd.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center', inline: 'center'});", thumb)
                time.sleep(delay/2)
                if thumb.is_displayed() and thumb.is_enabled():
                    actions = ActionChains(wd)
                    actions.move_to_element(thumb).pause(0.3).click().perform()
                    time.sleep(delay)
                else:
                    skips += 1
                    max_images += 1
                    continue

            except Exception as e:
                print(e)
                skips += 1
                max_images += 1
                continue
            
            try:
                WebDriverWait(wd, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "KfAt4d"))
                )
            except Exception as e:
                print(e)
                skips += 1
                max_images += 1
                continue
            images = wd.find_elements(By.CLASS_NAME, "KfAt4d")
            
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
                max_images += 1
                continue
        scroll_down(wd)

        
    return list(image_urls)
