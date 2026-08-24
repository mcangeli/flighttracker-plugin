import bullpen.api as api

import math
import requests
import time


class Data:
    def __init__(self, config):
        self.config = config
        self.current_flight = None
        self.last_update = 0

    def _calculate_bounding_box(self, lat, lon, radius_km):
        # 1 deg lat ~ 111 km, 1 deg lon ~ 111 km * cos(lat)
        lat_delta = radius_km / 111.0
        lon_delta = radius_km / (111.0 * math.cos(math.radians(lat)))
        return {
            "lat_max": lat + lat_delta,
            "lat_min": lat - lat_delta,
            "lon_max": lon + lon_delta,
            "lon_min": lon - lon_delta,
        }

    def _fetch_from_fr24(self):
        bounds = self._calculate_bounding_box(
            self.config.latitude, self.config.longitude, self.config.radius_km
        )
        url = (
            f"https://data-cloud.flightradar24.com/zones/fcgi/feed.js?"
            f"bounds={bounds['lat_max']:.3f},{bounds['lat_min']:.3f},"
            f"{bounds['lon_min']:.3f},{bounds['lon_max']:.3f}&"
            f"faa=1&satellite=1&mlat=1&flarm=1&adsb=1&gnd=0&air=1&vehicles=0&estimated=1"
        )
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        try:
            resp = requests.get(url, headers=headers, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                flights = []
                for k, v in data.items():
                    if isinstance(v, list) and len(v) >= 14:
                        # FlightRadar24 feed array mapping
                        flights.append({
                            "callsign": v[16] if len(v) > 16 and v[16] else v[13],
                            "aircraft": v[8] or "UNK",
                            "origin": v[11] or "---",
                            "destination": v[12] or "---",
                            "altitude": v[4],  # feet
                            "speed": v[5],     # knots
                            "heading": v[3],   # degrees
                            "lat": v[1],
                            "lon": v[2],
                        })
                return flights
        except Exception:
            pass
        return []

    def _fetch_from_local_adsb(self):
        try:
            resp = requests.get(self.config.local_url, timeout=3)
            if resp.status_code == 200:
                data = resp.json()
                aircraft_list = data.get("aircraft", [])
                flights = []
                for ac in aircraft_list:
                    if "lat" in ac and "lon" in ac:
                        flights.append({
                            "callsign": ac.get("flight", "UNK").strip(),
                            "aircraft": ac.get("t", "UNK"),
                            "origin": "---",
                            "destination": "---",
                            "altitude": ac.get("alt_geom", ac.get("alt_baro", 0)),
                            "speed": ac.get("gs", 0),
                            "heading": ac.get("track", 0),
                            "lat": ac["lat"],
                            "lon": ac["lon"],
                        })
                return flights
        except Exception:
            pass
        return []

    def update(self):
        """Polls for nearby aircraft."""
        now = time.time()
        # Avoid hammering the API faster than every 10 seconds
        if now - self.last_update < 10:
            return

        self.last_update = now
        flights = []
        if self.config.source == "local_adsb":
            flights = self._fetch_from_local_adsb()
        else:
            flights = self._fetch_from_fr24()

        if flights:
            # Pick the first aircraft or sort by closest/altitude
            self.current_flight = flights[0]
        else:
            self.current_flight = None
