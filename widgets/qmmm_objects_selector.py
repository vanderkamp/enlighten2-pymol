from qt_wrapper import QtWidgets, uic
import os
import pymol


class QmmmObjectsSelector(QtWidgets.QWidget):

    NEB_WIDGETS = ('object2Label', 'object2Combo')

    def __init__(self, *args):
        super(QmmmObjectsSelector, self).__init__(*args)

        ui_file = os.path.join(os.path.dirname(__file__),
                               'qmmm_objects_selector.ui')
        uic.loadUi(ui_file, self)
        self.setup_objects_list()
        self.neb = True

    def setup_objects_list(self):
        objects = pymol.cmd.get_names('objects')
        self.object1Combo.clear()
        self.object1Combo.addItems(objects)
        self.object1Combo.setCurrentIndex(len(objects) - 1)

    def set_neb(self, value):
        self.neb = value
        self.object2Label.setEnabled(value)
        self.object2Combo.setEnabled(value)
