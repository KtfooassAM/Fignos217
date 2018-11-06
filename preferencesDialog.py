"""Script defining the preferences window."""

import sys

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication


class SendConnectionInfos(QObject):  # No
    emitParameters = pyqtSignal(tuple)


class SendBarChose(QObject):  # No
    emitParameters = pyqtSignal(str)


class SendParameters(QObject):  # No
    emitParameters = pyqtSignal(dict)


class Communicate(QObject):  # Yes
    sendConnectionInfos = pyqtSignal(tuple)
    sendBarChoice = pyqtSignal(str)
    sendParameters = pyqtSignal(dict)


class ConnectionWidget(QWidget):
    """ Class defining a dialog widget to retrieve IP and port from user. """

    def __init__(self, dialog_window):
        """Constructor."""
        QWidget.__init__(self)
        self.__initUI(dialog_window)

    def __initUI(self, dialog_window):
        self.c = SendConnectionInfos()
        self.c.emitParameters.connect(dialog_window.receive_connection_info)

        frame = QFrame(self)
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        main_layout = QFormLayout()

        ip_label = QLabel("Adresse IP :")
        self.ip_cb = QComboBox(self)
        self.ip_cb.activated[str].connect(self.__cbChanged)
        # self.ip = ip_list[0]
        #
        # for ip in ip_list:
        #    self.ip_cb.addItem(ip)
        self.ip = ""

        main_layout.addRow(ip_label, self.ip_cb)

        port_label = QLabel("Port de connexion :")
        self.port_le = QLineEdit()
        main_layout.addRow(port_label, self.port_le)

        button = QPushButton("Connexion")
        button.clicked.connect(self.send)
        main_layout.addRow(button)

        frame.setLayout(main_layout)

        layout = QHBoxLayout()
        layout.addWidget(frame)
        self.setLayout(layout)

    def __cbChanged(self, text):
        self.ip = text

    def send(self):
        ip = self.ip
        port = self.port_le.text()
        self.c.emitParameters.emit((ip, port))


class BarWidget(QWidget):
    """ Class defining a dialog window to retrieve the bar. """

    def __init__(self, dialog_window, bar_list):
        """Constructor."""
        QWidget.__init__(self)
        self.__initUI(dialog_window, bar_list)

    def __initUI(self, dialog_window, bar_list):

        frame = QFrame(self)
        frame.setFrameShape(QFrame.StyledPanel)

        main_layout = QFormLayout()

        self.c = SendBarChose()
        self.c.emitParameters.connect(dialog_window.receive_bar_info)

        bar_label = QLabel("Choisissez votre bar :")
        self.bar_cb = QComboBox(self)
        self.bar_cb.activated[str].connect(self.__cbChanged)
        self.bar = bar_list[0]
        for bar in bar_list:
            self.bar_cb.addItem(bar)
        main_layout.addRow(bar_label, self.bar_cb)

        bar_creation_label = QLabel("Ou créez votre bar :")
        self.create_le = QLineEdit()
        main_layout.addRow(bar_creation_label, self.create_le)

        button = QPushButton("Valider")
        button.clicked.connect(self.send)
        main_layout.addRow(button)

        frame.setLayout(main_layout)

        layout = QHBoxLayout()
        layout.addWidget(frame)
        self.setLayout(layout)

    def __cbChanged(self, text):
        self.bar = text

    def send(self):
        if self.create_le.text() != "":
            bar = self.create_le.text()
        else:
            bar = self.bar
        self.c.emitParameters.emit(bar)


class PreferencesDialog(QDialog):
    """ Class defining a dialog window to set preferences."""

    def __init__(self, location):
        """Constructor."""
        QDialog.__init__(self)

        # Initializing output
        self.parameters = {}

        # Initializing the UI
        self.__initUI(location)

    def __initUI(self, location):
        """Method initializing the UI."""

        self.main_layout = QVBoxLayout()

        self.c = SendParameters()  # No then
        self.c.emitParameters.connect(receive_preferences)

        # try:
        #     self.connect_widget = ConnectionWidget(self, ip_list)
        # except:
        #     self.connect_widget = ConnectionWidget(self, [""])
        #     self.connect_widget.setEnabled(False)
        self.connect_widget = ConnectionWidget(self)

        self.bar_widget = BarWidget(self, [""])
        self.bar_widget.setEnabled(False)

        self.main_layout.addWidget(self.connect_widget)
        self.main_layout.addWidget(self.bar_widget)

        self.setLayout(self.main_layout)
        self.setWindowTitle('Préférences')

        # Preventing the dialog window to be re-sized
        # self.setFixedSize(self.size())

        self.exec_()

    def setIPList(self, ip_list):
        self.ip_list = ip_list # Not enough

    def setBarList(self, bar_list):
        self.bar_list = bar_list

    def receive_connection_info(self, val):
        self.parameters["IP"] = val[0]
        self.parameters["Host"] = val[1]  # WHat?
        self.bar_list = ["zqedZQERFT5", "<FSFQSDFG", "qzsefrdtgfy"]
        self.bar_widget.hide()
        self.bar_widget = BarWidget(self, self.bar_list)
        self.main_layout.addWidget(self.bar_widget)

    def receive_bar_info(self, val):
        self.parameters["Bar"] = val
        self.c.emitParameters.emit(self.parameters)
        self.close()


def receive_preferences(val):
    print(val)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cd = PreferencesDialog([])
