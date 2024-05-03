import datetime
from qfluentwidgets import ConfigItem, BoolValidator, Theme, OptionsValidator, QConfig

YEAR = datetime.datetime.now().year
AUTHOR = "ByteBasher"
VERSION = "1.0.0"


class Config(QConfig):
    checkUpdate = ConfigItem("Update", "checkUpdate", True, BoolValidator())
    micaEnabled = ConfigItem("Mica", "mica", True, BoolValidator())


cfg = Config()
cfg.themeMode.value = Theme.AUTO
