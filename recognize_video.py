# HOW USAGE
'''
 python recognize_video.py --detector face_detection_model --embedding-model openface_nn4.small2.v1.t7 --recognizer output/recognizer.pickle --le output/le.pickle
'''
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import pickle
import time
import cv2
import os
import tkinter as tk

#from lib.py import train
from lib import embeding , train
from libData import *

tulisan = "absen"
perintah = "normal"
img_counter = 0

def show_entry_fields():
    global tulisan
    global perintah
    tulisan = "daftar"
    part = mystring.get()
    print (tulisan)
    try:
    	os.mkdir("dataset//"+part)
    except OSError:
    	print ("gagal")
    	tulisan = "gagal coba nim lain"
    else:
    	print ("bisa")
    	img_counter = 0
    	while True:
		    frame = vs.read()
		    frame = imutils.resize(frame, width=600)
		    font = cv2.FONT_HERSHEY_SIMPLEX
		    cv2.putText(frame, tulisan, (10,450), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
		    cv2.putText(frame, str(img_counter), (10,300), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
		    cv2.imshow("Absen", frame)
		    key = cv2.waitKey(1) & 0xFF
		    if key == ord("r"):
		    	frame = vs.read()
		    	gambar= imutils.resize(frame, width=600)
		    	img_name = "dataset//"+part+"//0000{}.png".format(img_counter)
		    	cv2.imwrite(img_name, gambar)
		    	print("{} written!".format(img_name))
		    	img_counter += 1
		    	if img_counter > 5:
		    		break

    master.destroy()
    master.quit()
'''
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--detector", required=True,help="path to OpenCV's deep learning face detector")
ap.add_argument("-m", "--embedding-model", required=True,help="path to OpenCV's deep learning face embedding model")
ap.add_argument("-r", "--recognizer", required=True,help="path to model trained to recognize faces")
ap.add_argument("-l", "--le", required=True,help="path to label encoder")
ap.add_argument("-c", "--confidence", type=float, default=0.5,help="minimum probability to filter weak detections")
args = vars(ap.parse_args())
'''
inputMataKuliah()

args = {}
args["detector"]="face_detection_model"
args["embedding_model"]="openface_nn4.small2.v1.t7"
args["recognizer"]="output/recognizer.pickle"
args["le"]="output/le.pickle"
args["confidence"]=0.5

#print("[INFO] loading face detector...")
protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
modelPath = os.path.sep.join([args["detector"],"res10_300x300_ssd_iter_140000.caffemodel"])
print(args["detector"])
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

#print("[INFO] loading face recognizer...")
embedder = cv2.dnn.readNetFromTorch(args["embedding_model"])
print(args["embedding_model"])

recognizer = pickle.loads(open(args["recognizer"], "rb").read())
print(args["recognizer"])
le = pickle.loads(open(args["le"], "rb").read())
print(args["le"])

#print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

fps = FPS().start()


while True:
	frame = vs.read()

	frame = imutils.resize(frame, width=600)
	(h, w) = frame.shape[:2]

	imageBlob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300),(104.0, 177.0, 123.0), swapRB=False, crop=False)
	
	detector.setInput(imageBlob)
	detections = detector.forward()
	
	for i in range(0, detections.shape[2]):
		confidence = detections[0, 0, i, 2]
		if confidence > args["confidence"]:
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")
			face = frame[startY:endY, startX:endX]
			(fH, fW) = face.shape[:2]
			if fW < 20 or fH < 20:
				continue
			faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,(96, 96), (0, 0, 0), swapRB=True, crop=False)
			embedder.setInput(faceBlob)
			vec = embedder.forward()

			preds = recognizer.predict_proba(vec)[0]
			j = np.argmax(preds)
			proba = preds[j]
			name = le.classes_[j]
			simpanData.noId=name
			
			text = "{}: {:.2f}%".format(name, proba * 100)
			y = startY - 10 if startY - 10 > 10 else startY + 10
			cv2.rectangle(frame, (startX, startY), (endX, endY),(0, 0, 255), 2)
			cv2.putText(frame, text, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)	

	fps.update()

	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(frame, tulisan, (10,450), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
	cv2.putText(frame, getData("waktu"), (10,350), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
	cv2.putText(frame, getData("tangal"), (10,250), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
	
	cv2.putText(frame, dataDataBuff.mataKuliah, (10,50), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
	
	if simpanData.noId != "unknown":
		keDb()
		cv2.putText(frame, simpanData.getNama(), (10,150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv2.LINE_AA)
		tutupDb()
	else:
		cv2.putText(frame, "Scan Wajah Anda", (10,150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv2.LINE_AA)
	
	#print(simpanData.noId)
	cv2.imshow("Absen", frame)
	key = cv2.waitKey(1) & 0xFF
	#print(key)
	


	if key == ord("i"):
		keDb()
		simpanData.matkul=dataDataBuff.mataKuliah
		simpanData.iSql()
		tutupDb()

	if key == ord("b"):
		master = tk.Tk()
		mystring = tk.StringVar(master)
		tk.Label(master, text="NIM").grid(row=0)
		tk.Entry(master,textvariable = mystring).grid(row=0, column=1)
		tk.Button(master,text='OK',command=show_entry_fields).grid(row=0, column=2)
		master.mainloop()

	if key == ord("Q"):
		break
	if key == ord("q"):
		break
	if key == ord("z"):
		embeding()
		train()

fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()