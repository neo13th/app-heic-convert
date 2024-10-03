import os
from tkinter import Tk, Label, Button, filedialog, StringVar, OptionMenu
from tkinter import messagebox
from PIL import Image
import pillow_heif

# Реєстрація підтримки HEIF формату у Pillow
pillow_heif.register_heif_opener()

# Функція для конвертації HEIC у бажаний формат
def convert_heic_to(image_path, output_folder, output_format):
    image = Image.open(image_path)
    output_file = os.path.join(output_folder, os.path.splitext(os.path.basename(image_path))[0] + f'.{output_format}')
    image.save(output_file, output_format.upper())
    return output_file

# Вибір вхідної папки з HEIC файлами
def select_input_folder():
    folder = filedialog.askdirectory()
    if folder:
        input_folder.set(folder)

# Вибір папки для збереження результату
def select_output_folder():
    folder = filedialog.askdirectory()
    if folder:
        output_folder.set(folder)

# Виконання конвертації
def convert_files():
    in_folder = input_folder.get()
    out_folder = output_folder.get()
    format_choice = output_format.get()

    if not in_folder or not out_folder:
        messagebox.showerror("Помилка", "Оберіть папки для входу та виходу.")
        return

    heic_files = [f for f in os.listdir(in_folder) if f.lower().endswith('.heic')]
    if not heic_files:
        messagebox.showerror("Помилка", "У вибраній папці немає HEIC файлів.")
        return

    for file in heic_files:
        input_file_path = os.path.join(in_folder, file)
        try:
            converted_file = convert_heic_to(input_file_path, out_folder, format_choice)
            print(f"Конвертовано: {converted_file}")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося конвертувати файл {file}: {e}")

    messagebox.showinfo("Успіх", "Конвертація завершена!")

# Створення головного вікна
root = Tk()
root.title("Конвертер HEIC файлів")

# Створення змінних для зберігання шляху до папок і вибору формату
input_folder = StringVar()
output_folder = StringVar()
output_format = StringVar(value="jpg")

# Інтерфейс вибору папок та налаштувань
Label(root, text="Виберіть папку з HEIC файлами:").grid(row=0, column=0, padx=10, pady=10)
Button(root, text="Обрати папку", command=select_input_folder).grid(row=0, column=1, padx=10, pady=10)

Label(root, text="Виберіть папку для збереження:").grid(row=1, column=0, padx=10, pady=10)
Button(root, text="Обрати папку", command=select_output_folder).grid(row=1, column=1, padx=10, pady=10)

Label(root, text="Оберіть формат для збереження:").grid(row=2, column=0, padx=10, pady=10)
OptionMenu(root, output_format, "jpg", "png", "tiff").grid(row=2, column=1, padx=10, pady=10)

# Кнопка для запуску конвертації
Button(root, text="Конвертувати", command=convert_files).grid(row=3, column=0, columnspan=2, pady=20)

# Запуск головного циклу Tkinter
root.mainloop()
