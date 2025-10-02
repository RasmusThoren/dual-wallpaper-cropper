import subprocess
import math


def get_monitor_data():
    """Get monitor info (name, width_px, height_px) using xrandr."""
    try:
        output = subprocess.check_output("xrandr --query", shell=True).decode()
    except Exception as e:
        raise RuntimeError("❌ Failed to run xrandr. Is it installed?") from e

    monitors = []
    for line in output.splitlines():
        if " connected" in line and ("+" in line or "*" in line):
            parts = line.split()
            name = parts[0]
            for part in parts:
                if "x" in part and "+" in part:
                    res = part.split("+")[0]
                    w, h = res.split("x")
                    monitors.append((name, int(w), int(h)))
                    break
    return monitors


def compute_physical_size_from_diag(w_px, h_px, diag_inch):
    """Compute width/height in millimeters from diagonal size (inches)."""
    aspect_ratio = w_px / h_px
    diag_mm = diag_inch * 25.4
    h_mm = diag_mm / ((aspect_ratio**2 + 1) ** 0.5)
    w_mm = aspect_ratio * h_mm
    return w_mm, h_mm
