import tkinter as tk
from PIL import Image, ImageTk
import requests
import io
import os
import concurrent.futures
import threading

HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }

def review_images(image_urls, save_folder_path, subfolder_name):
    index = 0
    img_tk = None

    images = preload_images(image_urls)

    def show_image():
        nonlocal index, img_tk
        if index >= len(images):
            print("Finished.")
            root.destroy()
            return

        try:
            image = images[index].resize((500, 400), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(image)
            label.config(image=img_tk)
            root.title(f"Image {index + 1}/{len(image_urls)}")                                                                  
        except Exception as e:
            print(f"Failed to show image: {str(e)}")
            next_image()

    def save_image():
        nonlocal index
        try:
            image = images[index]
            filename = os.path.join(save_folder_path,subfolder_name, f"{index}.jpg")
            image.save(filename, "JPEG")
            print(f"Saved: {filename}")
        except Exception as e:
            print(f"Failed to save image: {str(e)}")
        next_image()

    def skip_image():
        nonlocal index
        next_image()

    def next_image():
        nonlocal index
        index += 1
        show_image()

    root = tk.Tk()
    root.title("Image Review")

    label = tk.Label(root)
    label.pack()

    btn_frame = tk.Frame(root)
    btn_frame.pack()
    tk.Button(btn_frame, text="Save", command=save_image).pack(side="left", padx=10)
    tk.Button(btn_frame, text="Skip", command=skip_image).pack(side="right", padx=10)

    os.makedirs(save_folder_path, exist_ok=True)
    os.makedirs(save_folder_path +subfolder_name +'/' , exist_ok=True)

    show_image()
    root.mainloop()

    threading._shutdown()


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