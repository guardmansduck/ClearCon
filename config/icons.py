import os
from io import BytesIO
from PIL import Image, ImageTk
import cairosvg

class IconManager:
    """
    Loads and caches SVG icons from assets/icons/
    Converts them to PhotoImage objects usable in Tkinter/CTk.
    """

    def __init__(self, base_path="assets/icons", size=(24, 24), color_tint=None):
        self.base_path = base_path
        self.size = size
        self.color_tint = color_tint
        self._cache = {}

    def _svg_to_image(self, path):
        """
        Converts an SVG file to a Tk-compatible image using CairoSVG.
        """
        try:
            png_data = cairosvg.svg2png(url=path, output_width=self.size[0], output_height=self.size[1])
            img = Image.open(BytesIO(png_data))
            if self.color_tint:
                r, g, b = self.color_tint
                tint_img = Image.new("RGBA", img.size, (r, g, b, 0))
                img = Image.blend(img.convert("RGBA"), tint_img, 0.5)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"[IconManager] Failed to load icon {path}: {e}")
            return None

    def load(self, name: str):
        """
        Loads (and caches) an icon by name (without .svg)
        """
        if name in self._cache:
            return self._cache[name]

        path = os.path.join(self.base_path, f"{name}.svg")
        if not os.path.exists(path):
            print(f"[IconManager] Missing icon: {path}")
            return None

        img = self._svg_to_image(path)
        if img:
            self._cache[name] = img
        return img
