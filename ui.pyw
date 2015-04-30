import tkinter as tk
import tkinter.filedialog
from datetime import datetime as dtime
import controller
import math
import time


class MainFrame(tk.Frame):


	def __init__(self, root=None):

		self._root = root
		self._configRoot()

		tk.Frame.__init__(self, self._root)	

		self._createMenu()	

		self.grid(row=0, column=0)	

		self._elements = {}	
		
		#Type 1 by default
		self._workType = 1		
		self._createTypeOneWidgets()	

		self._textFile = False


	def _collectSendData(self):
		"""collecting data from Entries and sending this voc to Controller"""
		
		data = {}
		data["artist"] = self._elements["eArtist"].get()
		data["track"] = self._elements["eTrack"].get()		
		year = int(self._elements["eYear"].get())
		month = int(self._elements["eMonth"].get())
		day = int(self._elements["eDay"].get())
		hour = int(self._elements["eHour"].get())
		minute = int(self._elements["eMinute"].get())
		dtimeObj = dtime(year, month, day, hour, minute).timestamp()
		data["timestamp"] = math.floor(dtimeObj)
		
		isAuthentificated = controller.Scrobbler.hasUser()

		if not isAuthentificated:

			controller.Scrobbler.authentificateUser()
			self._createQuestionFrame()	

		else:

			if data["artist"] != "" and data["track"] != "":
				controller.Scrobbler.scrobble(data)		


	def _configRoot(self):
		self._root.geometry("350x200")
		self._root.resizable(False, False)
		self._root.title("LastFM Desktop Scrobbler")


	def _createChoiceWidgets2(self):

		def openFile():
			filename = tkinter.filedialog.askopenfilename()
			if filename:
				filenameLast = filename.split("/")
				filenameLast = filenameLast[len(filenameLast) - 1]
				self._elements["lFileName"]["text"] = filenameLast
				self._textFile = open(filename, "r")
			else:
				self._elements["lFileName"]["text"] = "Файл не выбран!"
				self._textFile = False
		
		self._textFile = False
		self._elements["bFile"] = tk.Button(self, text="Выбрать файл", command=openFile)
		self._elements["bFile"].grid(row=1, column=0, padx=120, pady=3)		
		self._elements["lFileName"] = tk.Label(self, text="Выберите файл")
		self._elements["lFileName"].grid(row=2, column=0, padx=120, pady=3)
		self._elements["tText"] = tk.Text(self, font=("courier", 8), width=30, height=5)
		self._elements["tText"].grid(row=3, column=0, padx=30, pady=3)
		self._elements["tText"].delete(1.0, tk.END)
		self._elements["tText"].insert(1.0, "Scrobbling info will be this place...")


	def _createDateWidgets1(self):
		self._elements["lDate"] = tk.Label(self, text="Год - Месяц - День")
		self._elements["lDate"].grid(row=0, column=1, columnspan=5)
		self._elements["eYear"] = tk.Entry(self, width=5)
		self._elements["eYear"].insert(0, dtime.now().year)
		self._elements["eYear"].grid(row=1, column=1)
		self._elements["lSeparator1"] = tk.Label(self, text="-")
		self._elements["lSeparator1"].grid(row=1, column=2)
		self._elements["eMonth"] = tk.Entry(self, width=5)
		self._elements["eMonth"].insert(0, dtime.now().month)
		self._elements["eMonth"].grid(row=1, column=3)		
		self._elements["lSeparator2"] = tk.Label(self, text="-")
		self._elements["lSeparator2"].grid(row=1, column=4)
		self._elements["eDay"] = tk.Entry(self, width=5)
		self._elements["eDay"].insert(0, dtime.now().day)
		self._elements["eDay"].grid(row=1, column=5)


	def _createMenu(self):
		self._menu = tk.Menu(self._root)
		self._root.config(menu=self._menu)
		self._menu.add_command(label="Одиночный", command=self._setWorkTypeOne)
		self._menu.add_command(label="Из файла", command=self._setWorkTypeTwo)


	def _createQuestionFrame(self):
		self._root.withdraw()
		root = tk.Tk()
		dialog = QuestionFrame(self, root)
		dialog.mainloop()


	def _createSubmit1(self):
		self._elements["bSubmit"] = tk.Button(self, text="Scrobble")
		self._elements["bSubmit"].grid(row=4, column=0, pady=30, columnspan=6)
		self._elements["bSubmit"]["command"] = self._collectSendData


	def _createSubmit2(self):
		self._elements["bSubmit"] = tk.Button(self, text="Scrobble")
		self._elements["bSubmit"].grid(row=4, column=0, padx=120, pady=3)
		self._elements["bSubmit"]["command"] = self._processFile


	def _createTimeWidgets1(self):
		self._elements["lTime"] = tk.Label(self, text="Часы - Минуты")
		self._elements["lTime"].grid(row=2, column=1, columnspan=5)
		self._elements["eHour"] = tk.Entry(self, width=5)
		self._elements["eHour"].insert(0, dtime.now().hour)
		self._elements["eHour"].grid(row=3, column=1, columnspan=2)
		self._elements["lSeparator3"] = tk.Label(self, text="-")
		self._elements["lSeparator3"].grid(row=3, column=3)
		self._elements["eMinute"]= tk.Entry(self, width=5)
		self._elements["eMinute"].insert(0, dtime.now().minute)
		self._elements["eMinute"].grid(row=3, column=4, columnspan=2)


	def _createTrackWidgets1(self):
		self._elements["lArtist"] = tk.Label(self, text="Artist")		
		self._elements["lArtist"].grid(row=0, column=0, padx=30, pady=5)
		self._elements["eArtist"] = tk.Entry(self, width=20)
		self._elements["eArtist"].grid(row=1, column=0, padx=30)
		self._elements["lTrack"] = tk.Label(self, text="Track")
		self._elements["lTrack"].grid(row=2, column=0, padx=30, pady=5)
		self._elements["eTrack"] = tk.Entry(self, width=20)
		self._elements["eTrack"].grid(row=3, column=0, padx=30)		


	def _createTypeOneWidgets(self):
		self._createTrackWidgets1()
		self._createDateWidgets1()	
		self._createTimeWidgets1()	
		self._createSubmit1()	


	def _createTypeTwoWidgets(self):
		self._createChoiceWidgets2()
		self._createSubmit2()


	def _deleteWidgets(self):
		for element in self._elements:			
			self._elements[element].destroy()
		self._elements.clear()


	def _processFile(self):

		def _getData(textString):

			currStringList = textString.split("\n")[0].split("=>")			

			data = {}
			data["artist"] = currStringList[0]
			data["track"] = currStringList[1]				

			dateList = currStringList[2].split("/")
			year = int(dateList[0])
			month = int(dateList[1])
			day = int(dateList[2])			

			timeList = currStringList[3].split(":")
			hour = int(timeList[0])
			minute = int(timeList[1])			
			
			dtimeObj = dtime(year, month, day, hour, minute).timestamp()				
			data["timestamp"] = math.floor(dtimeObj)	

			return data
		
		if self._textFile:

			isAuthentificated = controller.Scrobbler.hasUser()
			if not isAuthentificated:
				controller.Scrobbler.authentificateUser()
				self._createQuestionFrame()	

			textList = self._textFile.readlines()
			self._textFile.close()
			self._textFile = None

			self._elements["tText"].delete(1.0, tk.END)			

			for i in range(len(textList)):

				time.sleep(0.5)
				
				try:
					data = _getData(textList[i])
				except:
					self._elements["tText"].insert(1.0, "Error: " + '"' + textList[i] + '"' + "\n")					
				else:																		
					controller.Scrobbler.scrobble(data)
					self._elements["tText"].insert(1.0, "Scrobbled: " + '"' + textList[i] + '"' + "\n")				
				
	
	def _setWorkTypeOne(self):
		if self._workType == 2:
			self._deleteWidgets()
			self._createTypeOneWidgets()
			self._workType = 1


	def _setWorkTypeTwo(self):
		if self._workType == 1:
			self._deleteWidgets()
			self._createTypeTwoWidgets()
			self._workType = 2
	

class QuestionFrame(tk.Frame):

	
	def __init__(self, main, root):
		self._root = root
		self._main = main
		self._configRoot()
		tk.Frame.__init__(self, self._root)
		self.grid(row=0, column=0)
		self._createWidgets()


	def _configRoot(self):
		self._root.geometry("300x100")
		self._root.resizable(False, False)
		self._root.title("Подтверждение авторизации")


	def _createWidgets(self):
		lNote = tk.Label(self, text="Нажмите ОК после подтверждения авторизации")
		lNote.grid(row=0, column=0, padx=10, pady=20)
		bOK = tk.Button(self, text="OK")
		bOK.grid(row=1, column=0)
		bOK["command"] = self._destroy


	def _destroy(self):
		controller.Scrobbler.getSession()
		self._main._root.deiconify()
		self._root.destroy()


def main():
	rootMain = tk.Tk()
	mainFrame = MainFrame(rootMain)
	mainFrame.mainloop()


main()