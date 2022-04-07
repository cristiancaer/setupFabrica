import numpy as np
import cv2
class ImgInfo:
    def __init__(self,img:np.ndarray,text:dict,objets:dict) -> None:
        self.img=img
        self.text=text
    def getImg(self)-> np.ndarray:
        return self.img
class Polyn:
    def __init__(self,nSegments:int):
        self.n=nSegments
        self.points=np.zeros((self.n,2),dtype=np.int)
        self.status=0
        self.isComplete=False
    def addPt(self,point):
        if not self.isComplete:
            self.points[self.status]=np.array(point)
            self.status+=1
            if self.status==self.n-1:
                self.isComplete=True
    def clear(self):
        self.status=0
        self.points=np.zeros((self.n,2),dtype=np.int)
    def __str__(self) -> str:
        return "nPoints {}: {}".format(len(self.points),self.points)
class Line(Polyn):
    def __init__(self):
        super().__init__(2)
        self.width=50
        self.kernel=9
        self.hight=50
        self.y1=0
        self.y2=480
    def getRoi(self,valueVertical,img):
        
        img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        x0=valueVertical-self.width
        return img[:,x0:valueVertical+self.width],x0
    def getPtsLine(self,roi,x0):
        roi=cv2.blur(roi,(self.kernel,self.kernel))
        roiUP=roi[self.y1:self.hight,:]
        roiDown=roi[self.y2-self.hight:,:]
        histoUP=roiUP.mean(axis=0)

        histoDown=roiDown.mean(axis=0)
        ix1=int(np.where(histoUP==histoUP.max())[0][0])
        
        ix2=int(np.where(histoDown==histoDown.max())[0][0])
        
        return [ix1+x0,ix2+x0]
    def updatePts(self,img):
        meanx=int(self.points.mean(axis=0)[0])   
        roi,x0=self.getRoi(meanx,img)
        [x1,x2]=self.getPtsLine(roi,x0)
        self.points=np.array(([x1,self.y1],[x2,self.y2]))
        del roi
    def ptIni(self):
        return tuple(self.points[0])
    def ptFin(self):
        return tuple(self.points[1])
    def getAngle(self):
        delta=np.diff(self.points,axis=0)[0]
        delta=delta.astype(float)
        if delta[0]==0:
            delta[0]=1E-9
            
        angle=np.arctan(delta[1]/delta[0])*180/np.pi
        return angle