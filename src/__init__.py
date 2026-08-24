from .config import FlightTrackerConfig
from .data import FlightTrackerData
from .renderer import FlightTrackerRenderer


def load():
    """Bullpen entrypoint hook."""
    return FlightTrackerConfig, FlightTrackerData, FlightTrackerRenderer
