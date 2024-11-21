import json
import os
from tkinter import *
import requests
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter import messagebox as mb
import pyperclip


history_file = "upload_history.json"


def save_history(file_path, download_link):
    history = []
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            history = json.load(f)

    history.append({"file_path": os.path.basename(file_path), "download_link": download_link})

    with open(history_file, "w") as f:
        json.dump(history, f, indent=4)


def upload():
    try:
        filepath = fd.askopenfilename()
        if filepath:
            with open(filepath, 'rb') as f:
                files = {'file': f}
                response = requests.post('https://file.io', files=files)
                response.raise_for_status()  # Проверка на ошибки HTTP
                download_link = response.json().get('link')
                if download_link:
                    entry.delete(0, END)
                    entry.insert(0, download_link)
                    pyperclip.copy(download_link)  # Копирование ссылки в буфер обмена
                    save_history(filepath, download_link)
                    mb.showinfo("Ссылка скопирована", "Ссылка успешно скопирована в буфер обмена")

                else:
                    raise ValueError("Не удалось получить ссылку для скачивания")
    except ValueError as ve:
        mb.showerror("Ошибка", f"Произошла ошибка: {ve}")
    except Exception as e:
        mb.showerror("Ошибка", f"Произошла ошибка: {e}")


window = Tk()
window.title("Сохранение файлов в облаке")
window.geometry("400x200")

upload_button = ttk.Button(text="Загрузить файл", command=upload)
upload_button.pack()

entry = ttk.Entry()
entry.pack()

window.mainloop()
