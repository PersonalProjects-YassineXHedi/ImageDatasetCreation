import tkinter as tk
from tkinter import messagebox
import threading
from web_scrapper import get_urls_from_query
from reviewer9 import review_images

PATH = "C:/Users/yassi/Desktop/Projet/CookBotProject/WebScrappingDownloads/chromedriver.exe"


def lunch_scrapping_setup_window(path):
    global query_entry, number_of_images, source_var_images, source_var_shopping, folder_name_entry, root


        
  
    root = tk.Tk()
    root.title("Scraper Setup")
    root.geometry("700x300")


    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(4, weight=1)  


    tk.Label(root, text="Query:", font=('calibre', 14, 'bold')).grid(row=0, column=0, padx=20, pady=15, sticky="e")
    query_entry = tk.Entry(root, font=('calibre', 14), width=40)
    query_entry.grid(row=0, column=1, padx=20, pady=15, sticky="w")

    tk.Label(root, text="Number of Images:", font=('calibre', 14, 'bold')).grid(row=1, column=0, padx=20, pady=15, sticky="e")
    number_of_images = tk.Entry(root, font=('calibre', 14), width=40)
    number_of_images.grid(row=1, column=1, padx=20, pady=15, sticky="w")

    tk.Label(root, text="Folder Name:", font=('calibre', 14, 'bold')).grid(row=2, column=0, padx=20, pady=15, sticky="e")
    folder_name_entry = tk.Entry(root, font=('calibre', 14), width=40)
    folder_name_entry.grid(row=2, column=1, padx=20, pady=15, sticky="w")

    source_var_images = tk.IntVar()
    source_var_shopping = tk.IntVar()

    tk.Label(root, text="Scraping Source:", font=('calibre', 14, 'bold')).grid(row=3, column=0, padx=20, pady=10, sticky="e")

    checkbox_frame = tk.Frame(root)
    checkbox_frame.grid(row=3, column=1, sticky="w", padx=20)

    chk_images = tk.Checkbutton(checkbox_frame, text="Google Images", variable=source_var_images, font=('calibre', 14))
    chk_images.pack(side="left", padx=10)

    chk_shopping = tk.Checkbutton(checkbox_frame, text="Google Shopping", variable=source_var_shopping, font=('calibre', 14))
    chk_shopping.pack(side="left", padx=10)

    tk.Label(root).grid(row=4, column=0)

    start_button = tk.Button(root, text="Start Scraping", font=('calibre', 14), width=20, command=start_scraping)
    start_button.grid(row=5, column=1, pady=20, padx=20, sticky="e")


    root.mainloop()


def start_scraping():
    if not check_entries():
        return
    waiting_window = switch_to_waiting_window(root)
    run_scraping(waiting_window)

def run_scraping(waiting_window):
    search_type = get_search_type()
    urls = get_urls_from_query(PATH, search_type, query_entry.get(), delay=1, max_images=int(number_of_images.get()))
    waiting_window.destroy()
    folder_name = folder_name_entry.get()
    root.destroy()
    if(urls):
        review_images(urls, save_folder_path="OutputData/", subfolder_name=folder_name)
    

def get_search_type():
    if(source_var_images.get() == 1 and source_var_shopping.get() != 1):
        return 0
    if(source_var_shopping.get() == 1 and source_var_images.get() != 1):
        return 1
    if(source_var_shopping.get() == 1 and source_var_images.get() == 1):
        return 2

def switch_to_waiting_window(root):
    root.withdraw()
    new_window = tk.Toplevel(root)
    new_window.geometry("700x300")
    new_window.title("Waiting Window")
    tk.Label(
        new_window,
        text="Images Scrapping is in progress, please wait!",
        font=("Helvetica", 24)
    ).pack(expand=True, fill="both")
    return new_window

def check_chekbox_entry():
    if(source_var_images.get() != 1 and source_var_shopping.get() != 1):
        messagebox.showerror("Error", "You need to check at least a scrapping source!")
        return False
    return True

def check_image_number_entry():
    value = number_of_images.get().strip()
    if not value:
        messagebox.showerror("Error", "The number of images cannot be empty!")
        return False
    try:
        num = int(value)
        if num <= 0:
            messagebox.showerror("Error", "The number must be greater than 0!")
            return False
    except ValueError:
        messagebox.showerror("Error", "The number must be an integer!")
        return False
    return True

def check_string_entry(entry):
    query_text = entry.get().strip()
    if not query_text:
        messagebox.showerror("Error", "The search query cannot be empty!")
        return False
    if not query_text.replace(" ", "").isalpha():
        messagebox.showerror("Error", "The search query must contain only letters!")
        return False
    return True

def check_entries():
    return (check_string_entry(query_entry) and check_string_entry(folder_name_entry) and check_image_number_entry() and check_chekbox_entry())
lunch_scrapping_setup_window(PATH)