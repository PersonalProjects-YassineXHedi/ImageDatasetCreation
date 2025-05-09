import tkinter as tk

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
max_items_entry = tk.Entry(root, font=('calibre', 14), width=40)
max_items_entry.grid(row=1, column=1, padx=20, pady=15, sticky="w")


source_var_images = tk.IntVar()
source_var_shopping = tk.IntVar()

tk.Label(root, text="Scraping Source:", font=('calibre', 14, 'bold')).grid(row=2, column=0, padx=20, pady=10, sticky="e")

# Create a frame to hold both checkboxes side by side
checkbox_frame = tk.Frame(root)
checkbox_frame.grid(row=2, column=1, sticky="w", padx=20)

chk_images = tk.Checkbutton(checkbox_frame, text="Google Images", variable=source_var_images, font=('calibre', 14))
chk_images.pack(side="left", padx=10)

chk_shopping = tk.Checkbutton(checkbox_frame, text="Google Shopping", variable=source_var_shopping, font=('calibre', 14))
chk_shopping.pack(side="left", padx=10)

tk.Label(root).grid(row=3, column=0)

def start_scraping():
    return 

start_button = tk.Button(root, text="Start Scraping", font=('calibre', 14), width=20, command=start_scraping)
start_button.grid(row=4, column=1, pady=20, padx=20, sticky="e")

root.mainloop()
