#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Image Optimizer — Fluent Full Dark Theme Edition
elfloli special build
"""

import os
import traceback
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import winreg
import ctypes


# =====================================================================
#                      FORCE DARK TITLEBAR
# =====================================================================
def force_dark_titlebar(window):
    try:
        HWND = ctypes.windll.user32.GetParent(window.winfo_id())
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        value = ctypes.c_int(1)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            HWND,
            DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(value),
            ctypes.sizeof(value)
        )
    except:
        pass


# =====================================================================
#                      DETECT WINDOWS THEME
# =====================================================================
def detect_windows_dark_mode() -> bool:
    try:
        reg = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        )
        value, _ = winreg.QueryValueEx(reg, "AppsUseLightTheme")
        winreg.CloseKey(reg)
        return value == 0
    except Exception:
        return False


# =====================================================================
#                  FLUENT FULL DARK STYLE FOR TTK
# =====================================================================
def apply_fluent_style(root: tk.Tk):
    DARK = {
        "bg": "#111111",
        "panel": "#181818",
        "panel_alt": "#202020",
        "text": "#E0E0E0",
        "muted": "#A0A0A0",
        "btn": "#1F1F1F",
        "btn_hover": "#2A2A2A",
        "accent": "#3A8DFF",
        "entry_bg": "#161616",
        "border": "#2A2A2A",
        "pg_bg": "#1A1A1A",
        "pg_fg": "#3A8DFF"
    }

    LIGHT = {
        "bg": "#F3F4F6",
        "panel": "#FFFFFF",
        "panel_alt": "#FAFAFB",
        "text": "#111827",
        "muted": "#374151",
        "btn": "#E6E7E9",
        "btn_hover": "#DCDDE0",
        "accent": "#2563EB",
        "entry_bg": "#FFFFFF",
        "border": "#D1D5DB",
        "pg_bg": "#E5E7EB",
        "pg_fg": "#2563EB"
    }

    pal = DARK if detect_windows_dark_mode() else LIGHT

    style = ttk.Style()
    style.theme_use("clam")

    # Global
    root.configure(bg=pal["bg"])
    style.configure(".", background=pal["bg"], foreground=pal["text"])

    # Frame
    style.configure("TFrame", background=pal["panel"])
    style.configure("TLabelframe", background=pal["panel"])
    style.configure("TLabelframe.Label", background=pal["panel"], foreground=pal["text"])

    # Label
    style.configure("TLabel", background=pal["bg"], foreground=pal["text"])

    # Buttons
    style.configure(
        "TButton",
        background=pal["btn"],
        foreground=pal["text"],
        bordercolor=pal["border"],
        focusthickness=2,
        focuscolor=pal["accent"]
    )
    style.map(
        "TButton",
        background=[("active", pal["btn_hover"])],
        foreground=[("active", pal["text"])]
    )

    # Entry
    style.configure(
        "TEntry",
        fieldbackground=pal["entry_bg"],
        background=pal["entry_bg"],
        foreground=pal["text"],
        bordercolor=pal["border"]
    )

    # Checkbutton
    style.configure(
        "TCheckbutton",
        background=pal["bg"],
        foreground=pal["text"],
    )
    style.map(
        "TCheckbutton",
        background=[("active", pal["panel"])],
        foreground=[("active", pal["text"])]
    )

    # Scale
    style.configure(
        "Horizontal.TScale",
        background=pal["panel"],
        troughcolor=pal["border"],
        sliderrelief="flat",
        slidercolor=pal["accent"]
    )

    # Progressbar
    style.configure(
        "TProgressbar",
        background=pal["pg_fg"],
        troughcolor=pal["pg_bg"],
        bordercolor=pal["border"],
        lightcolor=pal["pg_fg"],
        darkcolor=pal["pg_fg"]
    )

    return pal


# =====================================================================
#                     IMAGE OPTIMIZATION
# =====================================================================
def optimize_image(input_path, output_path, quality, palette_optimize, force_jpg):
    try:
        img = Image.open(input_path)

        # Remove EXIF
        data = list(img.getdata())
        img_no_exif = Image.new(img.mode, img.size)
        img_no_exif.putdata(data)

        if force_jpg:
            if img_no_exif.mode in ("RGBA", "P"):
                img_no_exif = img_no_exif.convert("RGB")
            output_path = os.path.splitext(output_path)[0] + ".jpg"
            img_no_exif.save(output_path, "JPEG", quality=quality, optimize=True, progressive=True)
            return True, output_path

        ext = (img.format or "").upper()

        if ext in ("JPG", "JPEG", "JFIF"):
            img_no_exif.save(output_path, "JPEG", quality=quality, optimize=True, progressive=True)
            return True, output_path

        elif ext == "PNG":
            if palette_optimize:
                img_no_exif = img_no_exif.convert("P", palette=Image.ADAPTIVE)
            img_no_exif.save(output_path, optimize=True)
            return True, output_path

        elif ext == "WEBP":
            img_no_exif.save(output_path, "WEBP", quality=quality, method=6)
            return True, output_path

        img_no_exif.save(output_path)
        return True, output_path

    except Exception as e:
        traceback.print_exc()
        return False, str(e)


def count_images(folder):
    total = 0
    for _, _, files in os.walk(folder):
        for f in files:
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                total += 1
    return total


def process_folder(folder, out, quality, palette_opt, force_jpg, progress_cb):
    total = count_images(folder)
    processed = 0

    for root, _, files in os.walk(folder):
        for f in files:
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                inp = os.path.join(root, f)
                rel = os.path.relpath(root, folder)
                dst = os.path.join(out, rel)
                os.makedirs(dst, exist_ok=True)

                out_file = os.path.splitext(f)[0] + (".jpg" if force_jpg else os.path.splitext(f)[1])
                out_path = os.path.join(dst, out_file)

                optimize_image(inp, out_path, quality, palette_opt, force_jpg)

                processed += 1
                progress_cb(processed, total, inp)


# =====================================================================
#                               GUI APP
# =====================================================================
class ImageOptimizerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Image Optimizer — Fluent Dark")
        root.geometry("660x680")

        force_dark_titlebar(root)

        self.palette = apply_fluent_style(root)

        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.quality = tk.IntVar(value=85)
        self.png_palette = tk.BooleanVar(value=True)
        self.force_jpg = tk.BooleanVar(value=False)
        self.progress = tk.DoubleVar()

        self.preview_image = None
        self.preview_size = (420, 300)

        self.build_ui()

        root.drop_target_register(DND_FILES)
        root.dnd_bind("<<Drop>>", self.on_drop)

    # ============================ UI BUILD ============================
    def build_ui(self):
        p = {"padx": 12, "pady": 6}

        # Input
        top = ttk.Frame(self.root, style="TFrame")
        top.pack(fill="x", **p)

        ttk.Label(top, text="File / Folder:").pack(anchor="w")

        row = ttk.Frame(top, style="TFrame")
        row.pack(fill="x")

        ttk.Entry(row, textvariable=self.input_path, width=58).pack(side="left", fill="x", expand=True)

        ttk.Button(row, text="File", command=self.choose_file).pack(side="left", padx=6)
        ttk.Button(row, text="Folder", command=self.choose_folder).pack(side="left")

        # Output
        ttk.Label(self.root, text="Save to folder:").pack(anchor="w", padx=12)
        out_row = ttk.Frame(self.root, style="TFrame")
        out_row.pack(fill="x", **p)
        ttk.Entry(out_row, textvariable=self.output_path, width=58).pack(side="left", fill="x", expand=True)
        ttk.Button(out_row, text="Choose", command=self.choose_output).pack(side="left", padx=6)

        # Preview
        mid = ttk.Frame(self.root, style="TFrame")
        mid.pack(fill="x", **p)

        ttk.Label(mid, text="Preview").grid(row=0, column=0, sticky="w")

        self.preview_box = tk.Label(
            mid,
            width=self.preview_size[0],
            height=self.preview_size[1],
            bg=self.palette["panel"],
            anchor="center"
        )
        self.preview_box.grid(row=1, column=0, padx=6, pady=6)

        # Options
        opts = ttk.Frame(mid, style="TFrame")
        opts.grid(row=1, column=1, sticky="n", padx=12)

        ttk.Label(opts, text="Quality:").pack(anchor="w")
        ttk.Scale(opts, from_=30, to=100, orient="horizontal", variable=self.quality, length=200).pack(anchor="w", pady=6)

        ttk.Checkbutton(opts, text="Optimize PNG palette", variable=self.png_palette).pack(anchor="w", pady=4)
        ttk.Checkbutton(opts, text="Always save as JPG", variable=self.force_jpg).pack(anchor="w", pady=4)

        ttk.Button(opts, text="Preview", command=self.show_preview).pack(side="left", pady=10, padx=4)
        ttk.Button(opts, text="Start", command=self.start).pack(side="left", pady=10)

        # Progress
        bottom = ttk.Frame(self.root, style="TFrame")
        bottom.pack(fill="x", **p)

        self.progressbar = ttk.Progressbar(bottom, maximum=100, variable=self.progress)
        self.progressbar.pack(fill="x")

        self.progress_label = ttk.Label(bottom, text="Progress: 0%")
        self.progress_label.pack(anchor="w")

        self.status_label = ttk.Label(self.root, text="")
        self.status_label.pack(anchor="w", padx=14)

    # =========================== ACTIONS =============================
    def choose_file(self):
        p = filedialog.askopenfilename(filetypes=[("Images", "*.jpg;*.jpeg;*.png;*.webp")])
        if p:
            self.input_path.set(p)
            self.update_preview(p)

    def choose_folder(self):
        p = filedialog.askdirectory()
        if p:
            self.input_path.set(p)
            self.preview_box.config(image="", text="Folder selected")

    def choose_output(self):
        p = filedialog.askdirectory()
        if p:
            self.output_path.set(p)

    def on_drop(self, e):
        path = e.data.strip("{}")
        self.input_path.set(path)
        if os.path.isfile(path):
            self.update_preview(path)
        else:
            self.preview_box.config(image="", text="Folder dropped")

    def update_preview(self, path):
        try:
            img = Image.open(path)
            img.thumbnail(self.preview_size)
            self.preview_image = ImageTk.PhotoImage(img)
            self.preview_box.config(image=self.preview_image, text="")
        except:
            self.preview_box.config(image="", text="Cannot preview")

    def show_preview(self):
        path = self.input_path.get()
        if os.path.isfile(path):
            self.update_preview(path)
        else:
            messagebox.showinfo("Preview", "Select a file first.")

    # ========================== PROCESSING ===========================
    def start(self):
        inp = self.input_path.get()
        out = self.output_path.get()

        if not inp:
            messagebox.showerror("Error", "Choose input first")
            return
        if not out:
            messagebox.showerror("Error", "Choose output folder")
            return

        self.progress.set(0)
        self.progress_label.config(text="Progress: 0%")

        q = self.quality.get()
        pal = self.png_palette.get()
        fj = self.force_jpg.get()

        def update(done, total, fn):
            pct = int((done / total) * 100) if total else 100
            self.root.after(0, lambda: self.update_progress(pct, done, total, fn))

        def worker():
            try:
                if os.path.isfile(inp):
                    name = os.path.basename(inp)
                    out_file = os.path.splitext(name)[0] + (".jpg" if fj else os.path.splitext(name)[1])
                    optimize_image(inp, os.path.join(out, out_file), q, pal, fj)
                    update(1, 1, inp)
                else:
                    process_folder(inp, out, q, pal, fj, update)

                self.root.after(0, lambda: messagebox.showinfo("Done", "Optimization completed"))
            except Exception as e:
                traceback.print_exc()
                self.root.after(0, lambda: messagebox.showerror("Error", str(e)))

        threading.Thread(target=worker, daemon=True).start()

    def update_progress(self, pct, done, total, fn):
        self.progress.set(pct)
        self.progress_label.config(text=f"Progress: {pct}%  ({done}/{total})")
        self.status_label.config(text=os.path.basename(fn) if fn else "")


# =====================================================================
#                               RUN
# =====================================================================
def main():
    root = TkinterDnD.Tk()
    ImageOptimizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
