from PIL import Image, ImageTk
from tkinter import Canvas, Tk, filedialog

import os
import traceback

from tkinter import messagebox


image_height = None
image_width = None


def process_image(filename):
    """
    Обработать файл изображения и вернуть объект PIL.ImageTk.PhotoImage.

Аргументы:
    filename (str): Путь к файлу изображения.

Возвращает:
    PIL.ImageTk.PhotoImage: Обработанное изображение.

Исключения:
    FileNotFoundError: Если файл изображения не существует.
    OSError: Если файл изображения не является допустимым файлом изображения.

    """
    global image_height, image_width
    # Check if the file exists
    if not os.path.isfile(filename):
        raise FileNotFoundError(f'File {filename} does not exist.')

    # Load the image
    try:
        with Image.open(filename) as img:
            img.load()
            print(
                f'Image size: {img.size}. '
                f'Format: {img.format}. Image type: {img.mode}'
            )
            # Определить ширину и высоту изображения
            image_width, image_height = img.size
            # Изменить размер изображения до размера окна
            img.thumbnail((image_width, image_height))
            # Сохранить как объект PIL.ImageTk.PhotoImage,
            # который является специфическим типом данных из библиотеки
            # Pillow (PIL),
            # используемый для хранения изображений, готовых к отображению
            # в графическом интерфейсе Tkinter.

            get_image = ImageTk.PhotoImage(img)
    except OSError as e:
        raise OSError(f'Error opening image file {filename}: {e}')

    return get_image  # Return the processed image


def choose_image_click():
    root = Tk()  # Создание корневого объкта - окна
    root.title('Выбор изображения')  # Устанавливаем заголовок окна
    # Открыть диалоговое окно для выбора файла
    filename = filedialog.askopenfilename()
    if filename:
        try:
            img = process_image(filename)  # Выполняем функцию
        except FileNotFoundError as e:
            messagebox.showerror("Файл не найден", str(e))
            return
        except OSError as e:
            messagebox.showerror("Ошибка чтения файла", str(e))
            return
        root.geometry(f'{img.width()}x{img.height()}')  # Установка размеров
        root.maxsize(1024, 768)  # Опционально установлен максимальный размер
        root.update_idletasks()
        canvas = Canvas(root, width=img.width(), height=img.height())
        canvas.pack()
        canvas.create_image(0, 0, anchor="nw", image=img)
    else:
        messagebox.showinfo("Выбор изображения", "Вы ничего не выбрали.")
    root.mainloop()


def main():
    try:
        choose_image_click()
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
