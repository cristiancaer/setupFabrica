import sys# las sisguientes dos lineas ayudan a ubicar al archivo calibracion.py

import sys
sys.path.append('/home/estufab4/Desktop/flujo de bagazo/codigo/solo_python/interfaz/setupFabrica2/')


import sys
from view.imshow import ImShowWidget
from model.model import Polyn, Line
import numpy as np
from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import  QApplication, QDialog,QGridLayout,QPushButton

class canvas(ImShowWidget):
    def __init__(self):
        super().__init__()
        self.listLines=[]
        self.listPol=[]
        self.drawing=False
        self.listBuffer=None
    def idle(self):
        return None
    def makeLine(self)->None:
        self.drawing=True
        self.listLines.append(Line())
        self.listBuffer=self.listLines
   
    def makePoly(self,nsegments:int)-> None:
        self.drawing=True
        self.listPol.append(Polyn(nsegments))
        self.listBuffer=self.listPol
    def mousePressEvent(self,event):
        e = QPointF(self.mapToScene(event.pos()))
        self.getStroke(e)

    def getStroke(self,e):
        
        if self.drawing:
            if not self.listBuffer[-1].isComplete:
                self.listBuffer[-1].addPt([e.x(),e.y()])
                if self.listBuffer[-1].isComplete:
                    self.listBuffer=None
                    self.drawing=False
                    for l in self.listLines:
                        print(l)
                    for p in self.listPol:
                        print(p)

class Dialogo(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.resize(500, 500)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.paint = canvas()
        
        self.btnDrawLine = QPushButton("Dibujar V")
  
        self.btn_clear = QPushButton("Clear")

        self.layout.addWidget(self.btnDrawLine)

        self.layout.addWidget(self.btn_clear)
        self.layout.addWidget(self.paint)
        

        self.btnDefault = "background-color: grey; border: 0; padding: 10px"
        self.btnActive = "background-color: orange; border: 0; padding: 10px"
        
        self.btnDrawLine.setStyleSheet(self.btnDefault)
        self.btn_clear.setStyleSheet(self.btnDefault)
        self.btnDrawLine.clicked.connect(self.paint.makeLine)

        self.btn_clear.clicked.connect(self.isClear)

    def isClear(self):
        self.paint.clear()
        self.btn_clear.setStyleSheet(self.btnActive)
        
        self.btn_clear.setStyleSheet(self.btnDefault)

if __name__=="__main__":
    app=QApplication(sys.argv)
    prueba=Dialogo()
    prueba.show()
    app.exec_()
