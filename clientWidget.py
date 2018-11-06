"""Script defining the middle part of the client UI."""
""" On order drink name send to receive_order method
    On delivery validation send drink and amount delivered
    to receive_delivery_success method"""

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *

from verticalScroll import VerticalScroll


class ClientWidget(QWidget):
    """Class defining the methods and attributes specific to the command keyboard."""
    """ Add delivery notification : ClientWidget.delivery("Drink name", Quantity)"""

    order_drink = pyqtSignal(str, bool)
    refuel_completed = pyqtSignal(str, int, int)

    def __init__(self):
        """Constructor."""
        QWidget.__init__(self)

        self.__current_notif_id = 0

        self.__init_UI()

    def __init_UI(self):
        """Method called to initialize the UI of the widget."""

        # Add main layout
        main_layout = QVBoxLayout()

        # Add notification area layout
        notif_layout = QVBoxLayout()
        self.notification_area = VerticalScroll(bottom_stretch=True)

        self.notif_info = QLabel("Notifications")
        notif_layout.addWidget(self.notif_info)

        notif_layout.addWidget(self.notification_area)

        # Add grid layout for the visual keypad
        grid = QGridLayout()
        grid.setSpacing(10)

        # Create buttons for the keypad
        # font = QFont()
        # font.setPointSize(16)

        # There is a better way! Think about it
        # self.buttons_list = []
        self.buttons_dict = {}
        names = ['', '/', '*', '-',
                 '7', '8', '9', '',
                 '4', '5', '6', '',
                 '1', '2', '3', '',
                 '', '', '.', '']
        # '' are ignored
        # (n,h,w) will represent a button at the equivalent grid position
        # n will be the name of the button
        # h, w will be the dimension of the button
        names = ['', ('/', 1, 1), ('*', 1, 1), ('-', 1, 1),
                 ('7', 1, 1), ('8', 1, 1), ('9', 1, 1), ('+', 2, 1),
                 ('4', 1, 1), ('5', 1, 1), ('6', 1, 1), '',
                 ('1', 1, 1), ('2', 1, 1), ('3', 1, 1), '',
                 ('0', 1, 2), '', ('.', 1, 1), '']
        # first value = associated button name
        # second value = drink name
        # third value = associated key id
        # fourth value = associated color
        # fifth value = quantity unit
        # self.drink_list = [("1", None, 49, "#FFFFFF", "L"), ("2", None, 50, "#FFFFFF", "L"),
        #                    ("3", None, 51, "#FFFFFF", "L"), ("4", None, 52, "#FFFFFF", "L"),
        #                    ("5", None, 53, "#FFFFFF", "L"), ("6", None, 54, "#FFFFFF", "L"),
        #                    ("7", None, 55, "#FFFFFF", "L"), ("8", None, 56, "#FFFFFF", "L"),
        #                    ("9", None, 57, "#FFFFFF", "L"), ("0", None, 48, "#FFFFFF", "L"),
        #                    (".", None, 46, "#FFFFFF", "L"), ("+", None, 43, "#FFFFFF", "L"),
        #                    ("-", None, 45, "#FFFFFF", "L"), ("*", None, 42, "#FFFFFF", "L"),
        #                    ("/", None, 47, "#FFFFFF", "L")]
        self.keys_map = {49: '1', 50: '2', 51: '3', 52: '4', 53: '5', 54: '6', 55: '7', 56: '8', 57: '9', 48: '0',
                         46: '.', 47: '/', 42: '*', 45: '-', 43: '+'}
        positions = [(i, j) for i in range(5) for j in range(4)]

        for position, name in zip(positions, names):
            if name != '':
                txt, width, height = name
                btn = QPushButton(txt)
                self.buttons_dict[txt] = btn
                # self.buttons_list.append(QPushButton(txt))
                grid.addWidget(btn, *position, width, height)
                # color = "#FFFFFF"
                # btn.setStyleSheet('QPushButton {background-color: %s}' % color)
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                btn.key = txt
                btn.is_restal = False
                btn.clicked.connect(lambda: self.order_drink.emit(self.sender().key,
                                                                  self.sender().is_restal))  # self.__buttonPressEvent)
                # btn.setFont(font)

        # Add sub layouts to global layout
        main_layout.addLayout(notif_layout)
        main_layout.addLayout(grid)

        # Add main layout
        self.setLayout(main_layout)

    # def __buttonPressEvent(self):
    #     """ Associate a drink to the button clicked. """
    #     name = str(self.sender().text())
    #     for i in range(len(self.drink_list)):
    #         if self.drink_list[i][0] == name:
    #             self.__order_drink(i)
    #             break

    def keyPressEvent(self, event):
        """ Associate a drink to the button pressed. """
        # key = e.key()
        # for j in range(len(self.drink_list)):
        #     if self.drink_list[j][2] == key:
        #         # self.__order_drink(j)
        #         for button in self.buttons_dict.values():
        #             if button.text() == self.drink_list[j][0]:
        #                 button.animateClick()
        #                 break
        #         break
        try:
            key = self.keys_map[event.key()]
        except KeyError:
            pass
        else:
            # self.order_drink.emit(key)
            self.buttons_dict[key].animateClick()

    def __next_notif_id(self):
        """Method giving each notif a specific id."""
        self.__current_notif_id += 1
        return self.__current_notif_id

    def delivery(self, drink, quantity):
        """Add notification based on the drink name and the quantities"""
        print("Adding a notification for the refuel of {} of drink '{}'".format(quantity, drink))

        id = self.__next_notif_id()
        notif = NotifRefuel(drink, quantity, id)
        notif.refuel_completed.connect(self.refuel_completed)

        self.notification_area.add_widget(notif)
        self.notif_info.setText("Un ZiBar arrive avec :")

    def del_delivery(self, id_refuel):
        """Method removing a refuel notification by its id."""

        for i, w in enumerate(self.notification_area.widgets_list):
            if int(w.id_refuel) == int(id_refuel):
                self.notification_area.remove_widget(i)

        # for i in range(len(self.notif_list)):
        #     notif = self.notif_list[i]
        #     if notif.ID == ID:
        #         notif_list = []
        #         for j in range(len(self.notif_list)):
        #             if i != j:
        #                 notif_list.append(self.notif_list[j])
        #         self.notif_list = notif_list
        #         self.notification_area.remove_widget(i)
        #         break
        # if len(self.notif_list) == 0:
        #     self.notif_info.setText("En attente")


class NotifRefuel(QFrame):
    """Class defining the notification to be displayed in the client widget."""

    refuel_completed = pyqtSignal(str, int, int)

    def __init__(self, drink, quantity, id_refuel):
        """Constructor."""
        QWidget.__init__(self)
        self.drink = drink
        self.quantity = quantity
        self.id_refuel = id_refuel
        self.__init_UI(drink, quantity)

    def __init_UI(self, drink, quantity):
        """Method called to initialize the UI of the notification."""

        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)

        layout = QVBoxLayout()

        text = "\t{} caisses/bouteilles/saladiers de '{}'.".format(quantity, drink)
        text = QLabel(text)

        button = QPushButton("Réapprovisionnement effectué", self)
        button.clicked.connect(lambda: self.refuel_completed.emit(self.drink, self.quantity, self.id_refuel))
        button.setStyleSheet('QPushButton {background-color: #a01010; color: white;}')

        layout.addWidget(text)
        layout.addWidget(button)

        self.setLayout(layout)


if __name__ == '__main__':
    # Importing modules used to run the app
    from PyQt5.QtWidgets import QApplication
    import sys

    # Instantiating the objects
    app = QApplication(sys.argv)

    client_widget = ClientWidget()
    client_widget.show()
    client_widget.delivery("Boisson 1", 2)
    client_widget.delivery("Boisson 2", 2)

    # Launching the app
    sys.exit(app.exec_())

    # TO-DO:
    #     Reformat the notification : too much layouts
    #     Add command sending to buttons (+ keys)
    #     Add more modular system for buttons
    # /!\ Handle key presses
