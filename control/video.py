
from PyQt5.QtWidgets import  QApplication
import numpy as np
from PyQt5.QtWidgets import QInputDialog,QApplication, QDialog, QGridLayout, QPushButton
from PyQt5.QtCore import QThread,pyqtSignal
from PyQt5.QtGui import QPen

import cv2


import time

class VideoThread(QThread):
    changeImgRgb= pyqtSignal(np.ndarray)
    changeImgDepth=pyqtSignal(np.ndarray)
    
    def __init__(self,camara):
        super().__init__()
        self._run_flag = True
        self.play=False
        self.camara=camara
    def run(self):
        while self._run_flag:
            if self.play:
                imgRgb=self.camara.getFrame((0))
                imgDepth=self.getDepth()
                imgDepth,imgRgb=self.preprocesar_imgs(imgRgb,imgDepth)
                self.changeImgRgb.emit(imgRgb)
                
                self.changeImgDepth.emit(imgDepth)
            time.sleep(0.01)
                
        # shut down capture system
        self.dev.close()
        openni2.unload()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

            


  
class Dialogo(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.resize(500, 500)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.paint = Paint()
        self.paintDepth=Paint()
        img=cv2.imread("/home/estufab4/Desktop/flujo de bagazo/codigo/solo_python/interfaz/img2.png",cv2.IMREAD_UNCHANGED)
        img=(img/255).astype(np.uint8)
        self.paint.update_image(img)
        # # path="C:/Users/crist/Desktop/Dron7500.avi"
        # self.video=VideoThread()
        # self.video.changeImgRgb.connect(self.paint.update_image)
        # self.video.changeImgDepth.connect(self.paintDepth.update_image)
  
        
        # # start the thread
        # self.video.start()

        # self.paint.imagen("img/flecha.png",0,[0,0])
        self.btnDrawLine = QPushButton("Dibujar V")
  
        self.btn_clear = QPushButton("Clear")

        self.layout.addWidget(self.btnDrawLine)

        self.layout.addWidget(self.btn_clear)
        self.layout.addWidget(self.paint)
        self.layout.addWidget(self.paintDepth)

        self.btnDefault = "background-color: grey; border: 0; padding: 10px"
        self.btnActive = "background-color: orange; border: 0; padding: 10px"
        
        self.btnDrawLine.setStyleSheet(self.btnDefault)
        self.btn_clear.setStyleSheet(self.btnDefault)

        # name, done1=QInputDialog.getText(
        #      self, 'Input Dialog', 'Enter your name:')
        # print(name,done1)
        self.btnDrawLine.clicked.connect(self.isDrawFondo)

        self.btn_clear.clicked.connect(self.isClear)
    def hola(self,lista):
        print("hola:",lista)
    def isDrawV(self):
        self.paint.isLineL=not(self.paint.isLineL)
        if self.paint.isLineL:
            self.btnDrawLine.setStyleSheet(self.btnActive)
        else:
            self.btnDrawLine.setStyleSheet(self.btnDefault)
    def isDrawFondo(self):
        self.paint.isFondo=not(self.paint.isFondo)
        if self.paint.isFondo:
            self.btnDrawLine.setStyleSheet(self.btnActive)
        else:
            self.btnDrawLine.setStyleSheet(self.btnDefault)
            self.paint.addMask()
    def isClear(self):
        self.paint.inicializar()
        self.btn_clear.setStyleSheet(self.btnActive)
        
        self.btn_clear.setStyleSheet(self.btnDefault)

        
if __name__ =="__main__":
    app = QApplication(sys.argv)
    dialogo = Dialogo()
    dialogo.show()
    app.exec_()
