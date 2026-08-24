from setuptools import setup, find_packages

setup(
    name="flighttracker-plugin",
    version="0.1.2",
    description="Overhead aircraft tracking plugin for MLB-LED-Scoreboard",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "Pillow>=10.0.0,<12.0.0",
    ],
    entry_points={
        "bullpen": [
            "flighttracker = flighttracker:load",
        ],
    },
)
