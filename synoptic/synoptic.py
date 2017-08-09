import os

from taurus.external.qt import Qt

from PyTango import DevState, Database

from svgsynoptic2.taurussynopticwidget import TaurusSynopticWidget
from taurus.qt.qtgui.panel import TaurusDevicePanel, TaurusForm
import taurus

from popup import CommandsWidgetPopup, ResetCommandsWidgetPopup


class TaurusFormExpanding(TaurusForm):

    "A TaurusForm that adapts its size to its children"

    max_vertical_size = 500

    def sizeHint(self):
        frame = self.scrollArea.widget()
        framehint = frame.sizeHint()
        hint = Qt.QSize(framehint.width(), min(self.max_vertical_size,
                                               framehint.height()))
        return hint + self.buttonBox.sizeHint() + Qt.QSize(0, 20)


class PyStateComposerMotorWidget(TaurusFormExpanding):

    "A widget for displaying motors listed in a PyStateComposer"

    _customWidgetMap = getattr(taurus.tauruscustomsettings,
                               'T_FORM_CUSTOM_WIDGET_MAP', {})

    def setModel(self, device):
        devices = self.get_devices(device)
        self.setCustomWidgetMap(getattr(taurus.tauruscustomsettings,
                                        'T_FORM_CUSTOM_WIDGET_MAP', {}))
        self.setWithButtons(False)
        TaurusFormExpanding.setModel(self, devices)

    @staticmethod
    def get_devices(composer):
        db = Database()
        return db.get_device_property(
            str(composer), "DevicesList")["DevicesList"]


class PlcPopup(ResetCommandsWidgetPopup):
    "Quick reset for plc"
    commands = "Reset"


class ValvePopup(CommandsWidgetPopup):
    "Quick open/close for vacuum valves"
    commands = ("Open", DevState.OPEN), ("Close", DevState.CLOSE)


class ScreenPopup(CommandsWidgetPopup):
    "Quick movements for camera screens"
    commands = ("MoveIn", DevState.INSERT), ("MoveOut", DevState.EXTRACT)


CLASS_PANELS = {
    "VacuumValve": ValvePopup,
    "CameraScreen": ScreenPopup,
    "HeatAbsorber": ValvePopup,
    "BeamShutter": ValvePopup,
    "AllenBradleyEIP": PlcPopup,
    "PyStateComposer": PyStateComposerMotorWidget
}


class SynopticWidget(TaurusSynopticWidget):

    def get_device_panel(self, device):
        """Override to change which panel is opened for a given
        device name. Return a widget class, or None if you're
        handling the panel yourself"""
        print "Get panel device", device
        try:
            devclass = taurus.Database().get_class_for_device(str(device))
        except:
            devclass = None

        if CLASS_PANELS.get(devclass):
            return CLASS_PANELS[devclass]
        else:
            print "No custom panel for", devclass, " - ", device
            return TaurusDevicePanel


def main():
    qapp = Qt.QApplication([])

    # We need to give the absolute path to the HTML file
    # because our webview is setup to load assets from the
    # svgsynoptic library's path, not from the module's path.
    path = os.path.dirname(__file__)
    widget = SynopticWidget()
    widget.setModel(os.path.join(path, "index.html"))

    widget.show()
    widget.setWindowTitle("Beamline synoptic")
    qapp.exec_()


if __name__ == "__main__":
    main()
