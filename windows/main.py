from qt_wrapper import QtWidgets, QtCore
from .preparation import PreparationTab
from .preparation_advanced import PreparationAdvancedWindow
from .dynamics import DynamicsTab
from .qmmm import QmmmTab
from .windows import move_to_center


class MainWindow(QtWidgets.QTabWidget):

    def __init__(self, window_manager):
        super(MainWindow, self).__init__()
        self.setWindowFlag(QtCore.Qt.Tool)
        self.window_manager = window_manager
        self.setWindowTitle('Enlighten2')
        self.addTab(PreparationTab('prep', window_manager), 'Preparation')
        self.addTab(DynamicsTab('dynam', window_manager, self), 'Dynamics')
        self.addTab(QmmmTab('qmmm', window_manager), 'QM/MM')
        PreparationAdvancedWindow('prep_advanced', window_manager)
        self.setFixedSize(self.sizeHint())
        move_to_center(self)

    def closeEvent(self, event):
        self.window_manager.close_all()
