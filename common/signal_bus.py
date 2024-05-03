from PySide6.QtCore import QObject, Signal, Slot


class Bus(QObject):
    micaEnableChanged = Signal(bool)

    def onMicaChanged(self, isChecked):
        # self.micaEnabled.se(isChecked)
        self.micaEnableChanged.emit(isChecked)


signalBus = Bus()
