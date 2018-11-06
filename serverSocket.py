"""Script defining a server socket."""

from PyQt5.QtNetwork import (QHostAddress, QNetworkConfiguration,
                             QNetworkConfigurationManager, QNetworkInterface, QNetworkSession,
                             QTcpServer)
from PyQt5.QtCore import QByteArray, QDataStream, QIODevice, QSettings, pyqtSignal


class ServerSocket:
    __active_socket=[]
    
    def __init__(self):
        self.__tcpServer = None
        self.__networkSession = None

        self.connections = []
        self.connected_clients_list = []

        self.event = Event()

        manager = QNetworkConfigurationManager()
        if manager.capabilities() & QNetworkConfigurationManager.NetworkSessionRequired:
            settings = QSettings(QSettings.UserScope, 'QtProject')
            settings.beginGroup('QtNetwork')
            id_ = settings.value('DefaultNetworkConfiguration', '')
            settings.endGroup()

            config = manager.configurationFromIdentifier(id_)
            if config.state() & QNetworkConfiguration.Discovered == 0:
                config = manager.defaultConfiguration()

            self.__networkSession = QNetworkSession(config, self)
            self.__networkSession.opened.connect(self.__session_opened)

            self.__networkSession.open()
        else:
            self.__session_opened()
        self.__tcpServer.newConnection.connect(self.__add_connection)

    def __session_opened(self):
        if self.__networkSession is not None:
            config = self.__networkSession.configuration()

            if config.type() == QNetworkConfiguration.UserChoice:
                id_ = self.__networkSession.sessionProperty('UserChoiceConfiguration')
            else:
                id_ = config.identifier()

            settings = QSettings(QSettings.UserScope, 'QtProject')
            settings.beginGroup('QtNetwork')
            settings.setValue('DefaultNetworkConfiguration', id_)
            settings.endGroup()

        self.__tcpServer = QTcpServer()
        PORT = 8000
        address = QHostAddress(QHostAddress.LocalHost)
        if not self.__tcpServer.listen(address, PORT):
            print("Unable to start the server: %s." % self.__tcpServer.errorString())
            self.__tcpServer.close()
            raise ConnectionError(self.__tcpServer.errorString())
        else:
            print('listening')

        for ipAddress in QNetworkInterface.allAddresses():
            if ipAddress != QHostAddress.LocalHost and ipAddress.toIPv4Address() != 0:
                break
        else:
            ipAddress = QHostAddress(QHostAddress.LocalHost)
        self.ipAddress = ipAddress.toString()
        self.port = self.__tcpServer.serverPort()

        print("The server is running on\n\nIP: %s\nport %d\n\n" % (address.toString(), PORT))
        print(self.__tcpServer.socketDescriptor())

    def __add_connection(self):
        self.__active_socket=[]
        client_connection = self.__tcpServer.nextPendingConnection()
        socket_list = self.__tcpServer.children()[1:]
        for socket in socket_list :
            id_socket=int(socket.socketDescriptor())
            if id_socket<=10000:
                #only sockets with id<10000 are active
                self.__active_socket.append((socket, id_socket))
        print(self.__active_socket)
        print('client', int(client_connection.socketDescriptor()))
        #add a way to sort __active_socket
    
    def send_message(self, message="Goodbye!", recipient="all"):
        print("sending..")
        # Get a QTcpSocket from the QTcpServer
        client_connection = self.__add_connection()[-1]
        print(int(client_connection.socketDescriptor()))        
        #client_connection = self.__tcpServer.nextPendingConnection()
        # instantiate a QByteArray
        block = QByteArray()
        # QDataStream class provides serialization of binary data to a QIODevice
        out = QDataStream(block, QIODevice.ReadWrite)
        # We are using PyQt5 so set the QDataStream version accordingly.
        out.setVersion(QDataStream.Qt_5_0)
        out.writeUInt16(0)
        # this is the message we will send it could come from a widget.
        # get a byte array of the message encoded appropriately.
        message = bytes(message, encoding='utf8')
        # now use the QDataStream and write the byte array to it.
        out.writeString(message)
        out.device().seek(0)
        out.writeUInt16(block.size() - 2)
        clientConnection.write(block)

    def read_message(self):
        clientConnection = self.__tcpServer.nextPendingConnection()
        clientConnection.waitForReadyRead()
        # read incomming data
        instr = clientConnection.readAll()
        # in this case we print to the terminal could update text of a widget if we wanted.
        print(str(instr, encoding='utf8'))

class Event:
    transaction = pyqtSignal()
    cancel = pyqtSignal()

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    server = ServerSocket()
    sys.exit(app.exec_())
