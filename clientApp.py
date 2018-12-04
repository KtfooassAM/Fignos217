"""Script defining the client app, inherited from the base App class."""

from PyQt5.QtCore import (QIODevice, pyqtSignal)
from PyQt5.QtNetwork import (QAbstractSocket, QTcpSocket)

from app import App
from window import Window, Locations

HOST, PORT = 'localhost', 3000


class ClientApp(App):
    """Class defining all methods necessary to the client app."""

    refuelling_in_progress = pyqtSignal(str, int)

    def __init__(self):
        """Constructor."""
        self.__tcpSocket = QTcpSocket()
        # print("client descriptor", int(self.__tcpSocket.socketDescriptor()))
        # print("set descriptor ?",self.__tcpSocket.setSocketDescriptor(122315546))  # Why?? Just Why?
        # self.blockSize = 0  # ?

        self.__drinks = {}
        for k in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', '/', '*', '-', '+']:
            self.__drinks[k] = None

        App.__init__(self)  # Used at the end because it launches the app

    def _open_window(self):
        """Method replacing the App one's to launch the user interface."""
        # Creating the window
        self._window = Window(self, Locations.BAR)

    def _connect_signals(self):
        """Method used to connect the signals."""

        App._connect_signals(self)

        # Connecting socket signals
        self.__tcpSocket.error.connect(self.__display_error)
        self.__tcpSocket.readyRead.connect(self.__read_message)

        # Connecting the socket when requested
        self._window.set_connection_infos.connect(lambda x: self.connect_to_server(*x))

        # Connecting the bar names request
        self._window.get_bar_names.connect(lambda: self.encode_message(action="LA"))

        # Setting the bar name when requested
        self._window.set_bar_name.connect(self.__set_name)

        # Connecting the preferences
        self._window.ask_preferences.connect(
            lambda: self.fill_preferences.emit((self.__tcpSocket.peerAddress().toString(), self.__tcpSocket.peerPort()),
                                               self._name))

        # Connecting the send message signal
        self._window.send_message.connect(lambda x: self.encode_message(action="ME", message=x))

        # Connecting the drink orders
        self._window.order_drink.connect(self.__order_drink)

        # Connecting the cancellation of an order
        self._window.cancel_order.connect(lambda x: print("Cancelling sale '{}'".format(x)))
        self._window.cancel_order.connect(lambda x: self.encode_message(action="AR", sale_id=x))

        # Connecting the refuel complete signal
        self._window.refuel_completed.connect(lambda d, q, i: self.encode_message(action="RE", key=d, quantity=q, id=i))

        # Connecting for the connection dialog
        self._window.request_connection_infos.connect(
            lambda: self.open_connection_dialog.emit([[self.__tcpSocket.peerAddress().toString(),
                                                      self.__tcpSocket.state() == QAbstractSocket.ConnectedState]]))

    def __display_error(self, socket_error):
        """Method displaying the error message from the socket."""
        if socket_error == QAbstractSocket.RemoteHostClosedError:
            self._window.open_dialog("Serveur déconnecté", "Le serveur s'est déconnecté !")
            # Add signal to be emitted that pops up a dialog window
        elif socket_error == QAbstractSocket.OperationError:  # Raised when the socket already is connected
            pass
        else:
            self._window.open_dialog("Erreur de connection",
                                     "L'erreur suivante est survenue : {}.".format(self.__tcpSocket.errorString()),
                                     type="error")

    def __read_message(self):
        """Method reading the messages received by the socket."""
        # instr = QDataStream(self.__tcpSocket)
        # instr.setVersion(QDataStream.Qt_5_0)
        # if self.blockSize == 0:
        #     if self.__tcpSocket.bytesAvailable() < 2:
        #         return
        #     self.blockSize = instr.readUInt16()
        # if self.__tcpSocket.bytesAvailable() < self.blockSize:
        #     return
        # # Print response to terminal, we could use it anywhere else we wanted.
        # message = str(instr.readString(), encoding='utf8')
        # print("New message received : '{}'.".format(message))
        # self.decode_message(message)

        instr = self.__tcpSocket.readAll()
        message = str(instr, encoding="utf8")
        self.decode_message(message)

    def __order_drink(self, key, is_restal):
        """Method handling the order of drink or food."""
        if not is_restal:
            self.encode_message(action="VE", drink_id=self.__drinks[key][0], quantity=self.__drinks[key][1])
        else:
            self.encode_message(action="RS", food_id=self.__drinks[key][0], quantity=self.__drinks[key][1])

    def __set_name(self, name):
        """Method called to set the client's name."""
        self._name = name
        self._window.chat_panel.place_name = name
        self.encode_message(action="NO", selected_name=name)

    def connect_to_server(self, host=HOST, port=PORT):
        """Method connecting the client to a given server."""
        # HOST = server.ipAddress
        # PORT = int(server.port)
        # self.tcpSocket.disconnectFromHost()
        # self.tcpSocket.waitForDisconnected ()
        # print(HOST, PORT)
        # self.__tcpSocket.connectToHost(host, port, QIODevice.ReadWrite)
        self.__tcpSocket.connectToHost(host, port, QIODevice.ReadWrite)
        if self.__tcpSocket.waitForConnected(5000):
            print('Client connected to server.')
            self.connection_established.emit((host, port))
        else:
            self._window.open_dialog("Impossible de se connecter au serveur !",
                                     "Vérifiez que les paramètres que vous avez entré sont corrects et que le serveur est en fonctionnement.",
                                     type="warning")
            print('Unable to connect...')

    def send_message(self, message):
        """Method sending a message to the connected server."""
        self.__tcpSocket.write(message.encode('utf8'))

    def decode_message(self, message):
        """Method decoding the message received from the server."""

        print("Decoding message '{}'".format(message))

        message_split = message[1:-1].split('||')

        if len(message_split) > 1:  # Several messages are queued
            for m in message_split:
                self.decode_message('|' + m + '|')
            return
        else:
            message = message_split[0]

        message_split = message.split('|')

        if message_split[0] == 'LA':

            list_bars = message_split[1].split(',')
            self.send_bar_names.emit(list_bars)  # Sending the list to the UI

        elif message_split[0] == 'AE':

            self._window.remove_cancelled_order(message_split[1])

        elif message_split[0] == 'ME':

            print("New message received : '{}'".format(message))

            if len(message_split) == 3:  # Author was found
                infos = (message_split[2], message_split[1])
            elif len(message_split) == 2:  # No author
                infos = (message_split[1],)
            try:
                self.message_received.emit(infos)
            except UnboundLocalError:
                self._window.open_dialog("Message de chat incompréhensible",
                                         "Le message de chat suivant n'a pas pu être décodé : {}".format(message),
                                         type="warning")

        elif message_split[0] == 'LO':  # Message is respecting convention 'LO|code1:drink1,code2:drink2...'

            self.name_set.emit()  # Warning the UI about the name being set

            if message_split[1]:
                tuples = message_split[1].split(',')
                drinks = [tuple(t.split(':')) for t in tuples]
                print('drinks', drinks)
                drinkss = []
                for j, (i, d, b) in enumerate(drinks):
                    drinkss.append((i, d, 1))
                    if b == '1':
                        drinkss.append((i, "Bouteille\n" + d, 7))
                names = {}
                if len(drinkss) <= 15:  # We got enough keys
                    for k, d in zip(self.__drinks.keys(), drinkss):
                        self.__drinks[k] = (d[0], d[2])
                        names[k] = d[1]
                else:
                    print("Unable to select keys for drinks '{}': too many drinks ({})".format(drinkss, len(drinks)))
                    self._window.open_dialog("Trop de boissons.",
                                             "Impossible de sélectionner des clés pour les boissons '{}': trop de boissons ({})".format(
                                                 drinkss, len(drinkss)), type="error")
                self._window.set_drinks(names)

            else:
                self._window.open_dialog("Aucune boissons associées à ce bar.",
                                         "Aucune boisson n'a été trouvée associée à ce bar. Essayez un autre bar ou contactez vos ZiT&lek'ss.")

        elif message_split[0] == 'LE':

            if message_split[1]:
                tuples = message_split[1].split(',')
                food = [tuple(t.split(':')) for t in tuples]
                available_keys = []
                for k, d in self.__drinks.items():
                    if not d:
                        available_keys.append(k)
                names = {}
                if len(food) <= len(available_keys):  # We got enough keys
                    for k, d in zip(available_keys, food):
                        self.__drinks[k] = (d[0], 1)
                        names[k] = d[1]
                else:
                    print("Unable to select keys for food '{}': too many items ({})".format(food, len(food)))
                    self._window.open_dialog("Trop de plats.",
                                             "Impossible de sélectionner des clés pour les plats '{}': plats trop nombreux ({})".format(
                                                 food, len(food)), type="error")
                self._window.set_drinks(names, is_restal=True)

            else:

                self._window.open_dialog("Aucune boissons associées à ce bar.",
                                         "Aucune boisson n'a été trouvée associée à ce bar. Essayez un autre bar ou contactez vos ZiT&lek'ss.")

        elif message_split[0] == "RE":

            id_refuel = message_split[1]
            self._window.remove_refuel_notif(id_refuel)

        elif message_split[0] == "RT":

            key = ""
            for k, d, in self.__drinks.items():
                if d[0] == message_split[1]:
                    key = k
                    break
            self.refuelling_in_progress.emit(key, int(message_split[2]))

        elif message_split[0] == "VE":  # Confirmation of sale

            try:
                id, drink, quantity = message[3:].split('|')
            except ValueError:
                print("Unable to add order from message '{}'".format(message))
            else:
                key = ""
                for k, d, in self.__drinks.items():
                    if d[0] == drink:
                        key = k
                        break
                self._window.add_order(id, key, quantity)

        elif message_split[0] == "CH":

            pass

        else:

            self._window.open_dialog("Message du serveur incompréhensible",
                                     "Le message suivant n'a pas pu être décodé : {}".format(message), type="warning")
            print("Error : message '{}' could not be decoded".format(message))

    def encode_message(self, **kwargs):
        """Method encoding a message to be sent to the server.
        :param kwargs: key 'action' related to agreed values: NO - VE - AR - ME - DE - RE - RS - LA
                       with following keys 'action' :
                            NO : use key 'selected_name' to send the bar's selected name
                            VE : use key 'drink_id' and 'quantity'
                            AR : use key 'sale_id'
                            ME : use key 'message'
                            DE : use no key
                            RE : use key 'drink'
                            RS : no effect for the moment
                            LA : no key
        """
        if kwargs["action"] == "NO":

            self.send_message("|%s|%s|" % (kwargs["action"], kwargs["selected_name"]))

        elif kwargs["action"] == "VE":

            if kwargs["drink_id"]:
                self.send_message("|VE|{}|{}|".format(kwargs["drink_id"], kwargs["quantity"]))
            else:
                print("Unknown drink")

        elif kwargs["action"] == "AR":

            if kwargs["sale_id"]:
                self.send_message("|%s|%s|" % (kwargs["action"], kwargs["sale_id"]))
            else:
                print("You must specify a sale to be cancelled.")

        elif kwargs["action"] == "ME":

            print("Sending tchat message '{}'".format(kwargs['message']))
            self.send_message("|%s|%s|" % (kwargs["action"], kwargs["message"]))

        elif kwargs["action"] == "RE":

            try:
                drink_id = self.__drinks[kwargs["key"]][0]
            except KeyError:
                print("Unable to send confirmation of refuel because drink at key '{}' could not be identified.".format(
                    kwargs["key"]))
            else:
                self.send_message("|RE|{}|{}|{}|".format(drink_id, kwargs['quantity'], kwargs['id']))

        elif kwargs["action"] == "RS":

            print("Asking server for food '{}'".format(kwargs['food_id']))
            self.send_message("|RS|{}|{}|".format(kwargs['food_id'], kwargs['quantity']))

        elif kwargs["action"] == "LA":

            self.send_message("|LA|")

        else:

            self._window.open_dialog("Impossible d'envoyer un message",
                                     "Le message suivant n'a pas pu être envoyé car mal encodé : {}".format(kwargs),
                                     type="warning")
            print("Error during encoding with arguments : %s" % kwargs)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import *
    import sys

    app = QApplication(sys.argv)
    
    file = QFile("style.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())

    client = ClientApp()
    sys.exit(app.exec_())
