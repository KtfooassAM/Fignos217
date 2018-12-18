from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
import sys
from PyQt5.QtCore import QDate, QTimer, QDateTime, Qt

class cdfWidget(QWidget):

    

    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):   
        
        main_layout = QVBoxLayout(self)
        
        self.setLayout(main_layout)
        
        self.graph_widget = PlotCanvas(self, width=5, height=4)
        main_layout.addWidget(self.graph_widget)

    def setValues(self, data):
        
        self.graph_widget.plot(data)

    def _CDFApp__set_champagne(self, champagne, rooms):
        """Method called to set the champagne's name."""

        self.graph_widget.set_champagne(champagne, rooms)
        
class PlotCanvas(FigureCanvas):
 
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        self.n_champ = 1
        self.x = [""]
        self.rooms = ["","","","",""]
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.initPlot()
 
 
    def initPlot(self):
        n_bar = 5
        
        self.ax = self.figure.add_subplot(111)

        data = np.zeros((n_bar,self.n_champ),int)
        data = data.tolist()
        
        self.plot(data)

    def set_champagne(self, champagne, rooms):
        self.n_champ = len(champagne)
        self.x = champagne
        self.rooms = rooms
        self.initPlot()
         
    def plot(self, data):
        self.ax.clear()
        data = np.array(data)
        dataT = data.transpose()
        
        self.salle1 = self.ax.bar(self.x, data[0], bottom=[sum(dataT[i,:0]) for i in range(self.n_champ)],color = "#8E2562")
        self.salle2 = self.ax.bar(self.x, data[1], bottom=[sum(dataT[i,:1]) for i in range(self.n_champ)],color = "#F29400")
        self.salle3 = self.ax.bar(self.x, data[2], bottom=[sum(dataT[i,:2]) for i in range(self.n_champ)],color = "#55BF35")
        self.salle4 = self.ax.bar(self.x, data[3], bottom=[sum(dataT[i,:3]) for i in range(self.n_champ)],color = "#0000FF")
        self.salle5 = self.ax.bar(self.x, data[4], bottom=[sum(dataT[i,:4]) for i in range(self.n_champ)],color = "#BF3547")

        self.ax.legend((self.salle1[0], self.salle2[0], self.salle3[0], self.salle4[0], self.salle5[0]),
                       self.rooms)        
        self.ax.set_title("Consommation de Champ'ss")
        self.draw()   
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = cdfWidget()
    ex.show()
    sys.exit(app.exec_())
    
