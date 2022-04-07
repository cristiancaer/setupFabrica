import queue
from threading import Thread
from time import sleep
import numpy as np
from openni import openni2
from openni import _openni2 as c_api
import cv2
from threading import Thread

from queue import Queue
# hilo para guardar stream de img
class writeImg(Thread):
    def __init__(self):
        super().__init__()
        self.que=Queue()
    def run(self) -> None:
        while True:
            [name,img]=self.que.get()# internamente espera hasta que haya información disponible en el buffer
            if hasattr(img,"shape"): # si no es una imagen/ variable numpy 
                cv2.imwrite(name,img)
            else: 
                break
    def close(self):
        self.que.put([None,None])
##########################
class Camara:
    def __init__(self,name:str,width:int,hight:int,fps:int) -> None:
        self.name=name
        self.canWork=False
        self.width=width
        self.hight=hight
        self.fps=fps
    def config(self) -> None:
        print("start configuration")
    def getFrame(self) -> np.ndarray:

        pass
    def closeCamara(self) -> None:
        pass

    def __str__(self) -> str:
        return f"Camara {self.name}: {self.width}x{self.hight} pixeles at {self.fps} FPS"
###################################################################
class handlerStream:
    def __init__(self,dev:object,type:str,width:int,hight:int,fps:int) -> None:
        self.width=width
        self.hight=hight
        self.fps=fps
        self.dev=dev
        self.waitms=10/1000
        if type=="rgb":
                self.dtype=np.uint8
                pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888
                self.stream=self.dev.create_color_stream()
                self.getFrame=self.getFrameRgb
        elif type=="depth":
                self.dtype=np.uint16
                self.stream=self.dev.create_depth_stream()
                pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM
                self.getFrame=self.getFrameDepth
        else:
                print("unidentified type")
                return None
        self.stream.set_video_mode(c_api.OniVideoMode(pixelFormat=pixelFormat, resolutionX= self.width, resolutionY = self.hight, fps = self.fps))
        self.stream.start()
        
    def getFrameRgb(self)-> np.ndarray:
        bgr   = np.frombuffer(self.stream.read_frame().get_buffer_as_uint16(),dtype=self.dtype).reshape(480,640,3)
        rgb   = cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB)
        
        return rgb
    def getFrameDepth(self)-> np.ndarray:
        depth = np.frombuffer(self.stream.read_frame().get_buffer_as_uint16(),dtype=self.dtype).reshape(480,640)
        depth=cv2.merge((depth,depth,depth))
        
        return depth
        

class CamaraOrbbec(Camara):
    def __init__(self) -> None:
        super().__init__("Orbbec",width=640,hight=480,fps=30)
        self.dev=None
        self.depthStream=None
        self.rgbStream=None
        self.handlerStreams=[]
        self.isOpen=False
    def config(self) -> None:
        super().config()
        # Initialize the depth device
        openni2.initialize()
        self.dev = openni2.Device.open_any()
        self.handlerStreams.append(handlerStream(self.dev,"rgb",self.width,self.hight,self.fps))
        self.handlerStreams.append(handlerStream(self.dev,"depth",self.width,self.hight,self.fps))
        self.isOpen=True
    def getFrame(self,streamType=0) -> np.ndarray:
        return self.handlerStreams[streamType].getFrame()

    def closeCamara(self) -> None:

        openni2.unload()
        self.isOpen=False
        print("camara closed")

if __name__== "__main__":
    orbecc=CamaraOrbbec()
    print(orbecc)
    orbecc.config()
    nameWindow="RGB"
    while orbecc.isOpen:
        rgb=orbecc.getFrame(0)
        cv2.imshow(nameWindow,rgb)
        key=cv2.waitKey(1) & 0xFF
        if key==ord('q'):
            orbecc.closeCamara()
            
    cv2.destroyAllWindows()
