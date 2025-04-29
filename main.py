from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from web_scrapper import get_images_from_google
from reviewer import review_images

if __name__ == "__main__":
    # Setup ChromeDriver
    PATH = "C:/Users/yassi/Desktop/Projet/CookBotProject/WebScrappingDownloads/chromedriver.exe" 
    service = Service(executable_path=PATH)
    wd = webdriver.Chrome(service=service)

    # Scrape images
    search_query = "cucumber on table"
    urls = get_images_from_google(search_query, wd, delay=1, max_images=5)
    wd.quit()

    # Review and selectively download
    review_images(urls, save_folder="imgs/")
