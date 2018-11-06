"""Script defining the restal main widget."""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout, QPushButton

from verticalScroll import VerticalScroll


class OrderWidget(QFrame):
    """Class defining the notification widget for a prevision."""

    def __init__(self, bar, food, quantity):
        """Constructor"""

        QFrame.__init__(self)

        # Create the UI
        self.__init_UI(bar, food, quantity)

    def __init_UI(self, bar, food, quantity):
        """Method creating the UI of the prevision label"""

        # UI properties
        self.setStyleSheet("background-color: none;")
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)

        # Create the layout
        layout = QHBoxLayout()

        # Create the label with text defined in constructor
        label = QLabel("Le bar '{}' a besoin de {} assiette{} de {}.".format(bar.capitalize(), quantity,
                                                                             ("s" if quantity > 1 else ""),
                                                                             food))

        # Create the 'Completed' button
        button = QPushButton("Fait", self)
        button.clicked.connect(lambda: self.setEnabled(False))

        # Add the elements
        layout.addWidget(label)
        layout.addStretch(1)
        layout.addWidget(button)

        # Set the layout
        self.setLayout(layout)


class RestalWidget(QWidget):
    """Class defining the main widget of the server window."""

    def __init__(self):
        """Constructor."""

        QWidget.__init__(self)

        # Build the UI
        self.__init_UI()

    def __init_UI(self):
        """Method called to initialize the UI of the widget."""

        # Create main layout
        layout = QVBoxLayout()

        # Create a label
        top_label = QLabel("Commandes", self)

        # Create a custom vertical scroll area
        self.scroll = VerticalScroll(bottom_stretch=True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Add the elements
        layout.addWidget(top_label)
        layout.addWidget(self.scroll)

        # Set the layout
        self.setLayout(layout)

    def add_order(self, bar, food, quantity):
        """Method adding a UI element to the list."""

        # Create a new prevision widget
        widget = OrderWidget(bar, food, quantity)

        # Add the widget to the vertical scroll area, always at the bottom for further sorting
        self.scroll.add_widget(widget)

        if self.scroll.count() > 30:
            self.scroll.remove_widget(-1)
