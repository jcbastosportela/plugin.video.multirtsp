import enum
from utils import warn
from dataclasses import dataclass
import xbmcaddon


class SettingsIds(enum.Enum):
    _FIRST_TIME = enum.auto()
    PLAY_TIME = enum.auto()
    STREAM_NAMES = enum.auto()
    STREAM_URLS = enum.auto()


@dataclass
class Settings:
    PLAY_TIME:int = 30
    STREAM_NAMES:str = "My Stream"
    STREAM_URLS:str = "rtsp://170.93.143.139/rtplive/470011e600ef003a004ee33696235daa"

    def __post_init__(self):
        self.PLAY_TIME = int(self.PLAY_TIME)


def load() -> Settings:
    """Loads settings

    Returns:
        Settings: Loaded settings
    """
    addon = xbmcaddon.Addon()
    s = Settings()
    try:
        s = Settings(
            *[addon.getSetting(s.name) for s in SettingsIds if not s.name.startswith("_")]
        )
    except Exception as ex:
        warn(f"Couldn't load settings. Using defaults. Error: {ex}")
    return s
