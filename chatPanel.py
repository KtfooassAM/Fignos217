"""Script defining the right part of the common UI, ie the chat."""

from PyQt5.QtCore import QTime, Qt, pyqtSignal
from PyQt5.QtWidgets import *
from random import randint

from verticalScroll import VerticalScroll


## ajouter un bouton qui change la couleur du chat
## ajouter en haut un qlabel pour un message important, qu'on pourra utiliser avec un boutton ou avec une commande en debut de message

class ChatPanel(QWidget):
    """Chat panel to be added on the right side of the windows.
    Add message to chat panel : ChatPanel.add_message("message")"""

    send_message = pyqtSignal(str)
    send_message_urgent = pyqtSignal(str)

    def __init__(self):
        """Constructor"""
        QWidget.__init__(self)

        self.place_name = None

        self.__init_UI()

    def __init_UI(self):
        """Method setting up the UI for the ChatPanel class"""

        # Creating of the main layout of the chat
        main_layout = QVBoxLayout()

        # Creating the message list (Important)
        self.message_list_important = VerticalScroll(top_stretch=True)

        # Creating tje message list (General)
        self.message_list_general = VerticalScroll(top_stretch=True)
        
        # Creating the layout to send messages
        new_message_layout = QHBoxLayout()
                
        # Creating field to compose messages
        self.new_message_entry = QLineEdit('', self)
        self.new_message_entry.setPlaceholderText("Entrez votre message ici :")

        # Creating the 'send' button
        send_message_button = QPushButton("Envoyer", self)
        send_message_button.clicked.connect(self.__send_message)

        # Creating the 'urgent' button
        send_message_button_urgent = QPushButton("Urgent", self)
        send_message_button_urgent.clicked.connect(self.__send_message_urgent)

        # Adding the widgets to the bottom layout
        new_message_layout.addWidget(self.new_message_entry)
        new_message_layout.addWidget(send_message_button)
        new_message_layout.addWidget(send_message_button_urgent)

        # Adding everything to the main layout
        main_layout.addWidget(QLabel("Discussion"))
        main_layout.addWidget(self.message_list_important,stretch = 1)
        main_layout.addWidget(self.message_list_general, stretch = 2)
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

            # Test
            # self.add_message((message,))
            
            


            
    def __send_message_urgent(self):
        """Method triggered by the 'Send Urgent' button sending the message."""

        # Getting the message to be sent
        message = self.new_message_entry.text()

        if message:
            # Sending the message
            self.send_message_urgent.emit(message)

            # Clearing the entry for another message to be sent
            self.new_message_entry.clear()

            # Test
            # self.add_message_urgent((message,))

    def keyPressEvent(self, event):
        """Method handling the key press events. Only for not important messages"""

        # Key pressed was Enter (both of them) : sending the message
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.__send_message()

        # Key pressed was Enter (both of them) : sending the message
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and event.key() == Qt.Key_Shift:
            self.__send_message_urgent()
            
    def add_message(self,msg):
        """Method to add message to the list"""
        # Revoir les formats des messages
        print(msg)
        if len(msg) == 2:
            wid = MessageWidget(msg[0],msg[1])
        elif len(msg) == 1:
            wid = MessageWidget(msg[0],"Inconnu")
        wid.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.message_list_general.add_widget(wid)

        
    def add_message_urgent(self,msg):
        """Method to add message to the list"""
        # Revoir les formats des messages
        print(msg)
        if len(msg) == 2:
            wid = MessageWidget(msg[0],msg[1])
        elif len(msg) == 1:
            wid = MessageWidget(msg[0],"Inconnu")
        wid.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.message_list_important.add_widget(wid)

        # Putting the VerticalScroll downest as possible
        # self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum())

class MessageWidget(QWidget):

    def __init__(self,msg,src):

        QWidget.__init__(self)

        self.message = msg
        self.source = src
        self.hour = QTime.currentTime().toString()

        self.dico_color = {'mexico':"QLabel {color:#8e2562}",
                           'chine':"QLabel {color:#f29400}",
                           'rio':"QLabel {color:#55bf35}",
                           'venise':"QLabel {color:#0000ff}",
                           "K'Ve":"QLabel {color:#bf3547}",
                           'reserve':"QLabel {color:yellow}",
                           'cdf':"QLabel {background-color:pink; color:#875121}",
                           'restal':"QLabel {color:brown}",
                           'Inconnu':"QLabel {color:#ffffff}"}

        self.__init_UI()

    def __init_UI(self):
        
        message_layout = QHBoxLayout()

        sender_name = QLabel(self.hour + " " + self.source + " :")
        if self.source in self.dico_color:
            sender_name.setStyleSheet(self.dico_color[self.source])

        
        message_slot = QLabel(self.message)
        
        message_layout.addWidget(sender_name,stretch=1)
        message_layout.addWidget(message_slot,stretch=3)
        self.setLayout(message_layout) 
        

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    Msg = ChatPanel()
    Msg.show()
    sys.exit(app.exec_())
