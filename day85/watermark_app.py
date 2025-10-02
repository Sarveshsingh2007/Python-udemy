import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

# ---------- GLOBAL VARIABLES ----------
original_image = None
watermarked_image = None

# ---------- FUNCTIONS ----------

def upload_image():
    global original_image, watermarked_image
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")]
    )
    if file_path:
        original_image = Image.open(file_path).convert("RGBA")
        watermarked_image = original_image.copy()
        display_image(original_image)
        add_watermark_button.pack(pady=10)

def display_image(img):
    img_resized = img.copy()
    img_resized.thumbnail((400, 400))
    img_tk = ImageTk.PhotoImage(img_resized)
    image_label.config(image=img_tk)
    image_label.image = img_tk

def add_watermark():
    global watermarked_image

    if original_image is None:
        messagebox.showerror("Error", "Please upload an image first!")
        return

    text = watermark_entry.get()
    if not text.strip():
        messagebox.showerror("Error", "Please enter watermark text!")
        return

    position = position_var.get()
    watermarked_image = original_image.copy()
    draw = ImageDraw.Draw(watermarked_image)

    font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

    width, height = watermarked_image.size
    margin = 10

    if position == "top-left":
        x, y = margin, margin
    elif position == "top-right":
        x, y = width - text_width - margin, margin
    elif position == "bottom-left":
        x, y = margin, height - text_height - margin
    elif position == "bottom-right":
        x, y = width - text_width - margin, height - text_height - margin
    else:
        x, y = (width - text_width) // 2, (height - text_height) // 2

    draw.text((x, y), text, fill=(255, 0, 0, 255), font=font)
    display_image(watermarked_image)

    save_button.pack(pady=15)
    root.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

def save_image():
    if watermarked_image is None:
        messagebox.showerror("Error", "Please add a watermark first!")
        return

    save_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")]
    )
    if save_path:
        watermarked_image.save(save_path)
        messagebox.showinfo("Success", f"Image saved as {os.path.basename(save_path)}")

# ---------- UI ----------

root = tk.Tk()
root.title("Image Watermarking App")

# ✅ Make full screen width and 90% height
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
window_w = screen_w
window_h = int(screen_h * 0.9)
root.geometry(f"{window_w}x{window_h}")
root.resizable(True, True)

# ✅ Create canvas + scrollbar
canvas = tk.Canvas(root, highlightthickness=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

# ✅ Place content in center using anchor="n" and window width
canvas_window = canvas.create_window((screen_w // 2, 0), window=scrollable_frame, anchor="n")
canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# ---------- MAIN CONTENT (Centered) ----------
title_label = tk.Label(scrollable_frame, text="🖼️ Image Watermarking App", font=("Arial", 24, "bold"))
title_label.pack(pady=20)

upload_button = tk.Button(scrollable_frame, text="📂 Upload Image", command=upload_image, bg="#007BFF", fg="white", font=("Arial", 14, "bold"), width=25)
upload_button.pack(pady=10)

image_label = tk.Label(scrollable_frame)
image_label.pack(pady=20)

watermark_label = tk.Label(scrollable_frame, text="Watermark Text:", font=("Arial", 14))
watermark_label.pack()
watermark_entry = tk.Entry(scrollable_frame, width=40, font=("Arial", 14))
watermark_entry.pack(pady=5)

position_label = tk.Label(scrollable_frame, text="Position:", font=("Arial", 14))
position_label.pack()

position_var = tk.StringVar(value="bottom-right")
position_menu = tk.OptionMenu(scrollable_frame, position_var, "top-left", "top-right", "bottom-left", "bottom-right", "center")
position_menu.config(font=("Arial", 13))
position_menu.pack(pady=5)

add_watermark_button = tk.Button(scrollable_frame, text="✨ Add Watermark", command=add_watermark, bg="green", fg="white", font=("Arial", 14, "bold"), width=25)
add_watermark_button.pack_forget()

save_button = tk.Button(scrollable_frame, text="💾 Save Image", command=save_image, bg="red", fg="white", font=("Arial", 14, "bold"), width=25)
save_button.pack_forget()

root.mainloop()