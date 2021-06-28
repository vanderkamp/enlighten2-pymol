from qt_wrapper import QtWidgets, QtCore, QtGui


class ElidedLabel(QtWidgets.QLabel):

    def setText(self, text):
        fm = QtGui.QFontMetrics(self.font())
        elided_text = fm.elidedText(text, QtCore.Qt.ElideRight, self.width())
        super(ElidedLabel, self).setText(elided_text)
        self.setToolTip(text)
