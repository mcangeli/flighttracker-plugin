from .config import FlightTrackerConfig
from .data import FlightTrackerData
from .renderer import FlightTrackerRenderer


def load() -> api.PLUGIN_DEFINITION:
    return FlightTrackerConfig, FlightTrackerData, FlightTrackerRenderer
