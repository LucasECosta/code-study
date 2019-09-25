import cv2
import numpy as np
import random
import time

class Video():
    def __init__(self,url):
        self._url = url
        self._frame = None
        self._fgbg = cv2.createBackgroundSubtractorMOG2()
        self._contours = None
        self._idtracked = []
        self._countours = []
        self.allowed = []
        self._items = {}
        self._vehicles = {'ID':1,'CENTER':2,'SPEED':3}

    def removeBG(self):
        
        self._frame = cv2.cvtColor (self._frame, cv2.COLOR_BGR2GRAY)
        fgmask = self._fgbg.apply (self._frame)
        kernel = np.ones((4,4),np.uint8)
        kernel_dilate = np.ones((5,5),np.uint8)        
        opening = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        dilation = cv2.morphologyEx(opening, cv2.MORPH_OPEN, kernel_dilate)
        self._contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self._frame = dilation
    
    @property
    def url(self):
        return self._url
    
    @url.setter
    def url(self, video=0):
        self._video = cv2.VideoCapture(self.url)
    
    def track_obj(self):
        contours = [cnt for cnt in self._contours]
        bboxes = [cv2.boundingRect(cnt) for cnt in contours]
        checked = [[((int(cnt[0]+cnt[2]/2)),int((cnt[1]+cnt[3]/2))), cnt[0], cnt[1], cnt[2], cnt[3]] for cnt in bboxes if cnt[2]*cnt[3] > 4000]
        size = len(checked)

        
        if len(self.allowed) == 0:
            self.allowed = [{"ID": random.randint(1000,9999), 
            "CENTER": checked[i][0], 
            "TL":(checked[i][1], checked[i][2]), 
            "BR":(checked[i][1] + checked[i][3], checked[i][2] + checked[i][4]),
            "SPEED":0} 
            for i in range(size)]
        else:
            self.allowed = [self.checkdistance(checked[i]) if self.checkdistance(checked[i]) else 
            {"ID": random.randint(1000,9999), 
            "CENTER": checked[i][0], 
            "TL":(checked[i][1], checked[i][2]), 
            "BR":(checked[i][1] + checked[i][3], checked[i][2] + checked[i][4]),
            "SPEED":0}
            for i in range(size)]
         
    def calcSpeed(self):
        contador = 0
        for vehicle in self.allowed:
            if self._vehicles['ID'] == vehicle['ID']:
                if contador == 0:
                    self._vehicles = {'ID':vehicle['ID'],'CENTER':vehicle['CENTER'],'SPEED':time.time()}
                    contador = 1
            else:
                if time.time()-self._vehicles['SPEED'] > 1500000000.0000000 or time.time()-self._vehicles['SPEED'] == 0 :
                    pass
                else:
                    conta = float((time.time() - self._vehicles['SPEED'])*100)
                    if conta < 15:
                        print(f"{int(conta*10)} KM/H")
                        
                self._vehicles = {'ID':vehicle['ID'],'CENTER':vehicle['CENTER'],'SPEED':0}
                contador = 0
                        
            cv2.circle(self._frame, vehicle["CENTER"],5,(0,0,0),-1)
            cv2.rectangle(self._frame, vehicle["TL"], vehicle["BR"], (255, 255, 0), 3)
            cv2.putText(self._frame, str(vehicle["ID"]), vehicle["BR"], cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))
            cv2.putText(self._frame, str(vehicle["CENTER"][1]), vehicle["TL"], cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))
    def checkdistance(self, obj):
        sizeallowed = len(self.allowed)
        distance = [(((obj[0][0] - self.allowed[i]["CENTER"][0])**2 +  (obj[0][1] - self.allowed[i]["CENTER"][1])**2)**(1/2), self.allowed[i]) for i in range(sizeallowed)]
        mindistance = min([x[0] for x in distance])
        item = [x[1] for x in distance if x[0] == mindistance][0]
        if mindistance < 100:
            item = {"ID": item["ID"], "CENTER": obj[0], "TL": (obj[1],obj[2]), "BR": (obj[1]+obj[3],obj[2]+obj[4]),"SPEED":0}
            return item

    def getSpeed(self):
        Y_TEST = 400
        lineThickness = 2
        cv2.line(self._frame, (0, Y_TEST), (1280, Y_TEST), (0,255,0), lineThickness)

    def realtime(self):
        FPS = 30
        while True:
            _, frame = self.url.read()
            self._frame = frame
            self.removeBG()
            self.track_obj()     
            self.getSpeed()
            self.calcSpeed()
            cv2.imshow("Janela", self._frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(1.0 / FPS)
        cv2.destroyAllWindows()
 
trafego = Video(cv2.VideoCapture('traffic_video.mp4'))
trafego.realtime()
