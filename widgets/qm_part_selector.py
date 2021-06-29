from qt_wrapper import QtWidgets, uic
import os


class QmPartSelector(QtWidgets.QWidget):

    def __init__(self, *args):
        super(QmPartSelector, self).__init__(*args)

        ui_file = os.path.join(os.path.dirname(__file__),
                               'qm_part_selector.ui')
        uic.loadUi(ui_file, self)
