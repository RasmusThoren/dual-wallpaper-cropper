import subprocess, re, math

def get_monitor_data():
    """
    Fetch monitor data using xrandr --verbose.
    Returns list of (name, width_px, height_px).
    """
    result = subprocess.run(["xrandr", "--verbose"], capture_output=True, text=True)
    lines = result.stdout.splitlines()

    monitors = []
    current_name = None
    for line in lines:
        if " connected" in line:
            current_name = line.split()[0]
        elif "preferred" in line and current_name:
            match_res = re.search(r"(\d+)x(\d+)", line)
            if match_res:
                w_px, h_px = int(match_res.group(1)), int(match_res.group(2))
                monitors.append((current_name, w_px, h_px))
                current_name = None
    return monitors

def compute_physical_size_from_diag(width_px, height_px, diag_inch):
    """Compute physical width/height in mm from resolution and diagonal size."""
    diag_px = math.sqrt(width_px**2 + height_px**2)
    mm_per_px = (diag_inch * 25.4) / diag_px
    width_mm = width_px * mm_per_px
    height_mm = height_px * mm_per_px
    return width_mm, height_mm
