"""Script defining the preferences dialog."""

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *

from locations import Locations

class PreferencesDialog(QDialog):
    """Class defining the preferences dialog window."""

    def __init__(self):
        """Constructor. This class must be executed directly by calling this.exec_()."""
        QDialog.__init__(self)

        # Initializing the UI
        self.__initUI()


    def __initUI(self):
        """Method creating the UI for this window."""

        # Setting title
        self.setWindowTitle("Préférences")

        # Creating main layout
        main_layout = QVBoxLayout()
        
        # Creating the top widget
        self.pwd_widget = PwdWidget(self)
        main_layout.addWidget(self.pwd_widget)

        # Creating the bottom widget
        self.preferences_widget = PreferencesWidget()
        self.preferences_widget.setEnabled(False)

        main_layout.addWidget(self.preferences_widget)

        # Setting the main layout
        self.setLayout(main_layout)

    def enableBottomWidget(self):
        self.preferences_widget.setEnabled(True)


class PwdWidget(QWidget):
    """Class defining a widget containing the fields necessary for the passsword verification"""

    def __init__(self,parent):
        """Constructor."""
        QWidget.__init__(self)

        self.ip = ""

        self.__initUI(parent)

    def __initUI(self,parent):
        """Method used to build the UI of the widget."""

        frame = QFrame(self)
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        main_layout = QFormLayout()

        pwd_label= QLabel("Mot de passe :")
        self.pwd_le = QLineEdit()

        main_layout.addRow(pwd_label, self.pwd_le)

        button = QPushButton("Vérification")
        
        button.clicked.connect(lambda: self.pwdCheck(parent))

        main_layout.addRow(button)

        frame.setLayout(main_layout)

        layout = QHBoxLayout()
        layout.addWidget(frame)
        self.setLayout(layout)

    def pwdCheck(self,parent):
        with open("password.txt","r") as f:
            password = f.readline()
            if password == self.pwd_le.text():
                parent.enableBottomWidget()

class PreferencesWidget(QWidget):
    def __init__(self):
        """Constructor."""
        QWidget.__init__(self)

        self.ip = ""

        self.__initUI()

    def __initUI(self):
        """Method used to build the UI of the widget."""

        frame = QFrame(self)
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        main_layout = QFormLayout()

        size_lb = QLabel("Taille de police :")

        list_size = [str(i) for i in range(6,50)]
        
        self.size_combo = QComboBox(self)        
        self.size_combo.addItems(list_size)
        
        main_layout.addRow(size_lb, self.size_combo)

        font_lb = QLabel("Police :")

        f = open("fonts.txt", "r")
        list_font = f.readlines()
        f.close()
        list_font =  [c.strip() for c in list_font]

        self.font_combo = QComboBox(self)
        self.font_combo.addItems(list_font)

        main_layout.addRow(font_lb, self.font_combo)

        bold_checkBox = QCheckBox("Bold", self)

        main_layout.addRow(bold_checkBox)
        
##        button_color_font = QPushButton("Color font", self)
##        button_color_font.clicked.connect(self.showDialog)
##
##        button_color_background = QPushButton("Color background", self)
##        button_color_background.clicked.connect(self.showDialog)
##
##        main_layout.addRow(button_color_font, button_color_background)
##
        

        button = QPushButton("Appliquer")
        button.clicked.connect(lambda: write(self, self.size_combo.currentText() ,self.font_combo.currentText(), bold_checkBox.isTristate))
        
        main_layout.addRow(button)

        frame.setLayout(main_layout)
        
        layout = QHBoxLayout()
        layout.addWidget(frame)
        self.setLayout(layout)

        def write(self, text_size, text_font, bool_bold):
            with open("stylebu.qss","r") as f:
                lines = f.readlines()
                if bool_bold:
                    lines[17] = "\tfont: bold {0}pt {1};\n".format(text_size,text_font)
                else:
                    lines[17] = "\tfont: {0}pt {1};\n".format(text_size,text_font)
                with open("style.qss","w") as f2:
                    for x in lines:
                        f2.write(x)

##    def showDialog(self):
##        col = QColorDialog.getColor()
##        if col.isValid():
##            col.rgb()
            
                
                
            
