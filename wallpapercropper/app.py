import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, StringVar, OptionMenu
from wallpapercropper.monitors import get_monitor_data, compute_physical_size_from_diag
from wallpapercropper.cropper import CropPreviewApp


def get_project_root():
    """Return the correct project root for both source and PyInstaller builds."""
    if getattr(sys, 'frozen', False):
        # Running inside PyInstaller build → use parent of dist/
        return os.path.abspath(os.path.join(os.path.dirname(sys.executable), ".."))
    else:
        # Running from source → repo root
        return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def run_gui():
    # Define input/output folders relative to project root
    project_root = get_project_root()
    input_dir = os.path.join(project_root, "input_images")
    output_dir = os.path.join(project_root, "output_images")

    # Ensure input/output directories exist
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Choose image (start in input_images/)
    root = tk.Tk()
    root.withdraw()
    image_path = filedialog.askopenfilename(
        parent=root,
        title="Select an image",
        initialdir=input_dir,
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp")]
    )
    root.destroy()
    if not image_path:
        return

    # Extract base filename for saving later
    base_name = os.path.splitext(os.path.basename(image_path))[0]

    # Step 2: Get monitors
    monitors = get_monitor_data()
    if len(monitors) < 2:
        messagebox.showerror("Error", "❌ Two monitors are required.")
        return

    # Step 3: Ask user for diagonal sizes + orientation
    diag_root = tk.Tk()
    diag_root.title("Enter Monitor Sizes & Orientation")
    entries = {}
    orientations = {}

    def on_submit():
        nonlocal monitors
        monitors_with_size = []
        try:
            for m in monitors:
                name, w_px, h_px = m
                diag_inch = float(entries[name].get())
                orientation = orientations[name].get()

                # Compute physical size
                w_mm, h_mm = compute_physical_size_from_diag(w_px, h_px, diag_inch)

                # If portrait, swap width/height
                if orientation == "Portrait":
                    w_px, h_px = h_px, w_px
                    w_mm, h_mm = h_mm, w_mm

                monitors_with_size.append((name, w_px, h_px, w_mm, h_mm, orientation))
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values.")
            return

        diag_root.destroy()
        monitors_sorted = sorted(monitors_with_size, key=lambda m: m[1], reverse=True)
        top_monitor, bottom_monitor = monitors_sorted[0], monitors_sorted[1]

        preview_root = tk.Tk()
        preview_root.title("Crop Preview")
        CropPreviewApp(preview_root, image_path, top_monitor, bottom_monitor, base_name, output_dir)
        preview_root.mainloop()

    for m in monitors:
        name, w_px, h_px = m
        frame = tk.Frame(diag_root)
        frame.pack(pady=5)

        # Diagonal entry
        tk.Label(frame, text=f"{name} ({w_px}x{h_px}) diagonal size (inches):").pack(side="left")
        entry = tk.Entry(frame, width=6)
        entry.pack(side="left", padx=5)
        entries[name] = entry

        # Orientation dropdown
        tk.Label(frame, text="Orientation:").pack(side="left")
        orientation_var = StringVar(value="Landscape")
        orientations[name] = orientation_var
        option_menu = OptionMenu(frame, orientation_var, "Landscape", "Portrait")
        option_menu.pack(side="left", padx=5)

    tk.Button(diag_root, text="OK", command=on_submit).pack(pady=10)
    diag_root.mainloop()


if __name__ == "__main__":
    run_gui()
