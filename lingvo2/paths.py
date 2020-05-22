import os

from pathlib import Path
ROOT = Path(os.path.join(os.path.dirname(__file__)))
CONFIG = ROOT / "config.yaml"
CARD_CONFIG = ROOT / "card_config.yaml"
PICKLE_CONFIG = ROOT / "pickle_config.pcl"
CORECONFIG = ROOT / "coreconfig.yaml"
DICTIONARIES = ROOT / "dictionaries"
CSS = ROOT / "css"
ICONS = ROOT / "resources/icons"
RESOURCES = ROOT / "resources"
UIFORM = ROOT / "gui/uiform"

DATATESTDIR = ROOT / "datatest"
BALABOLKA = ROOT / "libs/balcon/balcon.exe"