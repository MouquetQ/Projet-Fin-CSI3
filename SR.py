from tkinter import *
from PIL import Image,ImageTk
import cv2
from time import *

cap = cv2.VideoCapture(0)
rep, frame=cap.read()
cv2image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
Rapport=1/4
zoom=1
heightOr=cv2image.shape[0]
widthOr=cv2image.shape[1]
height=heightOr*Rapport
width=widthOr*Rapport

Fenetre0 =Tk()
Fenetre0.title("")
Fenetre0.resizable(width=False, height=False)
canvas0 = Canvas(Fenetre0, width = 2*widthOr, height = 2*heightOr)
canvas0.pack()

sr = cv2.dnn_superres.DnnSuperResImpl_create()
path = "C:/Users/stani/Documents/Python finCSI3/ESPCN_x4.pb"
sr.readModel(path)
sr.setModel("espcn",4)

t1=time()
sleep(1)

while True:

    t2=time()
    f=1/(t2-t1)
    print(int(f),1/Rapport)

    canvas0.delete(ALL)

    rep, frame=cap.read()
    frame = cv2.flip(frame, 1)

    cv2image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    img=Image.fromarray(cv2image)
    imgtk=ImageTk.PhotoImage(img)
    canvas0.create_image(0,0,anchor = NW,image=imgtk)

    frameComp=cv2.resize(frame,(int(width),int(height)))
    cv2imageComp = cv2.cvtColor(frameComp, cv2.COLOR_RGB2BGR)
    imgComp=Image.fromarray(cv2imageComp)
    imgtkComp=ImageTk.PhotoImage(imgComp)
    canvas0.create_image(widthOr,heightOr,anchor = NW,image=imgtkComp)

    frameBicubic=cv2.resize(frameComp,(int(widthOr),int(heightOr)))
    cv2imageBicubic = cv2.cvtColor(frameBicubic, cv2.COLOR_RGB2BGR)
    imgBicubic=Image.fromarray(cv2imageBicubic)
    imgtkBicubic=ImageTk.PhotoImage(imgBicubic)
    canvas0.create_image(widthOr,0,anchor = NW,image=imgtkBicubic)



    frameIA=sr.upsample(frameComp)
    cv2imageIA=cv2.cvtColor(frameIA,cv2.COLOR_BGR2RGB)
    imgIA=Image.fromarray(cv2imageIA)
    imgtkIA=ImageTk.PhotoImage(imgIA)
    canvas0.create_image(0,heightOr,anchor = NW,image=imgtkIA)


    t1=t2

    Fenetre0.update()