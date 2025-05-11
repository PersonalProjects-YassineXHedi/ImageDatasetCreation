from web_scrapper import get_urls_from_query
from reviewer9 import review_images

if __name__ == "__main__":
    
    # Setup ChromeDriver
    PATH = "C:/Users/yassi/Desktop/Projet/CookBotProject/WebScrappingDownloads/chromedriver.exe"

    # Scrape images
    search_type = 1 #It can be either shoppings (1) or images (0) or both (2)
    search_query = "mustard"
    start_from_buttom = True
    urls = get_urls_from_query(PATH, search_type, search_query, delay = 1, max_images = 2, start_from_bottom= start_from_buttom)

    # Review and selectively download
    review_images(urls, save_folder_path="OutputData/",subfolder_name='test')
 