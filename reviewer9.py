from tkinter import *
from PIL import Image, ImageTk
import requests
import io
import os
import concurrent.futures



HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }

def review_images(image_urls, save_folder_path, subfolder_name):
    index = 0
    selected_flags = [False] * 9
    img_buttons = []

    images = preload_images(image_urls)


    def toggle_selection(i):
        selected_flags[i] = not selected_flags[i]
        frame, btn = img_buttons[i]
        if selected_flags[i]:
            frame.config(highlightbackground="red")
        else:
            frame.config(highlightbackground="white")


    def show_batch():
        nonlocal index, img_buttons
        for widget in grid_frame.winfo_children():
            widget.destroy()

        img_buttons = []
        selected_flags[:] = [False] * 9
        for i in range(3):
            for j in range(3):
                if index >= len(images):
                    break
                img = images[index]
                img = img.resize((cell_width, cell_height), Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                frame = Frame(grid_frame, highlightthickness=4, highlightbackground="white")
                frame.grid(row=i, column=j, padx=5, pady=5)
                btn = Button(
                                    frame,
                                    image=img_tk,
                                    borderwidth=0,
                                    command=lambda i=len(img_buttons): toggle_selection(i)
                                )
                btn.image = img_tk
                btn.pack()
                img_buttons.append((frame, btn))
                index += 1



    def next_batch():
        nonlocal index
        for i, selected in enumerate(selected_flags):
            img_index = index - 9 + i
            if selected and img_index < len(images):
                try:
                    image = images[img_index]
                    filename = os.path.join(folder_path, f"{img_index}.jpg")
                    image.save(filename, "JPEG")
                    print(f"Saved: {filename}")
                except Exception as e:
                    print(f"Failed to save image: {str(e)}")
        if index >= len(images):
            root.destroy()
        else:
            show_batch()

    root = Tk()

    screen_width = root.winfo_screenwidth() - 25
    screen_height = root.winfo_screenheight() - 50
    cell_width = (screen_width // 3) - 25
    cell_height = (screen_height // 3) - 50

    root.maxsize(screen_width, screen_height)
    root.title("Select images to save")
    grid_frame = Frame(root)
    grid_frame.pack()


    os.makedirs(save_folder_path, exist_ok=True)
    folder_path = os.path.join(save_folder_path,subfolder_name)
    i = 1
    while os.path.exists(folder_path):
        folder_path = os.path.join(save_folder_path,f"{subfolder_name}{i}")
        i += 1
    os.makedirs(folder_path , exist_ok=True)


    Button(root, text="Next", command=next_batch).pack(pady=10)
    root.bind("<space>", lambda event: next_batch())

    show_batch()
    root.mainloop()



def preload_images(image_urls):
    images_data = []

    def download_and_process(url):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            img = Image.open(io.BytesIO(response.content)).convert("RGB")
            return img
        except Exception as e:
            print(f"Failed to preload {url}: {str(e)}")
            return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(download_and_process, url) for url in image_urls]

        for future in concurrent.futures.as_completed(futures):
            img = future.result()
            if img is not None:
                images_data.append(img)

    return images_data