"""Script defining the preferences dialog."""

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QWidget, QFrame, QSizePolicy, QFormLayout, QLabel, QComboBox, \
    QLineEdit, QPushButton, QHBoxLayout

from locations import Locations

class PreferencesDialog(QDialog):
    """Class defining the preferences dialog window."""

    barParameters = pyqtSignal(str)
    connectParameters = pyqtSignal(tuple)

    def __init__(self, location):
        """Constructor. This class must be executed directly by calling this.exec_()."""
        QDialog.__init__(self)

        self.location = location

        # Initializing the UI
        self.__initUI(location)

        # Handling communications
        self.connect_widget.connectParameters.connect(self.connectParameters.emit)
        self.bar_widget.barParameters.connect(lambda x: self.barParameters.emit(x))

    def __initUI(self, location):
        """Method creating the UI for this window."""

        # Setting title
        self.setWindowTitle("Préférences")

        # Creating main layout
        main_layout = QVBoxLayout()

        # Creating the top widget
        self.connect_widget = ConnectionWidget(location)
        main_layout.addWidget(self.connect_widget)

        # Creating the bottom widget
        self.bar_widget = BarWidget()
        self.bar_widget.setEnabled(False)

        main_layout.addWidget(self.bar_widget)

        # Setting the main layout
        self.setLayout(main_layout)

    def set_ips(self, ips_list):
        """Method modifying the list of ips the app can connect to."""
        self.connect_widget.set_ips(ips_list)

    def set_names(self, names_list):
        """Method modifying the list of bar names the bar can take."""
        try:
            self.bar_widget.set_names(names_list)
        except AttributeError:
            raise ValueError("This window was set up on the server side and therefore has no bar name.")

    def validate_connection_infos(self):
        """Method called after the connection infos have been sent to the core to skip to next part."""
        self.bar_widget.setEnabled(True)

    def validate_bar_name(self):
        """Method called after the bar name was set."""
        self.close()

    def fill_values(self, infos, name):
        """Method setting the values of the fields."""
        if infos[0]:
            if self.location == Locations.RESERVE:  # Combobox
                index = self.connect_widget.ip_cb.findText(infos[0])
                if index == -1:  # Not found
                    self.connect_widget.ip_cb.addItem(infos[0])
                    index = self.connect_widget.ip_cb.findText(infos[0])
                self.connect_widget.ip_cb.setCurrentIndex(index)
            else:  # ip_cb is a text edit
                self.connect_widget.ip_cb.setText(infos[0])
        if infos[1]:
            self.connect_widget.port_le.setText(str(infos[1]))

        if infos[0] and infos[1]:  # Both are set
            self.connectParameters.emit(infos)
            self.bar_widget.setEnabled(True)

        self.bar_widget.create_le.setText(name)


class ConnectionWidget(QWidget):
    """Class defining a widget containing the fields necessary to connection config."""

    connectParameters = pyqtSignal(tuple)

    def __init__(self, location):
        """Constructor."""
        QWidget.__init__(self)

        self.ip = ""

        self.__initUI(location)

    def __initUI(self, location):
        """Method used to build the UI of the widget."""

        frame = QFrame(self)
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        main_layout = QFormLayout()

        ip_label = QLabel("Adresse IP :")
        if location is Locations.RESERVE:
            self.ip_cb = QComboBox(self)
            self.ip_cb.activated[str].connect(self.__change_ip)
        else:
            self.ip_cb = QLineEdit()
            self.ip_cb.textChanged.connect(self.__change_ip)

        main_layout.addRow(ip_label, self.ip_cb)

        port_label = QLabel("Port de connexion :")
        self.port_le = QLineEdit()

        main_layout.addRow(port_label, self.port_le)

        button = QPushButton("Connexion")
        button.clicked.connect(lambda: self.connectParameters.emit((self.ip, int(self.port_le.text()))))

        main_layout.addRow(button)

        frame.setLayout(main_layout)

        layout = QHBoxLayout()
        layout.addWidget(frame)
        self.setLayout(layout)

    def __change_ip(self, ip):
        """Method called when changing the combo box value."""
        self.ip = ip

    def set_ips(self, ips_list):
        """Method used to populate the combobox with ips."""
        if len(ips_list) > 0:
            self.ip = ips_list[0]

        for ip in ips_list:
            self.ip_cb.addItem(ip)


class BarWidget(QWidget):
    """Class defining a dialog window to retrieve the bar."""

    barParameters = pyqtSignal(str)

    def __init__(self):
        """Constructor."""
        QWidget.__init__(self)

        self.bar = ""

        self.__initUI()

    def __initUI(self):
        """Method used to construct the UI."""

        frame = QFrame(self)
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        main_layout = QFormLayout()

        bar_label = QLabel("Choisissez votre bar :")
        self.bar_cb = QComboBox(self)
        self.bar_cb.activated[str].connect(self.__change_bar)

        main_layout.addRow(bar_label, self.bar_cb)

        bar_creation_label = QLabel("Ou créez votre bar :")
        self.create_le = QLineEdit()
        self.create_le.textChanged.connect(self.__change_bar)

        main_layout.addRow(bar_creation_label, self.create_le)

        button = QPushButton("Valider")
        button.clicked.connect(lambda: self.barParameters.emit(self.bar if self.bar else "inconnu"))

        main_layout.addRow(button)

        frame.setLayout(main_layout)

        layout = QHBoxLayout()
        layout.addWidget(frame)
        self.setLayout(layout)

    def __change_bar(self, bar):
        """Method called when changing the combobox value."""
        self.bar = bar

    def set_names(self, bars_list):
        """Method used to populate the combobox with ips."""
        if len(bars_list) > 0:
            self.bar = bars_list[0]

        for ip in bars_list:
            self.bar_cb.addItem(ip)
            
class SettingsWidget(QWidget):
    """Class defining a dialog window to retrieve the bar."""

    barParameters = pyqtSignal(str)

    def __init__(self):
        """Constructor."""
        QWidget.__init__(self)

        self.bar = ""

        self.__initUI()

    def __initUI(self):
        """Method used to construct the UI."""

        frame = QFrame(self)
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        main_layout = QFormLayout()

        pwd_lb = QLabel("Mot de passe :")
        self.pwd_le = QLineEdit()
        self.pwd_le.activated[str].connect(lambda:pass)

        main_layout.addRow(pwd_lb, pwd_le)

        size_lb = QLabel("Taille de la police :")
        self.size_le = QLineEdit()
        self.size_le.textChanged.connect(lambda:pass)

        main_layout.addRow(size_lb, self.size_le)

        button = QPushButton("Valider")
        button.clicked.connect(lambda:pass)

        main_layout.addRow(button)

        frame.setLayout(main_layout)

        layout = QHBoxLayout()
        layout.addWidget(frame)
        self.setLayout(layout)
