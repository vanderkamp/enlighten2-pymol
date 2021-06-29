from collections import Counter
from qt_wrapper import QtWidgets, QtCore, uic
import os
import pymol


class QmPartSelector(QtWidgets.QWidget):

    selectionChanged = QtCore.pyqtSignal(list)

    def __init__(self, *args):
        super(QmPartSelector, self).__init__(*args)

        ui_file = os.path.join(os.path.dirname(__file__),
                               'qm_part_selector.ui')
        uic.loadUi(ui_file, self)
        self.getSelectionButton.clicked.connect(self.parse_selection)
        self.object = None
        self.selection = []

    def set_object(self, name):
        if self.object != name:
            self.object = name
            self.selection = []
            self.reset_labels()

    def reset_labels(self):
        self.update_atoms_info_label([])
        self.update_res_info_label([], [])

    def parse_selection(self):
        if 'sele' not in pymol.cmd.get_names('selections'):
            self._error("No (sele) selection found")
            return

        if any(model != self.object for model in self._get_sele_key('model')):
            self._error("Only atoms from Structure 1 allowed in (sele)")
            return

        self.selection = self._get_sele_key('index')
        self.selectionChanged.emit(self.selection)
        self.update_atoms_info_label(self._get_sele_key('elem'))
        self.update_res_info_label(self._get_sele_key('resn'),
                                   self._get_sele_key('resi'))

    def update_atoms_info_label(self, elem):
        counted_elem = Counter(elem).items()
        sorted_counted_elem = sorted(counted_elem, key=lambda _: _[0])
        elem_text = ', '.join('{} {}'.format(n, el)
                              for el, n in sorted_counted_elem)
        if elem_text:
            elem_text = '(' + elem_text + ')'
        text = 'Atoms: {n} {elem_text}'.format(n=len(elem),
                                               elem_text=elem_text)
        self.atomsInfoLabel.setText(text)

    def update_res_info_label(self, resn, resi):
        res = {'{}{}'.format(resn, resi) for resn, resi in zip(resn, resi)}
        res_text = ', '.join(sorted(list(res)))
        if res_text:
            res_text = '(' + res_text + ')'
        text = 'Residues: {n} {res_text}'.format(n=len(res),
                                                 res_text=res_text)
        self.resInfoLabel.setText(text)

    def _error(self, error):
        QtWidgets.QMessageBox.critical(self, "Error", error)

    @staticmethod
    def _get_sele_key(key):
        space = {'data': []}
        pymol.cmd.iterate('sele', 'data.append(' + key + ')', space=space)
        return space['data']
