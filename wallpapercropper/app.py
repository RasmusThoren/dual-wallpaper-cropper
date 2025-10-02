import tkinter as tk
from tkinter import filedialog, messagebox
from wallpapercropper.monitors import get_monitor_data, compute_physical_size_from_diag
from wallpapercropper.cropper import CropPreviewApp

def run_gui():
    # Step 1: Choose image
    root = tk.Tk()
    root.withdraw()
    image_path = filedialog.askopenfilename(
        parent=root,
        title="Select an image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp")]
    )
    root.destroy()
    if not image_path:
        return

    # Step 2: Get monitors
    monitors = get_monitor_data()
    if len(monitors) < 2:
        messagebox.showerror("Error", "❌ Two monitors are required.")
        return

    # Step 3: Ask for diagonal sizes
    diag_root = tk.Tk()
    diag_root.title("Enter Monitor Sizes")
    entries = {}

    def on_submit():
        nonlocal monitors
        monitors_with_size = []
        try:
            for m in monitors:
                name, w_px, h_px = m
                diag_inch = float(entries[name].get())
                w_mm, h_mm = compute_physical_size_from_diag(w_px, h_px, diag_inch)
                monitors_with_size.append((name, w_px, h_px, w_mm, h_mm))
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values.")
            return

        diag_root.destroy()
        monitors_sorted = sorted(monitors_with_size, key=lambda m: m[1], reverse=True)
        top_monitor, bottom_monitor = monitors_sorted[0], monitors_sorted[1]

        preview_root = tk.Tk()
        preview_root.title("Crop Preview")
        CropPreviewApp(preview_root, image_path, top_monitor, bottom_monitor)
        preview_root.mainloop()

    for m in monitors:
        name, w_px, h_px = m
        frame = tk.Frame(diag_root)
        frame.pack(pady=5)
        tk.Label(frame, text=f"{name} ({w_px}x{h_px}) diagonal size (inches):").pack(side="left")
        entry = tk.Entry(frame)
        entry.pack(side="left")
        entries[name] = entry

    tk.Button(diag_root, text="OK", command=on_submit).pack(pady=10)
    diag_root.mainloop()

if __name__ == "__main__":
    run_gui()
