from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import concurrent.futures
import time

CHROME_VERSION = 135

def get_urls_from_query(executable_path, search_type, search_query, delay, max_images):
    futures = []
    urls =[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        if(search_type == 0):
            futures.append(executor.submit(get_images_from_google, executable_path, 'images', search_query, delay, max_images))
        elif(search_type == 1):
            futures.append(executor.submit(get_images_from_google, executable_path, 'shoppings', search_query, delay, max_images))
        elif (search_type == 2):
            futures.append(executor.submit(get_images_from_google, executable_path, 'images', search_query, delay, max_images//2))
            futures.append(executor.submit(get_images_from_google, executable_path, 'shoppings', search_query, delay, max_images//2))
        else:
            print('This is a wrong search type.')
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result is not None:
                urls.extend(result)
    print(urls)
    return urls



def get_images_from_google(executable_path, search_type, query, delay, max_images):
    match search_type:
        case 'images':
            return get_images_from_google_images(executable_path, query, delay, max_images)
        case 'shoppings':
            return get_images_from_google_shop(query, delay, max_images)

def scroll_down(wd, delay):
    try:
        last_height = wd.execute_script("return document.body.scrollHeight")
        wd.execute_script("window.scrollBy(0, document.body.scrollHeight);")
        time.sleep(delay)
        new_height = wd.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("Reached the end of the page.")
            return False
        return True
    except Exception as e:
        print(e)
        return False

def get_images_from_google_images(executable_path, query, delay, max_images):
    service = Service(executable_path=executable_path)

    chrome_options = Options()
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
    )

    wd = webdriver.Chrome(service=service, options=chrome_options)

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
        if(not scroll_down(wd, delay)):
            break
    wd.quit()    
    return list(image_urls)

def get_images_from_google_shop(query, delay, max_images):
    options = uc.ChromeOptions()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
    )

    wd = uc.Chrome(options=options, version_main=CHROME_VERSION)

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
        if(not scroll_down(wd, delay)):
            break
    wd.quit()    
    return list(image_urls)
