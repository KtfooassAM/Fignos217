"""Script defining the Restal app, inherited from the base App class."""

from PyQt5.QtCore import (QIODevice, pyqtSignal)
from PyQt5.QtNetwork import (QAbstractSocket, QTcpSocket)

from app import App
from window import Window, Locations

HOST, PORT = 'localhost', 3000


class RestalApp(App):
	"""Class defining all methods necessary to the Restal app."""

	send_bar_names = pyqtSignal(list)
	name_set = pyqtSignal()
	add_order = pyqtSignal(str, str, int)

	def __init__(self):
		"""Constructor."""
		self.__tcpSocket = QTcpSocket()

		self.__name = ""
		self.__food = {}

		App.__init__(self)  # Used at the end because it launches the app

	def _open_window(self):
		"""Method replacing the App one's to launch the user interface."""
		# Creating the window
		self._window = Window(self, Locations.RESTAL)

	def _connect_signals(self):
		"""Method used to connect the signals."""

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
											   self.__name))

		# Connecting the send message signal
		self._window.send_message.connect(lambda x: self.encode_message(action="ME", message=x))

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
		#	 if self.__tcpSocket.bytesAvailable() < 2:
		#		 return
		#	 self.blockSize = instr.readUInt16()
		# if self.__tcpSocket.bytesAvailable() < self.blockSize:
		#	 return
		# # Print response to terminal, we could use it anywhere else we wanted.
		# message = str(instr.readString(), encoding='utf8')
		# print("New message received : '{}'.".format(message))
		# self.decode_message(message)

		instr = self.__tcpSocket.readAll()
		message = str(instr, encoding="utf8")
		self.decode_message(message)

	def __set_name(self, name):
		"""Method called to set the client's name."""
		self.__name = name
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

		elif message_split[0] == 'LO':  # Message is '|LO|' so just ignoring it

			self.name_set.emit()  # Warning the UI about the name being set

		elif message_split[0] == "CH":

			pass
		
		elif message_split[0] == 'UR':

			print("New message received : '{}'".format(message))

			if len(message_split) == 3:  # Author was found
				infos = (message_split[2], message_split[1])
			elif len(message_split) == 2:  # No author
				infos = (message_split[1],)
			try:
				self.urgent_message_received.emit(infos)
			except UnboundLocalError:
				self._window.open_dialog("Message de chat incompréhensible",
										 "Le message de chat suivant n'a pas pu être décodé : {}".format(message),
										 type="warning")
			
		elif message_split[0] == "LE":  # Getting the list of products

			if message_split[1]:
				tuples = message_split[1].split(',')
				for t in tuples:
					i, f = t.split(':')
					self.__food[int(i)] = f

		elif message_split[0] == "RS":  # A new order for Restal

			try:
				food = self.__food[int(message_split[2])]
			except KeyError:
				food = "Inconnue"
				print("Unable to get the name of food '{}'".format(message_split[2]))
			print(message_split[1],message_split[3],message_split[2])
			self.add_order.emit(message_split[1], food, int(message_split[3]))

		else:
			self._window.open_dialog("Message du serveur incompréhensible",
									 "Le message suivant n'a pas pu être décodé : {}".format(message), type="warning")
			print("Error : message '{}' could not be decoded".format(message))

	def encode_message(self, **kwargs):
		"""Method encoding a message to be sent to the server."""

		if kwargs["action"] == "NO":

			self.send_message("|%s|%s|" % (kwargs["action"], kwargs["selected_name"]))

		elif kwargs["action"] in ["ME","UR"]:

			self.send_message("|%s|%s|" % (kwargs["action"], kwargs["message"]))

		elif kwargs["action"] == "LA":

			self.send_message("|LA|")

		elif message_split[0] == "CH":

			pass
			
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

	client = RestalApp()
	sys.exit(app.exec_())
