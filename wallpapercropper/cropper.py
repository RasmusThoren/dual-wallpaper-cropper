import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox


class CropPreviewApp:
    def __init__(self, root, image_path, top_monitor, bottom_monitor, base_name, output_dir):
        self.root = root
        self.img = Image.open(image_path)
        self.base_name = base_name
        self.output_dir = output_dir

        self.top_monitor = top_monitor
        self.bottom_monitor = bottom_monitor

        # Extract monitor data
        top_name, top_w_px, top_h_px, top_w_mm, top_h_mm = top_monitor
        bottom_name, bottom_w_px, bottom_h_px, bottom_w_mm, bottom_h_mm = bottom_monitor

        # Scale to match physical size
        top_ppmm = top_w_px / top_w_mm
        bottom_ppmm = bottom_w_px / bottom_w_mm
        scale_factor = bottom_ppmm / top_ppmm

        self.top_w = int(top_w_px * scale_factor)
        self.top_h = int(top_h_px * scale_factor)
        self.bottom_w = bottom_w_px
        self.bottom_h = bottom_h_px

        # Scale image for preview
        self.preview_max_w, self.preview_max_h = 1600, 900
        self.scale = min(self.preview_max_w / self.img.width,
                         self.preview_max_h / self.img.height, 1.0)
        preview_size = (int(self.img.width * self.scale), int(self.img.height * self.scale))
        self.preview_img = self.img.resize(preview_size, Image.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(self.preview_img, master=root)

        self.canvas = tk.Canvas(root, width=preview_size[0], height=preview_size[1])
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)

        # Default crop positions
        self._init_crops(preview_size)
        self.selected_rect = None
        self._create_controls(root)

    def _init_crops(self, preview_size):
        """Initialize default crop rectangles."""
        self.bottom_y2 = preview_size[1]
        self.bottom_y1 = self.bottom_y2 - int(self.bottom_h * self.scale)
        self.bottom_x1 = (preview_size[0] - int(self.bottom_w * self.scale)) // 2
        self.bottom_x2 = self.bottom_x1 + int(self.bottom_w * self.scale)

        self.top_y2 = preview_size[1] - int(self.bottom_h * self.scale)
        self.top_y1 = self.top_y2 - int(self.top_h * self.scale)
        self.top_x1 = (preview_size[0] - int(self.top_w * self.scale)) // 2
        self.top_x2 = self.top_x1 + int(self.top_w * self.scale)

        # Rectangles
        self.top_rect = self.canvas.create_rectangle(
            self.top_x1, self.top_y1, self.top_x2, self.top_y2, outline="red", width=3
        )
        self.bottom_rect = self.canvas.create_rectangle(
            self.bottom_x1, self.bottom_y1, self.bottom_x2, self.bottom_y2, outline="blue", width=3
        )

    def _create_controls(self, root):
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Select Top", command=lambda: self.select_rect(self.top_rect)).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Select Bottom", command=lambda: self.select_rect(self.bottom_rect)).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Crop & Save", command=self.crop_and_save).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cancel", command=root.quit).pack(side="left", padx=10)

        self.info_label = tk.Label(root, text="Select Top/Bottom, then use arrow keys to move")
        self.info_label.pack(pady=5)

        self.move_step = 10
        root.bind("<Left>", lambda e: self.move_selected(-self.move_step, 0))
        root.bind("<Right>", lambda e: self.move_selected(self.move_step, 0))
        root.bind("<Up>", lambda e: self.move_selected(0, -self.move_step))
        root.bind("<Down>", lambda e: self.move_selected(0, self.move_step))

    def select_rect(self, rect_id):
        self.selected_rect = rect_id
        self.canvas.itemconfig(self.top_rect, width=3)
        self.canvas.itemconfig(self.bottom_rect, width=3)
        self.canvas.itemconfig(rect_id, width=5)
        msg = "Top monitor selected" if rect_id == self.top_rect else "Bottom monitor selected"
        self.info_label.config(text=f"{msg} — use arrow keys to move")

    def move_selected(self, dx, dy):
        if self.selected_rect:
            self.canvas.move(self.selected_rect, dx, dy)
        else:
            self.info_label.config(text="⚠️ Select a monitor first!")

    def crop_and_save(self):
        top_coords = [int(x / self.scale) for x in self.canvas.coords(self.top_rect)]
        bottom_coords = [int(x / self.scale) for x in self.canvas.coords(self.bottom_rect)]

        img_w, img_h = self.img.size
        if (top_coords[2] > img_w or top_coords[3] > img_h or
            bottom_coords[2] > img_w or bottom_coords[3] > img_h):
            messagebox.showerror("Image Too Small",
                                 f"Image {img_w}x{img_h} is too small for the required crops.")
            return

        # Use monitor names for filenames
        top_name = self.top_monitor[0]
        bottom_name = self.bottom_m
