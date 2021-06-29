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
        self.object1Combo.currentTextChanged.connect(self.on_first_changed)

    def setup_objects_list(self):
        objects = pymol.cmd.get_names('objects')
        self.object1Combo.clear()
        self.object1Combo.addItems(objects)
        self.object1Combo.setCurrentIndex(len(objects) - 1)

    def set_neb(self, value):
        self.neb = value
        self.object2Label.setEnabled(value)
        self.object2Combo.setEnabled(value)

        if not value:
            self.object2Combo.clear()
        else:
            self.on_first_changed(self.object1Combo.currentText())

    def on_first_changed(self, name):
        if not self.neb:
            return

        hash1 = self._obj_hash(name)
        valid_second_objects = []
        for second_name in pymol.cmd.get_names('objects'):
            if second_name != name and self._obj_hash(second_name) == hash1:
                valid_second_objects.append(second_name)

        self.object2Combo.clear()
        if len(valid_second_objects) == 0:
            self.object2Combo.hide()
            self.object2ErrorLabel.show()
            return

        self.object2ErrorLabel.hide()
        self.object2Combo.show()
        self.object2Combo.addItems(valid_second_objects)
        self.object2Combo.setCurrentIndex(len(valid_second_objects) - 1)

    @staticmethod
    def _obj_hash(name):
        space = {'names': []}
        pymol.cmd.iterate(name, 'names.append(name)', space=space)
        return ':'.join(space['names'])
