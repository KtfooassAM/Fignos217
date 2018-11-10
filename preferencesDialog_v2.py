"""Script defining the preferences dialog."""

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QWidget, QFrame, QSizePolicy, QFormLayout, QLabel, QComboBox, \
    QLineEdit, QPushButton, QHBoxLayout

from locations import Locations

class PreferencesDialog(QDialog):
    """Class defining the preferences dialog window."""

    def __init__(self, location):
        """Constructor. This class must be executed directly by calling this.exec_()."""
        QDialog.__init__(self)

        self.location = location

        # Initializing the UI
        self.__initUI(location)


    def __initUI(self, location):
        """Method creating the UI for this window."""

        # Setting title
        self.setWindowTitle("Préférences")

        # Creating main layout
        main_layout = QVBoxLayout()
        
        # Creating the top widget
        self.pwd_widget = PwdWidget()
        main_layout.addWidget(self.pwd_widget)

        # Creating the bottom widget
        self.preferences_widget = PreferencesWidget()
        self.preferences_widget.setEnabled(False)

        main_layout.addWidget(self.preferences_widget)

        # Setting the main layout
        self.setLayout(main_layout)


class PwdWidget():
    """Class defining a widget containing the fields necessary for the passsword verification"""

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

        pwd_label= QLabel("Mot de passe :")
        self.pwd_le = QLineEdit()

        main_layout.addRow(pwd_label, self.pwd_le)

        button = QPushButton("Vérification")
        ##button.clicked.connect(lambda: x:x)

        main_layout.addRow(button)

        frame.setLayout(main_layout)

        layout = QHBoxLayout()
        layout.addWidget(frame)
        self.setLayout(layout)

class PreferenceWidget():
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

        size_lb = QLabel("Taille de police :")

        list_size = [i for i in range(6,50)]
        
        self.size_combo = QComboBox(self)        
        self.size_combo.addItems(list_size)
        
        main_layout.addRow(size_lb, self.size_combo)

        font_lb = QFormLayout()

        f = open("fonts.txt", "r")
        list_font = f.readlines()
        f.close()
        list_font =  [c.strip() for c in lignes]

        self.font_combo = QComboBox(self)
        self.font_combo.addItems(list_font)

        main_layout.addRow(font_lb, self.font_combo)
        



        frame.setLayout(main_layout)

        layout = QHBoxLayout()
        layout.addWidget(frame)
        self.setLayout(layout)
