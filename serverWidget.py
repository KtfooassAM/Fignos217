"""Script defining the server main widget."""

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import *

from verticalScroll import VerticalScroll


class ServerWidget(QWidget):
    """Class defining the main widget of the server window."""

    sending_refuel = pyqtSignal(tuple)

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
        top_label = QLabel("Demandes de réapprovisionnements", self)

        # Create a custom vertical scroll area
        self.scroll = VerticalScroll(bottom_stretch=True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Add the elements
        layout.addWidget(top_label)
        layout.addWidget(self.scroll)

        # Set the layout
        self.setLayout(layout)

    def add_prevision_widget(self, bar, drink, time):
        """Method adding a UI element to the prevision list. Not meant to be called directly"""

        # Create a new prevision widget
        prevision_widget = PrevisionWidget(Prevision(bar, drink, time))

        prevision_widget.send_refill.connect(self.sending_refuel)

        # Add the widget to the vertical scroll area, alays at the bottom for further sorting
        self.scroll.add_widget(prevision_widget)

    def delete_prevision_widget(self, bar, drink):
        """Method deleting a prevision widget from the shwon prevision list"""

        # Delete the prevision widget
        self.scroll.remove_widget(self.get_prevision_widget_id(bar, drink))

    def __sort_previsions(self):
        """Method sorting the UI elements related to previsions according to priority."""

        # Sort the list of prevision widgets by time
        self.scroll.widgets_list.sort(key=lambda x: x.prevision.time)
        self.scroll._refresh()

    def get_prevision_widget_id(self, bar, drink):
        """Method returning the id of the given widget in the scroll."""

        for i, w in enumerate(self.scroll.widgets_list):
            if w.prevision.drink == drink and w.prevision.bar == bar:
                return i

        return -1

    def update_prevision_widget(self, bar, drink, time, is_critical, is_refuel):
        """Method called to update the widgets with new data."""

        # Searching for a previous record
        id = self.get_prevision_widget_id(bar, drink)

        if is_critical:
            if id != -1:
                widget = self.scroll.widgets_list[id]
                widget.update_time(time)
                if is_refuel:
                    widget.setEnabled(True)
                    widget.slider.slider.setValue(3)
            else:
                self.add_prevision_widget(bar, drink, time)
        else:
            if id != -1:
                self.scroll.remove_widget(id)

        # Re computing the order of the notifications (and refreshing)
        self.__sort_previsions()


class PrevisionWidget(QFrame):
    """Class defining the notification widget for a prevision."""

    send_refill = pyqtSignal(tuple)

    # cancel_refill = pyqtSignal()

    def __init__(self, prevision):
        """Constructor"""

        QWidget.__init__(self)
        self.prevision = prevision  # For further access

        # Create the UI
        self.__init_UI()

    def __init_UI(self):
        """Method creating the UI of the prevision label"""

        # Create the layout
        layout = QHBoxLayout()

        # Create the label with text defined in constructor
        self.label = QLabel(self)
        self.__update_label()

        # # Create the slider
        # self.slider = QSlider(Qt.Horizontal, self)
        # self.slider.setRange(1, 4)
        # # self.slider.setMinimum(1)
        # # self.slider.setMaximum(4)
        # self.slider.setValue(3)
        # # self.slider.setTickPosition(QSlider.TicksBelow)
        # # self.slider.setTickInterval(1)
        # grid_layout = QGridLayout(self)
        # grid_layout.addWidget(self.slider, 0, 0, 1, 4)
        # for i in range(1, 5):
        #     grid_layout.addWidget(QLabel(str(i), self), 1, i, 1, 1)
        self.slider = SliderWidget(1, 4, 3)

        # Create the 'Réapprovisionner' button
        self.button = QPushButton("Réapprovisionner", self)
        # self.button.setFixedWidth(134)
        self.button.clicked.connect(self.__button_clicked_to_refill)

        # Add the elements
        layout.addWidget(self.label)
        layout.addStretch(1)
        # layout.addWidget(QLabel("1"))
        # layout.addWidget(self.slider)
        # layout.addWidget(QLabel("4"))
        layout.addWidget(self.slider)
        layout.addWidget(self.button)

        # Set the layout
        self.setLayout(layout)

    def __button_clicked_to_refill(self):
        """Method called when the button is clicked to go refill."""

        # Retrieve the quantity chosen
        quantity = self.slider.value()

        # Send the data
        self.send_refill.emit((self.prevision.bar, self.prevision.drink, quantity))

        # Disable the slider
        # self.slider.setEnabled(False)

        # Change the button properties
        # self.button.setText("Annuler")
        # self.button.setEnabled(False)
        # self.button.setFixedWidth(134)

        self.setEnabled(False)

        # Reconnecting the button to second behavior
        # self.button.clicked.disconnect()  # Forget about that refilling function
        # self.button.clicked.connect(self.__button_clicked_to_cancel)

    def update_time(self, time):
        """Method called to modify the time of the prevision."""

        print("Modifying time of refill of drink '{}' in bar '{}' to '{}'".format(self.prevision.drink.capitalize(),
                                                                                  self.prevision.bar.capitalize(), time))
        self.prevision.time = time
        self.__update_label()

    def __update_label(self):
        """Method used to reset the label."""

        ZERO_TIME = "Imminent"

        # Reformating duration to human readable
        if self.prevision.time > 0:
            time = ""
            if self.prevision.time >= 60:  # More than one hour
                time += str(int(self.prevision.time // 60)) + "h "
            time += str(round(self.prevision.time % 60)) + "min"
        else:
            time = ZERO_TIME

        # Creating text
        text = "{}<br>{}<br>({})".format(self.prevision.bar.capitalize(), self.prevision.drink.capitalize(), time)

        # Setting colors
        if time is ZERO_TIME:
            color = 'red'
        else:
            color = 'black'

        # Setting text
        self.label.setText("<font color='{}'>{}</font>".format(color, text))


class Prevision():
    """Class defining a prevision"""

    def __init__(self, bar, drink, time):
        """Constructor"""
        self.bar = bar
        self.drink = drink
        self.time = time


class SliderWidget(QWidget):
    """Class defining a slider widget."""

    def __init__(self, min, max, value, interval=1):
        """Constructor."""
        QWidget.__init__(self)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(min, max)
        self.slider.setValue(value)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(interval)

        grid_layout = QGridLayout(self)
        grid_layout.addWidget(self.slider, 1, 0, 1, 4)
        for i in range(4):
            label = QLabel(str(i + 1), self)
            label.setAlignment(Qt.AlignCenter)
            grid_layout.addWidget(label, 0, i, 1, 1)

        self.setLayout(grid_layout)

    def value(self):
        """Method returning the current value of the slider."""
        return self.slider.value()


if __name__ == "__main__":
    # Importing modules used to run the app
    from PyQt5.QtWidgets import QApplication
    import sys

    # Instantiating the objects
    app = QApplication(sys.argv)

    ## TEST PREVISION WIDGET
    # prevision_widget = PrevisionWidget(Prevision(0, "Tesla", "Vin", 14))
    # prevision_widget.show()

    ## TEST SERVER WIDGET
    server_widget = ServerWidget()

    prevision_test_list = [("Tesla", "Vin", 2), ("Edison", "Bière", 5), ("Da Vinci", "Grenadine", 1)]

    for prevision in prevision_test_list:
        bar, drink, time = prevision
        server_widget.add_prevision_widget(bar, drink, time)
        
    # Showing
    server_widget.show()

    # Launching the app
    sys.exit(app.exec_())
