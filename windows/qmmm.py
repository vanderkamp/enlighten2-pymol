from .windows import ManagedWindow
from qt_wrapper import QtGui
import os
from validators import NotEmptyValidator, IntegerValidator
from widgets.form import Form


class QmmmTab(ManagedWindow):

    def __init__(self, name, window_manager):
        path = os.path.join(os.path.dirname(__file__), 'qmmm.ui')
        super(QmmmTab, self).__init__(name, path, window_manager)
        self.setup_file_selectors()
        self.setup_radio_buttons()
        self.ligandChargeEdit.setValidator(QtGui.QIntValidator())
        self.ligandChargeEdit.set_validator(IntegerValidator('Ligand charge'))
        self.jobNameEdit.set_validator(NotEmptyValidator('System name'))

    def setup_file_selectors(self):
        self.workingDirSelector.set_directory_mode(True)

    def setup_radio_buttons(self):
        self.optRadio.setChecked(True)
        self.nebRadio.setChecked(False)
        self.objectsSelector.set_neb(False)
        self.nebRadio.toggled.connect(self.objectsSelector.set_neb)

    def bind(self, controller):
        controller.update('qmmm.neb', False)
        self.nebRadio.toggled.connect(controller.updater('qmmm.neb'))

        object1Combo = self.objectsSelector.object1Combo

        controller.update('qmmm.object1', object1Combo.currentText())
        controller.bind_qmmm_objects_selector('qmmm.object1',
                                              'qmmm.object2',
                                              self.objectsSelector)

        self.update_run_button()
        object1Combo.currentTextChanged.connect(self.update_run_button)
        self.nebRadio.toggled.connect(self.update_run_button)

        self.qmPartSelector.set_object(object1Combo.currentText())
        object1Combo.currentTextChanged.connect(self.qmPartSelector.set_object)
        self.qmPartSelector.selectionChanged.connect(
            controller.updater('qmmm.qm_region')
        )
        self.qmPartSelector.selectionChanged.connect(self.update_run_button)

        controller.bind_lineEdit('qmmm.charge', self.ligandChargeEdit)
        controller.bind_lineEdit('qmmm.job_name', self.jobNameEdit)
        controller.bind_file_selector('working_dir', self.workingDirSelector)

        self.form = Form(fields=(self.ligandChargeEdit,
                                 self.workingDirSelector.lineEdit,
                                 self.jobNameEdit),
                         button=self.runButton,
                         submit_callback=controller.run_qmmm)

    def update_run_button(self, *args):
        objects_valid = self.objectsSelector.is_valid()
        has_selection = self.qmPartSelector.has_selection()
        self.runButton.setEnabled(objects_valid and has_selection)
