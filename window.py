"""Script defining a base window, with common attributes to both the client and server windows."""

from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *  # qApp, QMainWindow, QWidget, QHBoxLayout, QAction, QMessageBox, QPushButton

from chatPanel import ChatPanel
from connectionDialog import ConnectionDialog
from preferencesDialog_v2 import PreferencesDialog
from informationDialog import InformationDialog
from locations import Locations
from ordersPanel import OrdersPanel
from preferencesDialog_v2 import PreferencesDialog


class Window(QMainWindow):
    """Class defining a base window with attributes shared by both the client and server windows."""

    quit_app = pyqtSignal()
    export_db = pyqtSignal(str)
    get_connection_infos = pyqtSignal()
    get_bar_names = pyqtSignal()
    set_connection_infos = pyqtSignal(tuple)
    set_bar_name = pyqtSignal(str)
    send_message = pyqtSignal(str)
    ask_preferences = pyqtSignal()
    order_drink = pyqtSignal(str, bool)
    drop_base = pyqtSignal()
    cancel_order = pyqtSignal(int)
    sending_refuel = pyqtSignal(tuple)
    refuel_completed = pyqtSignal(str, int, int)
    request_connection_infos = pyqtSignal()

    def __init__(self, app, location=Locations.BAR):
        """Constructor."""
        QMainWindow.__init__(self)

        self.__app = app

        self.__location = location
        self.__drinks = {}

        # Initializing the UI
        self.__init_UI(location)

        # Connecting signals
        app.message_received.connect(self.chat_panel.add_message)
        self.chat_panel.send_message.connect(self.send_message)
        if location == Locations.BAR:
            self.main_widget.order_drink.connect(self.order_drink)
            self.__app.refuelling_in_progress.connect(self.add_refuel_notif)
            self.main_widget.refuel_completed.connect(self.confirm_refuel_complete)
        elif location == Locations.RESERVE:
            self.__app.request_refuel.connect(self.main_widget.update_prevision_widget)
            self.main_widget.sending_refuel.connect(self.sending_refuel)
        elif location == Locations.RESTAL:
            self.__app.add_order.connect(self.__add_restal_order)

    def __init_UI(self, location):
        """Method used to initialize the interface of the window."""

        # Set the title
        title = "Fignos - "
        if location == Locations.BAR:
            title += "Bar"
        elif location == Locations.RESERVE:
            title += "Réserve ZiBars"
        elif location == Locations.RESTAL:
            title += "Restal"
        elif location == Locations.CDF:
            title += "CDF"
        else:  # Adding this in case of a typo
            title += "Unknown location"
        self.setWindowTitle(title)

        # Adding the icon
        icon = QIcon()
        icon.addPixmap(QPixmap("teleks_ico.png"))
        self.setWindowIcon(icon)

        # Adding the menu
        menubar = self.menuBar()

        # Adding 'Fichier' sub-menu
        file_menu = menubar.addMenu("&Fichier")

        # Adding export option
        if location is Locations.RESERVE:
            export_act = QAction("&Exporter les données", self)
            export_act.setStatusTip("Exporter les données sous format Excel")
            export_act.setShortcut("Ctrl+E")
            export_act.triggered.connect(self.__export)

            file_menu.addAction(export_act)
            file_menu.addSeparator()

            # To be commented because zibars are morons
            drop_act = QAction("&Vider la table", self)
            drop_act.setStatusTip("Vider entièrement la base de données")
            drop_act.triggered.connect(self.drop_base)

            file_menu.addAction(drop_act)
            file_menu.addSeparator()

        # Adding exit option
        exit_act = QAction("&Quitter", self)
        exit_act.setStatusTip("Quitter l'application")
        #exit_act.setShortcut("Ctrl+Q")
        exit_act.triggered.connect(self.close)

        file_menu.addAction(exit_act)

        # Adding 'Editer' sub-menu
        edit_menu = menubar.addMenu("&Éditer")

        pref_act = QAction("&Préférences", self)
        pref_act.setStatusTip("Ouvrir le menu des préférences")
        #pref_act.setShortcut("Ctrl+P")
        pref_act.triggered.connect(self.__show_preferences_dialog)

        edit_menu.addAction(pref_act)

        conn_act = QAction("&Connexion", self)
        conn_act.setStatusTip("Ouvrir le menu de connexion")
        #conn_act.setShortcut("Ctrl+C")
        conn_act.triggered.connect(lambda: self.__show_connection_dialog(location))

        edit_menu.addAction(conn_act)
        
        infco_act = QAction("&Informations", self)
        infco_act.setStatusTip("Ouvrir les informations de connexion")
        #infco_act.setShortcut("Ctrl+I")
        infco_act.triggered.connect(self.__show_information_dialog)

        edit_menu.addAction(infco_act)

        # Adding 'Aide' sub-menu
        help_menu = menubar.addMenu("&Aide")

        help_act = QAction("&Aide", self)
        help_act.setStatusTip("Aide sur l'utilisation de l'application")
        help_act.setShortcut("Ctrl+H")
        help_act.triggered.connect(self.__show_help_dialog)

        about_act = QAction("&À propos", self)
        about_act.setStatusTip("À propos de l'application")
        about_act.triggered.connect(self.__show_about_dialog)

        help_menu.addAction(help_act)
        help_menu.addSeparator()
        help_menu.addAction(about_act)

        # Adding the status bar # Why?
        self.statusBar()

        # Creating the main widget of the window
        widget = QWidget()

        # Adding the global layout
        layout = QHBoxLayout()

        # Adding the left panel (orders)
        if location in [Locations.BAR, Locations.RESERVE]:  # To be modified
            self.orders_panel = OrdersPanel(location)
            self.orders_panel.cancel_order.connect(self.cancel_order)
            layout.addWidget(self.orders_panel, stretch = 0)

        # Adding the main widget
        if location is Locations.RESERVE:

            from serverWidget import ServerWidget
            self.main_widget = ServerWidget()
            layout.addWidget(self.main_widget, stretch = 1)

        elif location is Locations.BAR:

            from clientWidget import ClientWidget
            self.main_widget = ClientWidget()
            layout.addWidget(self.main_widget, stretch = 1)

        elif location is Locations.RESTAL:

            from restalWidget import RestalWidget
            self.main_widget = RestalWidget()
            layout.addWidget(self.main_widget, stretch = 1)

        elif location is Locations.CDF:

            from cdfWidget import cdfWidget
            self.main_widget = cdfWidget()
            self.__app.send_champagne_cdf.connect(self.main_widget.setValues)
            layout.addWidget(self.main_widget, stretch = 3)
            #self.cdfWidget.setValues.connect

        else:  # If place is CDF or Unknown
            pass

        # Adding the right panel (chat) for everyone
        self.chat_panel = ChatPanel()
        layout.addWidget(self.chat_panel, stretch = 2)

        # Setting layout on the widget
        widget.setLayout(layout)

        # Attaching the widget to the main window
        self.setCentralWidget(widget)

        # Set window to maximized
        self.showMaximized()

        # Showing the window
        self.show()

    def closeEvent(self, event):
        """Overridden closeEvent method."""

        # Ignore the signal sent when clicking the closing button
        # event.ignore() # No

        # Open the confirmation dialog
        # Create the message box
        exit_box = QMessageBox()

        exit_box.setWindowTitle("Quitter ?")
        exit_box.setIcon(QMessageBox.Question)
        exit_box.setText("Voulez-vous vraiment quitter ?")

        exit_box.addButton(QPushButton('Oui'), QMessageBox.YesRole)
        exit_box.addButton(QPushButton('Non'), QMessageBox.NoRole)

        # If yes is chosen, then exit the app
        if not exit_box.exec_():  # Don't know why 'yes' and 'no' are inverted
            # qApp.exit()
            # sys.exit(qApp.exec_())
            # sys.exit() # No
            self.quit_app.emit()
            event.accept()
        else:
            event.ignore()

    def __export(self):
        """Method used to export (save) the DB in excel format."""

        # Open the file dialog window
        name = QFileDialog.getSaveFileName(self, "Exporter", "fignos.xls", "Classeurs Excel (*.xls, *.xlsx)")[0]
        # Arg 0 is the path to the file and 1 is the type of file.

        # Emit the export signal
        self.export_db.emit(name)

    def __show_preferences_dialog(self):
        preferences = PreferencesDialog()

        # Executing
        preferences.exec_()
        
    
    def __show_information_dialog(self):
        """Method used to display all the information related to connections"""

        # It is no good practice but I don't have time to correct that
        def test(x):
            d = InformationDialog(x)
            d.exec_()

        self.__app.open_connection_dialog.connect(test)
        self.request_connection_infos.emit()
        
    def __show_connection_dialog(self, location):
        """Method used to setup the app."""
        # Renommer tous les signaux preferences par connection
        
        preferences = ConnectionDialog(location)
        # Handling connection signals
        self.__app.fill_preferences.connect(preferences.fill_values)
        self.ask_preferences.emit()
        self.__app.send_connection_infos.connect(preferences.set_ips)
        self.get_connection_infos.emit()
        preferences.connectParameters.connect(lambda x: print("Preferences dialog returned : '{}'.".format(x)))
        preferences.connectParameters.connect(self.set_connection_infos.emit)
        self.__app.connection_established.connect(preferences.validate_connection_infos)
        # Handling bar names signals
        self.__app.connection_established.connect(self.get_bar_names.emit)  # Asking for bar names

        self.__app.send_bar_names.connect(preferences.set_names)
        preferences.barParameters.connect(lambda x: print("Preferences dialog returned :'{}'.".format(x)))
        preferences.barParameters.connect(lambda x: self.set_bar_name.emit(x))
        preferences.barParameters.connect(self.__setBar)
        self.__app.name_set.connect(preferences.validate_bar_name)

        # Executing
        preferences.exec_()

    def __setBar(self, bar):
        self.bar = bar
        print("Bar name set to '{}'".format(bar))

    def __show_help_dialog(self):
        """Method showing a 'Help' frame."""

        message = "Le paramétrage passe par le menu des préférences (Editer > Préférences) :\n\n"
        message += "1) Renseigner à quelle IP se connecter sur quel port.\n"
        message += "2) Choisir ensuite le nom du bar.\n"
        message += "    (Si celui-ci n'existe pas, le créer.)"

        box = QMessageBox()
        box.setIcon(QMessageBox.Information)
        box.setText("Pikal thuysse")
        box.setInformativeText(message)
        box.setWindowTitle("Aide")
        box.exec_()

    def __show_about_dialog(self):
        """Method showing a 'About' frame."""

        message = "Logiciel reliant les différentes entités du Grand Gala des Fignos, "
        message += "tels que les bars, la reserve, la Restal, et le CDF pour faciliter "
        message += "le réapprovisionnement et le décompte des boissons."

        box = QMessageBox()
        box.setIcon(QMessageBox.Information)
        box.setText("    Usiné par les T&lek's 216 et 217 et .18   ")
        box.setInformativeText(message)
        box.setWindowTitle("À propos")
        box.exec_()

    def open_dialog(self, title, message, type="info"):
        """Method opening a dialog."""

        box = QMessageBox(self)
        box.setText("    " + title + "    ")
        box.setInformativeText(message)

        if type == "question":
            box.setIcon(QMessageBox.Question)
            box.setWindowTitle("Question")
        elif type == "error":
            box.setIcon(QMessageBox.Critical)
            box.setWindowTitle("Erreur critique")
        elif type == "warning":
            box.setIcon(QMessageBox.Warning)
            box.setWindowTitle("Erreur")
        else:
            box.setIcon(QMessageBox.Information)
            box.setWindowTitle("Information")

        box.exec_()

    def set_drinks(self, drinks, is_restal=False):
        """Method setting the drinks for display."""

        if self.__location == Locations.BAR:
            for k, d in drinks.items():
                self.__drinks[k] = d
            for k, n in drinks.items():
                button = self.main_widget.buttons_dict[k]
                button.setText(k + '\n' + n)

                # Setting the buttons color
                if not is_restal:
                    color = "red"
                else:
                    color = "blue"
                button.setStyleSheet("background-color: {}".format(color))

                # Setting if button is restal
                button.is_restal = is_restal

        else:
            print('This window does not have the UI elements required to set drinks. It is not a pian window.')

    def add_order(self, id, drink, quantity, bar=None):
        """Method called to add a confirmation of sale."""
        if self.__location == Locations.BAR:  # The names are stored in the window for the client and not the server
            try:
                drink = self.__drinks[drink]
            except KeyError:
                drink = "Boisson inconnue"
                print("Drink '{}' is not sold in this bar".format(drink))
        self.orders_panel.add_order_widget((id, drink, quantity, bar))

    def remove_cancelled_order(self, id):
        """Method called to remove a cancelled order from the stack."""
        print("Cancelling order '{}'".format(id))
        self.orders_panel.remove_order_widget(id)

    def add_refuel_notif(self, key, quantity):
        """Method adding a refuel notification for the given key."""
        try:
            drink = self.__drinks[key]
        except KeyError:
            drink = "Boisson inconnue"
            print("Drink '{}' is not sold in this bar".format(drink))
        self.main_widget.delivery(drink, quantity)

    def remove_refuel_notif(self, id_refuel):
        """Method removing a refuel notif by its id."""
        self.main_widget.del_delivery(id_refuel)

    def confirm_refuel_complete(self, drink, quantity, id_refuel):
        """Method called to confirm the refuel of a drink."""
        key = ""
        for k, d in self.__drinks.items():
            if d == drink:
                key = k
                break
        if key:
            self.refuel_completed.emit(key, quantity, id_refuel)
        else:
            print("Unable to relay confirmation because drink '{}' could not be identified".format(drink))

    def __add_restal_order(self, bar, food, quantity):
        """Method called to add a new order for the restal."""
        self.main_widget.add_order(bar, food, quantity)
