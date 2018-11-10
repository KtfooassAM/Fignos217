"""Script defining the connection dialog."""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QStyle

from locations import Locations


class ConnectionDialog(QDialog):
    """Class defining the connection dialog window."""

    def __init__(self, device_list):
        """Constructor. This class must be executed directly by calling this.exec_()."""
        QDialog.__init__(self)

        # Initializing the UI
        self.__init_UI(device_list)

    def __init_UI(self, device_list):
        """Method creating the UI for this window."""

        # Setting title
        self.setWindowTitle("Informations de connexion")

        # Creating main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel("Etat des différentes connexions :"))

        for device in device_list:
            name, state = device
            is_connected = bool(state)

            device_layout = QHBoxLayout()
            device_layout.addWidget(LedIndicator(is_connected))
            device_layout.addWidget(QLabel(name))
            device_layout.addStretch()

            main_layout.addLayout(device_layout)

        # Setting the main layout
        self.setLayout(main_layout)

        self.setFixedSize(self.sizeHint())


class LedIndicator(QPushButton):
    """Class defining a led indicator"""

    def __init__(self, state=False):
        """Constructor."""

        QPushButton.__init__(self)

        self.__init_UI(state)

    def __init_UI(self, state):
        """Method used to construct the UI."""

        self.setFlat(True)
        self.mousePressEvent = lambda event: event.ignore()
        self.set_state(state)

    def set_state(self, state):
        """Method changing the led state"""

        if state is True:
            icon = "SP_DialogYesButton"
        else:
            icon = "SP_DialogNoButton"

        self.setIcon(self.style().standardIcon(getattr(QStyle, icon)))


if __name__ == "__main__":
    # Importing modules used to run the app
    from PyQt5.QtWidgets import QApplication
    import sys

    # Instantiating the objects
    app = QApplication(sys.argv)

    devices_list = []
    for i in range(4):
        devices_list.append(("Bar {}".format(i), i % 2))

    widget = ConnectionDialog(devices_list)

    # Showing
    widget.show()

    # Launching the app
    sys.exit(app.exec_())
