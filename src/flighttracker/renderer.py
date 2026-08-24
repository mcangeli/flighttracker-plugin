from PIL import Image, ImageDraw, ImageFont

from bullpen.api import Layout, Color, PluginRenderer
from bullpen.util import center_text_position, scrolling_text
from bullpen.logging import LOGGER

from .config import Config
from .data import Data

class Renderer(PluginRenderer):
    def __init__(self, config, data):
        self.config = config
        self.data = data
        self.font_main = ImageFont.load_default()

    def render(self, canvas):
        flight = self.data.current_flight

        # If no aircraft is overhead and configured to hide, skip rendering
        if not flight:
            if self.config.hide_when_empty:
                return False
            # Render idle status
            draw = ImageDraw.Draw(canvas)
            draw.text((2, 12), "SKY CLEAR", fill=(80, 80, 80), font=self.font_main)
            return True

        image = Image.new("RGB", (64, 32), (0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Top Header: Aircraft Type & Callsign (Cyan & White)
        callsign = flight.get("callsign", "N/A")[:7]
        aircraft = flight.get("aircraft", "AIR")[:4]
        draw.text((2, 1), f"{callsign}", fill=(0, 255, 255), font=self.font_main)
        draw.text((42, 1), f"{aircraft}", fill=(180, 180, 180), font=self.font_main)

        # Middle Line: Route (Yellow)
        origin = flight.get("origin", "---")[:3]
        dest = flight.get("destination", "---")[:3]
        route_text = f"{origin} > {dest}"
        draw.text((2, 11), route_text, fill=(255, 215, 0), font=self.font_main)

        # Bottom Line: Altitude & Speed (Green)
        alt = flight.get("altitude", 0)
        alt_str = f"{alt // 1000}k" if isinstance(alt, (int, float)) and alt >= 1000 else f"{alt}"
        spd = flight.get("speed", 0)
        draw.text((2, 21), f"{alt_str}ft {spd}kt", fill=(0, 255, 100), font=self.font_main)

        # Heading indicator arrow / dot (Top right corner)
        draw.rectangle([58, 22, 60, 24], fill=(255, 140, 0))

        # Paste onto canvas
        canvas.SetImage(image, 0, 0)
        return True
