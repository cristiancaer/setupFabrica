import numpy as np
import cv2
from PyQt5.QtWidgets import QInputDialog,QApplication, QDialog, QGraphicsView,QGraphicsScene,QGraphicsPixmapItem
from PyQt5.QtCore import QPointF, QRectF,pyqtSlot
from PyQt5.QtGui import QPen, QBrush,QTransform,QPolygonF,QPainter, QPixmap,QImage
class ImShowWidget(QGraphicsView):
    def __init__(self):
        QGraphicsView.__init__(self)
        self.setSceneRect(QRectF())
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.img=np.zeros((480,640,3),dtype=np.uint8)
     # limpiar canvas
    def clear(self):
        self.img=np.zeros((480,640,3),dtype=np.uint8)
        self.scene.clear()
        self.update_image(self.img)
    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        self.img=cv_img.copy()
        self.scene.clear()
        pixmap = self.convert_cv_qt(cv_img)
        self.scene.addPixmap(pixmap)
        self.setScene(self.scene)
     
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = QPixmap(convert_to_Qt_format)
        return p
    
class drawInCV2:
    def __init__(self) -> None:
        self.color = (0, 255, 0)
        self.maskFondo=np.zeros((480,640),dtype=np.uint8)
        # Line thickness of 9 px
        self.thickness = 9
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.fontScale = 1
    def line(self,img:np.ndarray,ptIni:tuple,ptFin:tuple,color=None)-> np.ndarray:
        if not color:
            color=self.color
        return cv2.line(img, ptIni, ptFin, color, self.thickness)
    def text(self,img:np.ndarray,text:str,pt:tuple)-> np.ndarray:
        return  cv2.putText(img,text,pt,self.font,self.fontScale,self.color,3,cv2.LINE_AA)
    def toUint8(self,img):
        img=255*(img-img.min())/(img.max()-img.min())
        img=np.array(img,dtype=np.uint8)
        img= cv2.applyColorMap(img, cv2.COLORMAP_JET)
        return img

