# Dual Wallpaper Cropper 🎨🖼️

**Dual Wallpaper Cropper** is a simple GUI tool for Linux (X11) that lets you crop a single image into perfectly aligned wallpapers for a dual-monitor layout.  
It ensures both monitors line up correctly by taking into account their **physical sizes** as well as their **resolutions**.

---

## ✨ Features
- T-shape (top + bottom)
- Side-by-side (left + right)
- Detects monitors automatically using `xrandr`
- Enter real diagonal sizes (inches) to account for DPI differences
- GUI preview of crop areas
- Move crop areas with **arrow keys**
- Separate crops for **top/left** and **bottom/right** monitor
- Saves wallpapers using original filename + monitor name  
  e.g. `sunset_HDMI-1.jpg`, `sunset_DP-1.jpg`
- Error handling with GUI dialogs

---

## 📂 File Organization

- Place your input wallpapers in:  
  ```
  input_images/
  ```

- Cropped wallpapers will be saved in:  
  ```
  output_images/
  ```

Example: if you load `input_images/sunset.jpg` and have monitors named `HDMI-1` and `DP-1`, the results will be:  
```
output_images/sunset_HDMI-1.jpg
output_images/sunset_DP-1.jpg
```

---

## 📥 Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/yourusername/dual-wallpaper-cropper.git
cd dual-wallpaper-cropper
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 🖥️ System Requirements

This tool requires **Tkinter** (for the GUI) and `xrandr` (for monitor detection).

On Linux (X11), install them with:

- **Debian/Ubuntu:**
  ```bash
  sudo apt install python3-tk x11-xserver-utils
  ```
- **Fedora:**
  ```bash
  sudo dnf install python3-tkinter xrandr
  ```
- **Arch Linux:**
  ```bash
  sudo pacman -S tk xorg-xrandr
  ```

---

## 🚀 Usage

Run the app directly:

```bash
python -m wallpapercropper.app
```

Steps:
1. Place your wallpaper image in `input_images/`  
2. Select it from the file dialog  
3. Enter the diagonal size (inches) for each monitor  
4. Choose layout (**T-shape** or **Side-by-side**)  
5. Adjust crop areas in the preview:  
   - Use the buttons to select **Top/Left** or **Bottom/Right** monitor  
   - Use the **arrow keys** to move the crop box  
6. Save wallpapers — they will appear in `output_images/`  

---

## 🛠️ Building Executable

You can build a standalone binary with **PyInstaller**:

```bash
chmod +x build.sh
./build.sh
```

The binary will be in `dist/dual-wallpaper-cropper` and can run on any Linux (X11) system without Python installed.

Run it with:

```bash
./dist/dual-wallpaper-cropper
```

---

## 📸 Screenshots

_(Add screenshots of your app here)_

- Main preview window:  
  ![Preview Screenshot](assets/preview.png)

- Cropped output example:  
  ![Result Screenshot](assets/result.png)

---

## 📜 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.