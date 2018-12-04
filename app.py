"""Script defining the base App class, with all the parameters shared between the server and the client application."""

import sys

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication


class App(QObject):
    """Base class defining a PyQt5 app."""

    send_connection_infos = pyqtSignal(list)
    send_bar_names = pyqtSignal(list)
    connection_established = pyqtSignal(tuple)
    name_set = pyqtSignal()
    fill_preferences = pyqtSignal(tuple, str)
    open_connection_dialog = pyqtSignal(list)
    send_champagne_cdf = pyqtSignal(list)
    

    message_received = pyqtSignal(tuple)

    def __init__(self, exit_on_quit=True):
        """Constructor."""
        QObject.__init__(self)

        self._name = ""

        # Creating the PyQt application
        self.__qApp = QApplication([sys.argv[0]])  # Prevent optional (and unwanted) parameters

        # Creating the window object
        self._open_window()

        # Connection signals
        self._connect_signals()

        # Exiting the app
        if exit_on_quit:  # Exit the program when quitting the app
            sys.exit(self.__qApp.exec_())
        else:
            self.__qApp.exec_()

    def _open_window(self):
        """Method opening the user interface."""

        # Importing test window (the base window)
        from window import Window

        # Creating the window
        self._window = Window(self)

    def _connect_signals(self):
        """Method used to connect the signals."""
        pass

if __name__ == "__main__":
    app = App()
