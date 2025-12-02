📦 Image Optimizer — Simple GUI Tool for Image Compression & Conversion

Image Optimizer is a lightweight and user-friendly Python utility with a graphical interface that allows you to quickly compress, optimize, and convert images without noticeable quality loss.

✨ Features
🔧 Image Optimization

Compress images while keeping visual quality

Remove EXIF metadata to reduce file size

Optional PNG palette optimization (adaptive palette)

📁 Batch Processing

Process a single file or an entire folder

Automatically preserves folder structure in output

🖼 Format Conversion (Optional)

Convert all images to JPEG with a checkbox toggle

Ensures maximum size reduction

Automatically handles PNG/WebP transparency → RGB

📥 Drag & Drop Support

Simply drag files or folders into the application window

👀 Image Preview

Shows a thumbnail preview of the selected file

📸 Supported Input Formats

JPEG / JPG

PNG

WEBP

Output format depends on the selected settings:

Original format, or

Forced JPEG (if the checkbox is enabled)

🚀 Installation
1. Install Python (3.9+ recommended)

Download from: https://www.python.org/downloads/

Make sure to check “Add to PATH” during installation.

2. Install required dependencies

Run this command in your terminal:

pip install pillow tkinterdnd2


(No installation needed for Tkinter — it comes with Python.)

▶️ How to Run

Navigate to the folder containing the script and run:

python image_optimizer.py


(Replace image_optimizer.py with your actual filename.)

The GUI window will open immediately.

🧰 How to Use

Choose an input file or folder

Choose an output directory

Adjust the quality slider (30–100)

(Optional) Enable:

Optimize PNG palette

Always save as JPEG

Click “Start Optimization”

The program will process all files and notify you when it’s finished.

📌 Notes

When “Save as JPEG” is enabled, all images will be converted to .jpg

PNG transparency will be removed when converting to JPEG (converted to RGB)

Optimization runs in a separate thread, so the UI remains responsive

📜 License

This project is released under the MIT License — free for personal and commercial use.
