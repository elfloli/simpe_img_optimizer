import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk


def optimize_image(input_path, output_path, quality, palette_optimize, force_jpg):
    try:
        img = Image.open(input_path)

        # Убираем EXIF
        data = list(img.getdata())
        img_no_exif = Image.new(img.mode, img.size)
        img_no_exif.putdata(data)

        # Принудительное сохранение в JPEG
        if force_jpg:
            if img_no_exif.mode in ("RGBA", "P"):
                img_no_exif = img_no_exif.convert("RGB")

            save_path = os.path.splitext(output_path)[0] + ".jpg"

            img_no_exif.save(
                save_path,
                format="JPEG",
                quality=quality,
                optimize=True,
                progressive=True
            )
            return

        # -------- Сохранение в оригинальном формате --------
        ext = img.format
        params = {}

        if ext == "JPEG":
            params.update({"optimize": True, "progressive": True, "quality": quality})

        elif ext == "PNG":
            if palette_optimize:
                img_no_exif = img_no_exif.convert("P", palette=Image.ADAPTIVE)
            params.update({"optimize": True})

        else:  # WebP или другие
            params.update({"quality": quality, "method": 6})

        img_no_exif.save(output_path, **params)

    except Exception as e:
        print(f"Ошибка файла {input_path}: {e}")


def process_folder(input_folder, output_folder, quality, palette_optimize, force_jpg):
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                in_path = os.path.join(root, file)
                rel_path = os.path.relpath(root, input_folder)
                out_dir = os.path.join(output_folder, rel_path)
                os.makedirs(out_dir, exist_ok=True)

                if force_jpg:
                    out_file = os.path.splitext(file)[0] + ".jpg"
                else:
                    out_file = file

                out_path = os.path.join(out_dir, out_file)

                optimize_image(in_path, out_path, quality, palette_optimize, force_jpg)


# --- GUI ---
root = TkinterDnD.Tk()
root.title("Image Optimizer")
root.geometry("600x600")

input_path = tk.StringVar()
output_path = tk.StringVar()
quality_var = tk.IntVar(value=85)
palette_var = tk.BooleanVar(value=True)
force_jpg_var = tk.BooleanVar(value=False)   # <<< чекбокс JPG

preview_label = tk.Label(root, text="Предпросмотр не загружен")
preview_label.pack(pady=10)


def update_preview(path):
    try:
        img = Image.open(path)
        img.thumbnail((250, 250))
        img_tk = ImageTk.PhotoImage(img)
        preview_label.config(image=img_tk)
        preview_label.image = img_tk
    except:
        preview_label.config(text="Нет предпросмотра")


def select_input():
    path = filedialog.askopenfilename() or filedialog.askdirectory()
    if path:
        input_path.set(path)
        if os.path.isfile(path):
            update_preview(path)


def select_output():
    path = filedialog.askdirectory()
    if path:
        output_path.set(path)


def run_optimization():
    inp = input_path.get()
    out = output_path.get()
    quality = quality_var.get()
    palette = palette_var.get()
    force_jpg = force_jpg_var.get()

    if not inp:
        messagebox.showerror("Ошибка", "Выберите файл или папку")
        return
    if not out:
        messagebox.showerror("Ошибка", "Выберите путь сохранения")
        return

    def task():
        if os.path.isfile(inp):
            name = os.path.basename(inp)

            if force_jpg:
                name = os.path.splitext(name)[0] + ".jpg"

            out_file = os.path.join(out, name)

            optimize_image(inp, out_file, quality, palette, force_jpg)
        else:
            process_folder(inp, out, quality, palette, force_jpg)

        messagebox.showinfo("Готово", "Оптимизация завершена!")

    threading.Thread(target=task).start()


# --- Drag & Drop ---
def drop_handler(event):
    path = event.data.strip("{}").replace("\\", "/")
    input_path.set(path)
    if os.path.isfile(path):
        update_preview(path)

root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drop_handler)


# --- UI Layout ---
tk.Label(root, text="Файл/Папка для оптимизации:").pack(anchor="w", padx=10)
tk.Entry(root, textvariable=input_path, width=70).pack(padx=10)
tk.Button(root, text="Выбрать", command=select_input).pack(pady=5)

tk.Label(root, text="Папка для сохранения:").pack(anchor="w", padx=10)
tk.Entry(root, textvariable=output_path, width=70).pack(padx=10)
tk.Button(root, text="Выбрать", command=select_output).pack(pady=5)

# Ползунок качества
tk.Label(root, text="Качество JPEG/WebP:").pack(anchor="w", padx=10)
tk.Scale(root, from_=30, to=100, orient="horizontal", variable=quality_var).pack(fill="x", padx=10)

# PNG палитра
tk.Checkbutton(root, text="Оптимизировать палитру PNG", variable=palette_var).pack(pady=5)

# NEW: чекбокс JPEG
tk.Checkbutton(root, text="Всегда сохранять в JPEG", variable=force_jpg_var).pack(pady=5)

# Старт
tk.Button(root, text="Начать оптимизацию", command=run_optimization, bg="#4CAF50", fg="white", height=2).pack(pady=20)

root.mainloop()
