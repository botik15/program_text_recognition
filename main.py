
import os
import tkinter as tk
import webbrowser
from tkinter import filedialog, ttk
import cv2
import pytesseract
from PIL import Image
from tkinter import messagebox
from tkinter.ttk import Progressbar
from docx import Document


def clicked():
    messagebox.showinfo('Уведомление', 'Успешно!')


def start_processing():
    try:

        label.pack_forget()
        bar.pack()
        bar['value'] = 0
        image = filedialog.askopenfilename(
            filetypes=[("jpg", "*.jpg"), ("Text jpeg", "*.jpeg"), ("png", "*.png"), ("All files", "*.*")])
        image_url = image
        preprocess = "thresh"
        bar['value'] = 20

        # загрузить образ и преобразовать его в оттенки серого
        if image == '':
            pass

        else:
            image = cv2.imread(image)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            bar['value'] = 40
            # проверьте, следует ли применять пороговое значение для предварительной обработки изображения

            if preprocess == "thresh":
                gray = cv2.threshold(gray, 0, 255,
                                     cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

            # если нужно медианное размытие, чтобы удалить шум
            elif preprocess == "blur":
                gray = cv2.medianBlur(gray, 3)
            bar['value'] = 60
            # сохраним временную картинку в оттенках серого, чтобы можно было применить к ней OCR
            filename = "{}.png".format(os.getpid())
            cv2.imwrite(filename, gray)
            # загрузка изображения в виде объекта image Pillow, применение OCR, а затем удаление временного файла
            text = pytesseract.image_to_string(Image.open(filename), lang='rus')
            os.remove(filename)
            bar['value'] = 80
            print(text)
            image_url = str(image_url.split('/')[len(image_url.split('/')) - 1].split(".")[0]+'.txt')
            print(image_url)
            with open(image_url, "w") as file:
                file.write(text)

            bar['value'] = 100
            clicked()

            webbrowser.open(os.getcwd() + "/" + image_url)
        bar.pack_forget()
    except:
        label.pack(text='Ошибка')
        bar.pack_forget()


# создаем окно приложения
window = tk.Tk()
window.geometry('300x300+200+100')
window.title("Программа")
window.resizable(False, False)

bar = Progressbar(window, length=200)

label = tk.Label(window, text="bobbyhadz.com", height=3)
label.pack_forget()

# создаем кнопку "Начать" и привязываем к ней функцию начала обработки файла
start_button = tk.Button(window, text="Начать", command=start_processing)
start_button.pack()

# создаем кнопку "Начать" и привязываем к ней функцию начала обработки файла
starts_button = tk.Button(window, text="Выйти", command=window.destroy)
starts_button.pack()

# запускаем главный цикл обработки событий
window.mainloop()
