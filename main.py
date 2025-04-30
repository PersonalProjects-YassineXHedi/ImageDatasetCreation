from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from web_scrapper import get_images_from_google
from reviewer9 import review_images

if __name__ == "__main__":
    # Setup ChromeDriver
    PATH = "C:/Users/yassi/Desktop/Projet/CookBotProject/WebScrappingDownloads/chromedriver.exe" 
    service = Service(executable_path=PATH)
    wd = webdriver.Chrome(service=service)

    # Scrape images
    search_query = "lemon on table"
    urls = get_images_from_google(search_query, wd, delay=1, max_images=300)
    print(urls)
    wd.quit()

    # Review and selectively download
    review_images(urls, save_folder_path="OutputData/",subfolder_name='lemon')
