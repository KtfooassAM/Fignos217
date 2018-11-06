"""Script defining the server socket."""

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtNetwork import QTcpServer, QNetworkInterface, QHostAddress


class ServerSocket(QObject):
    """Class defining a socket for the server."""

    listening = pyqtSignal(tuple)
    message_received = pyqtSignal(tuple)
    client_disconnected = pyqtSignal(str)

    def __init__(self):
        """Constructor."""
        QObject.__init__(self)

        self.__tcpServer = QTcpServer()

        self.__active_sockets = []

        self.__tcpServer.newConnection.connect(self.__new_connection)

    def __new_connection(self):
        """Method handling a new connection to the server."""
        # Connecting the new client
        client = self.__tcpServer.nextPendingConnection()
        client.readyRead.connect(self.read_message)
        client.disconnected.connect(self.__find_disconnected_client)
        client.disconnected.connect(client.deleteLater)  # Not sure
        self.__active_sockets.append(client)  # Hyper important !!!
        print("A new client connected from address '{}'.".format(client.peerAddress().toString()))

    def __find_disconnected_client(self):
        """Method trying to find the disconnected client."""
        self.client_disconnected.emit(self.sender().localAddress().toString())

        self.__active_sockets = []
        for socket in self.__tcpServer.children()[1:]:
            if int(socket.socketDescriptor()) <= 10000:  # Socket is active
                self.__active_sockets.append(socket)

    def get_available_ips(self):
        """Method returning the list of available ips."""
        return QNetworkInterface.allAddresses()

    def listen(self, host=None, port=3000):
        """Method making the server listening to a given address."""
        # If no address was specified: trying to give the best one
        if host is None:
            for ip in self.get_available_ips():
                if ip != QHostAddress.LocalHost and ip.toIPv4Address():
                    host = ip
            if host is None:  # No suitable address was found
                host = QHostAddress.LocalHost
        # The address was given as string
        if type(host) == str:
            host = QHostAddress(host)
        # For printing...
        address = "{}:{}".format(host.toString(), port)
        # Launching server
        if not self.__tcpServer.listen(host, port):
            self.__tcpServer.close()
            print("Unable to listen on address '{}': {}.".format(address, self.__tcpServer.errorString()))
            raise ConnectionError(self.__tcpServer.errorString())
        else:
            print("Server is listening on address '{}'.".format(address))
            self.listening.emit((host, port))

    def read_message(self):
        """Method handling the messages."""
        for socket in self.__active_sockets:
            instr = socket.readAll()
            message = str(instr, encoding="utf8")
            if message:
                self.message_received.emit((message, socket))

    def __send_msg(self, message, socket):
        """Method effectively sending a message."""
        socket.write(bytes(message, encoding="utf8"))
        socket.flush()

    def send_message(self, message, recipient=None):
        """Method used to send a message to the clients."""
        if recipient:  # A single recipient was provided
            if type(recipient) is not str:  # Given socket directly
                self.__send_msg(message, recipient)
            else:  # Given ip address
                for socket in self.__active_sockets:
                    if socket.peerAddress().toString() == recipient:
                        self.__send_msg(message, socket)
        else:  # Send for everyone
            for socket in self.__active_sockets:
                self.__send_msg(message, socket)

            # block = QByteArray()
            # out = QDataStream(block, QIODevice.ReadWrite)
            # out.setVersion(QDataStream.Qt_5_0)
            # out.writeUInt16(0)
            # message = bytes(message, encoding="utf8")
            # out.writeString(message)
            # out.device().seek(0)
            # out.writeUInt16(block.size() - 2)
            # socket.write(block)

    def get_address(self):
        """Method returning the adress."""
        return self.__tcpServer.serverAddress()

    def get_port(self):
        """Method returning the port."""
        return self.__tcpServer.serverPort()


if __name__ == "__main__":
    # Importing modules used to run the app
    from PyQt5.QtWidgets import QApplication
    import sys

    # Instantiating the objects
    app = QApplication(sys.argv)

    server = ServerSocket()
    server.message_received.connect(lambda x: print(x))
    server.client_disconnected.connect(lambda x: print("Client '{}' disconnected".format(x)))
    # print([a.toString() for a in server.get_available_ips()])
    # ip = input('Enter one of the previous ips : ')
    server.listen()

    # Launching the app
    sys.exit(app.exec_())
