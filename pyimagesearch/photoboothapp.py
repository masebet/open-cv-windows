# import the necessary packages
from __future__ import print_function
from imutils.video import VideoStream
from imutils.video import FPS
from PIL import Image
from PIL import ImageTk
import tkinter as tki
import numpy as np
import argparse
import threading
import datetime
import imutils
import pickle
import cv2
import os
import sys
import shutil

from lib import embeding , train
from libData import *

class PhotoBoothApp:
	def __init__(self, vs):
		self.vs = vs
		self.frame = None
		self.thread = None
		self.stopEvent = None

		self.root = tki.Tk()
		self.root.geometry("800x450") 
		self.panel = None

		self.stopEvent = threading.Event()
		self.fps = FPS().start()
		args = {}
		args["detector"]="face_detection_model"
		args["embedding_model"]="openface_nn4.small2.v1.t7"
		args["recognizer"]="output/recognizer.pickle"
		args["le"]="output/le.pickle"
		args["confidence"]=0.5
		self.protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
		self.modelPath = os.path.sep.join([args["detector"],"res10_300x300_ssd_iter_140000.caffemodel"])
		self.detector = cv2.dnn.readNetFromCaffe(self.protoPath, self.modelPath)
		self.embedder = cv2.dnn.readNetFromTorch(args["embedding_model"])
		self.recognizer = pickle.loads(open(args["recognizer"], "rb").read())
		self.le = pickle.loads(open(args["le"], "rb").read())	
		self.tulisan = "absen"
		self.buff = "nama"
		self.img_counter = 0

		self.thread = threading.Thread(target=self.absen, args=())
		self.thread1 = threading.Thread(target=self.event, args=())

		self.thread.start()
		self.thread1.start()

		self.root.wm_title("A B S E N S I")
		self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

	def videoLoop(self):
		try:
			while not self.stopEvent.is_set():
				self.frame = self.vs.read()
				self.frame = imutils.resize(self.frame, width=300)
				image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
				image = Image.fromarray(image)
				image = ImageTk.PhotoImage(image)
				if self.panel is None:
					self.panel = tki.Label(image=image)
					self.panel.image = image
					self.panel.pack(side="left", padx=10, pady=10)
				else:
					self.panel.configure(image=image)
					self.panel.image = image

		except RuntimeError:
			print("[INFO] caught a RuntimeError")

	def takeSnapshot(self):
		ts = datetime.datetime.now()
		filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
		p = os.path.sep.join((self.outputPath, filename))

		cv2.imwrite(p, self.frame.copy())
		print("[INFO] saved {}".format(filename))

	def absen(self):
		try:
			while not self.stopEvent.is_set():
				self.frame = self.vs.read()
				self.frame = imutils.resize(self.frame, width=600)
				(h, w) = self.frame.shape[:2]

				imageBlob = cv2.dnn.blobFromImage(cv2.resize(self.frame, (300, 300)), 1.0, (300, 300),(104.0, 177.0, 123.0), swapRB=False, crop=False)	
				self.detector.setInput(imageBlob)
				self.detections = self.detector.forward()
				
				for i in range(0, self.detections.shape[2]):
					confidence = self.detections[0, 0, i, 2]
					if confidence > 0.5 :
						box = self.detections[0, 0, i, 3:7] * np.array([w, h, w, h])
						(startX, startY, endX, endY) = box.astype("int")
						face = self.frame[startY:endY, startX:endX]
						(fH, fW) = face.shape[:2]
						if fW < 20 or fH < 20:
							continue
						faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,(96, 96), (0, 0, 0), swapRB=True, crop=False)
						self.embedder.setInput(faceBlob)
						vec = self.embedder.forward()

						preds = self.recognizer.predict_proba(vec)[0]
						j = np.argmax(preds)
						proba = preds[j]
						name = self.le.classes_[j]
						simpanData.noId=name		
						text = "{}: {:.2f}%".format(name, proba * 100)
						y = startY - 10 if startY - 10 > 10 else startY + 10
						cv2.rectangle(self.frame, (startX, startY), (endX, endY),(0, 0, 255), 2)
						cv2.putText(self.frame, name, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
				
				self.fps.update()

				font = cv2.FONT_HERSHEY_SIMPLEX
				# cv2.putText(self.frame, self.tulisan, (10,450), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
				# cv2.putText(self.frame, getData("waktu"), (10,350), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
				# cv2.putText(self.frame, getData("tangal"), (10,250), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
				# cv2.putText(self.frame, dataDataBuff.mataKuliah, (10,50), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
				if simpanData.noId != "unknown":
					try:
						keDb()
						cv2.putText(self.frame,getNama(), (10,150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv2.LINE_AA)
						tutupDb()
					except:
						print("masalah")	
				else:
					cv2.putText(self.frame, "Scan Wajah Anda", (10,150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv2.LINE_AA)

				if self.buff != simpanData.noId :
					self.buff = simpanData.noId
					tki.Label(self.root, text="                                ").place(x = 610, y = 110)
				else:
					tki.Label(self.root, text=simpanData.noId).place(x = 610, y = 110)

				tki.Label(self.root, text=getData("waktu")).place(x = 610, y = 70)
				tki.Label(self.root, text=getData("tangal")).place(x = 610, y = 90)
				image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
				image = Image.fromarray(image)
				image = ImageTk.PhotoImage(image)
				if self.panel is None:
					self.panel = tki.Label(image=image)
					self.panel.image = image
					self.panel.place(x = 0, y = 0)
				else:
					self.panel.configure(image=image)
					self.panel.image = image
		except RuntimeError:
			print("[INFO] caught a RuntimeError")
	
	def onClose(self):
		self.fps.stop()
		self.stopEvent.set()
		self.vs.stop()
		self.root.quit()

	def event(self):
		OPTIONS = [
		"Semester 1",
		"Semester 2",
		"Semester 3",
		"Semester 4",
		"Semester 5",
		"Semester 6",
		"Semester 7"
		] 
		OPTIONS_MATKUL = [
		"MTK",
		"AGAMA",
		"MK1",
		"MK2",
		"MK3",
		"MK4",
		"MK5"
		] 
		dataDataBuff.semester = tk.StringVar(self.root)
		dataDataBuff.semester.set(OPTIONS[0])

		dataDataBuff.mataKuliah = tk.StringVar(self.root)
		dataDataBuff.mataKuliah.set(OPTIONS_MATKUL[0])

		tki.OptionMenu(self.root, dataDataBuff.semester, *OPTIONS).place(x = 610, y = 0)
		tki.OptionMenu(self.root, dataDataBuff.mataKuliah, *OPTIONS_MATKUL).place(x = 610, y = 30)
		tki.Button(self.root, text="Klik To Absen",command=self.inputAbsen).place(x = 610, y = 400)
		return 0;

	def inputAbsen(self):
		try:
			simpanData.semester=dataDataBuff.semester.get()
			simpanData.matkul=dataDataBuff.mataKuliah.get()
			print(simpanData.semester)
			print(simpanData.noId)
			print(getData("waktu"))
			print(getData("tangal"))
			simpanData.nama=getNama()
			keDb()
			simpanData.iSql()
			tutupDb()
			if dataSyncOk()>0:
				dataSync()
		except RuntimeError:
			print("[INFO] caught a RuntimeError")
		return 0;

	def inputAction():
		global buffString
		dataDataBuff.mataKuliah.get()
		dataDataBuff.semester.get()
		return 0;