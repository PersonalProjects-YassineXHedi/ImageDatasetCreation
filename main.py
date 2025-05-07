from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from web_scrapper import get_urls_from_query
from reviewer9 import review_images

if __name__ == "__main__":
    
    # Setup ChromeDriver
    PATH = "C:/Users/yassi/Desktop/Projet/CookBotProject/WebScrappingDownloads/chromedriver.exe" 
    service = Service(executable_path=PATH)
    wd = webdriver.Chrome(service=service)

    # Scrape images
    search_type = 1 #It can be either shoppings (1) or images (0) or both (2)
    search_query = "mustard"
    urls = get_urls_from_query(PATH, search_type, search_query, delay = 1, max_images = 10)

    # Review and selectively download
    review_images(urls, save_folder_path="OutputData/",subfolder_name='test')
 