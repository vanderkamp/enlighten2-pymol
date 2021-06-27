from .windows import ManagedWindow
from qt_wrapper import QtGui
import os
from validators import NotEmptyValidator, IntegerValidator


class QmmmTab(ManagedWindow):

    NEB_WIDGETS = ('object2Label', 'object2Combo')

    def __init__(self, name, window_manager):
        path = os.path.join(os.path.dirname(__file__), 'qmmm.ui')
        super(QmmmTab, self).__init__(name, path, window_manager)
        self.setup_file_selectors()
        self.setup_radio_buttons()
        self.setup_objects_list()
        self.ligandChargeEdit.setValidator(QtGui.QIntValidator())
        self.ligandChargeEdit.set_validator(IntegerValidator('Ligand charge'))
        self.jobNameEdit.set_validator(NotEmptyValidator('System name'))

    def setup_file_selectors(self):
        self.workingDirSelector.set_directory_mode(True)

    def setup_radio_buttons(self):
        self.optRadio.setChecked(True)
        self.nebRadio.setChecked(False)
        self.on_radio_changed(False)
        self.nebRadio.toggled.connect(self.on_radio_changed)

    def setup_objects_list(self):
        import pymol
        objects = pymol.cmd.get_names('objects')
        self.object1Combo.clear()
        self.object1Combo.addItems(objects)
        self.object1Combo.setCurrentIndex(len(objects) - 1)

    def on_radio_changed(self, value):
        self.set_group_enabled(self.NEB_WIDGETS, value)

    def bind(self, controller):
        pass
