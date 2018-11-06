"""Script defining the right part of the common UI, ie the chat."""

from PyQt5.QtCore import QTime, Qt, pyqtSignal
from PyQt5.QtWidgets import *

from verticalScroll import VerticalScroll


## ajouter un bouton qui change la couleur du chat
## ajouter en haut un qlabel pour un message important, qu'on pourra utiliser avec un boutton ou avec une commande en debut de message

class ChatPanel(QWidget):
    """Chat panel to be added on the right side of the windows.
    Add message to chat panel : ChatPanel.add_message("message")"""

    send_message = pyqtSignal(str)

    def __init__(self):
        """Constructor"""
        QWidget.__init__(self)

        self.place_name = None

        self.__init_UI()

    def __init_UI(self):
        """Method setting up the UI for the ChatPanel class"""

        # Creating of the main layout of the chat
        main_layout = QVBoxLayout()

        # Creating the vertical scroll area to display messages
        self.scroll = VerticalScroll(top_stretch=True)

        # Creating the layout to send messages
        new_message_layout = QHBoxLayout()

        # Creating field to compose messages
        self.new_message_entry = QLineEdit('', self)
        self.new_message_entry.setPlaceholderText("Entrez votre message ici :")

        # Creating the 'send' button
        send_message_button = QPushButton("Envoyer", self)
        send_message_button.clicked.connect(self.__send_message)

        # Adding the widgets to the bottom layout
        new_message_layout.addWidget(self.new_message_entry)
        new_message_layout.addWidget(send_message_button)

        # Adding everything to the main layout
        main_layout.addWidget(QLabel("Discussion"))
        main_layout.addWidget(self.scroll)
        main_layout.addLayout(new_message_layout)

        # Ajout du widget principal au chat
        self.setLayout(main_layout)

    def __send_message(self):
        """Method triggered by the 'Send' button sending the message."""

        # Getting the message to be sent
        message = self.new_message_entry.text()

        if message:
            # Sending the message
            self.send_message.emit(message)

            # Clearing the entry for another message to be sent
            self.new_message_entry.clear()

    def keyPressEvent(self, event):
        """Method handling the key press events."""

        # Key pressed was Enter (both of them) : sending the message
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.__send_message()

    def add_message(self, infos):
        """Method called to add a message to the list."""
        # Rewriting message
        if len(infos) == 2:  # With author
            message = QTime.currentTime().toString(Qt.DefaultLocaleLongDate)[:-6] + ' - ' + infos[1].capitalize() + ' : ' + infos[0]
        elif len(infos) == 1:
            message = QTime.currentTime().toString(Qt.DefaultLocaleLongDate)[:-6] + ' - ' + infos[0]
        else:
            message = "### ERROR ###"
        # Adding the message to the vertical scroll
        label = QLabel(message)
        if len(infos) == 2:  # With author
            if self.place_name == infos[1]:
                label.setStyleSheet('color: black')
            else:
                label.setStyleSheet('color: red')
        self.scroll.add_widget(label)

        # Scrolling to the bottom (to the last label added)
        # print(self.scroll.verticalScrollBar().maximum())
        self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum())


if __name__ == '__main__':
    # Importing modules used to run the app
    from PyQt5.QtWidgets import QApplication
    import sys

    # Instantiating the objects
    app = QApplication(sys.argv)

    chat_panel = ChatPanel()
    chat_panel.show()

    # Launching the app
    sys.exit(app.exec_())

# TO-DO:
#     Add reception of messages
#     Add sending of messages through socket
#     Prevent the chat to get the cursor by default
#     Clarify architecture : too many items (layout and widgets)
#     Add scrollabel object to simplify architecture

# BUGS
#	Scrolling to bottom doesn't work completely : one element missing
