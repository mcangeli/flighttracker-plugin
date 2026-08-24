import bullpen.api as api

class Config(api.PluginConfig):
    def __init__(self, top_level_config, plugin_config):
        self.top_level = top_level_config
        self.plugin_config = plugin_config or {}

        # Observer coordinates & detection radius
        self.latitude = float(self.plugin_config.get("latitude", 33.7490))
        self.longitude = float(self.plugin_config.get("longitude", -84.3880))
        self.radius_km = float(self.plugin_config.get("radius_km", 15.0))

        # Data source settings ("flightradar24" or "local_adsb")
        self.source = self.plugin_config.get("source", "flightradar24")
        self.local_url = self.plugin_config.get("local_adsb_url", "http://localhost:8080/data/aircraft.json")

        # Display preferences
        self.units = self.plugin_config.get("units", "imperial")  # 'imperial' (ft/mph) or 'metric' (m/kmh)
        self.display_duration = int(self.plugin_config.get("display_duration", 15))
        self.hide_when_empty = bool(self.plugin_config.get("hide_when_empty", True))
