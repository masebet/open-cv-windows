import MySQLdb
from datetime import date
from datetime import datetime
import tkinter as tk

global db

def getData(getOut):
	today = date.today()
	now = datetime.now()
	if getOut == "tangal":
		return today.strftime("%Y/%m/%d")
	if getOut == "waktu":
		#return now.strftime("%H:%M:%S")
		return now.strftime("%H:%M")

def keDb():
	global db
	db = MySQLdb.connect(host="localhost",user="root",passwd="",db="absen")
'''
cursor = db.cursor()
cursor.execute("SELECT * FROM `data-angota`")
numrows = cursor.rowcount
for x in range(0, numrows):
    row = cursor.fetchone()
    print (row[0],row[1],row[2],row[3])
db.close()
'''
def tutupDb():
	global db
	db.close()


def qSql():
	global db
	cursor = db.cursor()
	cursor.execute("SELECT * FROM `log-absen`")
	numrows = cursor.rowcount
	for x in range(0, numrows):
		row = cursor.fetchone()
		print (row[0],row[1],row[2],row[3],row[4],row[5])

class simpanData:
	matkul =""
	nama =""
	noId = ""

	def qPSql(dataIn):
		global db
		cursor = db.cursor()
		cursor.execute("SELECT dataIn FROM `log-absen` WHERE id = "+simpanData.noId+"")
		numrows = cursor.rowcount
		row = cursor.fetchone()
		return row[0]

	def getNama():
		global db
		cursor = db.cursor()
		cursor.execute("SELECT nama FROM `data-angota` WHERE id = "+simpanData.noId+"")
		numrows = cursor.rowcount
		row = cursor.fetchone()
		return row[0]	

	def iSql():
		simpanData.nama=simpanData.getNama()
		global db
		cursor = db.cursor()	
		cursor.execute("INSERT into `log-absen` (`status`,`id`,`nama`,`hari`,`jam`,`matkul`) VALUES (%s,%s,%s,%s,%s,%s)",("0",""+simpanData.noId+"",""+simpanData.nama+"",getData("tangal"),getData("waktu"),""+simpanData.matkul+""))
		db.commit()


class dataDataBuff:
	mataKuliah =""
	master = 0

def inputAction():
	global buffString	
	dataDataBuff.mataKuliah = buffString.get()
	dataDataBuff.master.destroy()
	dataDataBuff.master.quit()

def inputMataKuliah():
	dataDataBuff.master = tk.Tk()
	global buffString
	buffString = tk.StringVar(dataDataBuff.master)
	tk.Label(dataDataBuff.master, text="INPUT MATKUL").grid(row=0)
	tk.Entry(dataDataBuff.master,textvariable = buffString).grid(row=0, column=1)
	tk.Button(dataDataBuff.master,text='OK',command=inputAction).grid(row=0, column=2)
	dataDataBuff.master.mainloop()
