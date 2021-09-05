from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import os
from pydub import AudioSegment
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from qt_material import apply_stylesheet, QtStyleTools
import youtube_dl
import sqlite3

class Stream(QObject):
	newText = pyqtSignal(str)

	def write(self, text):
		self.newText.emit(str(text))

	def flush(self):
		pass

class VideoplayerWindow(QMainWindow):
	state = pyqtSignal(bool)

class YtdownloadWindow(QMainWindow):
	dloadfinished = pyqtSignal(bool)

class SaavnDownloadWindow(QMainWindow):
	dloadfinished = pyqtSignal(bool)

# Thread for music convertor
class ConvertorThread(QThread):
	signal = pyqtSignal()

	def __init__(self):
		QThread.__init__(self)
		self.song = ""
		self.finalname = ""
		self.strippedname = ""

	def run(self):
		AudioSegment.from_file(self.song).export(self.finalname + ".mp3", format="mp3", bitrate="192k")
		self.signal.emit()

# Thread for ytdl
class ytdlThread(QThread):
	signal = pyqtSignal()

	def __init__(self):
		QThread.__init__(self)
		self.url = ""
		self.ydl_opts = {}

	def run(self):
		youtube_dl.YoutubeDL(self.ydl_opts).download([self.url])
		self.signal.emit()

class PList(QAbstractListModel):
	def __init__(self, playlist, *args, **kwargs):
		super(PList, self).__init__(*args, **kwargs)
		self.playlist = playlist

	def data(self, index, role):
		if role == Qt.DisplayRole:
			media = self.playlist.media(index.row())
			return media.canonicalUrl().fileName()

	def rowCount(self, index):
		return self.playlist.mediaCount()

class TRB(QMainWindow, QtStyleTools):
	def __init__(self):
		super().__init__()
		self.ui = uic.loadUi('trb.ui', self)
		self.setWindowTitle("TheRagingBeast")
		self.setFixedSize(800, 600)
		self.setWindowIcon(QIcon('pics/icon.png'))
		QFontDatabase.addApplicationFont('googlesans.ttf')
		self.player = QMediaPlayer(self)
		self.playlist = QMediaPlaylist()
		self.player.setPlaylist(self.playlist)
		self.addsongs.triggered.connect(self.getsongs)
		self.plcurrentadded.triggered.connect(self.plcurradded)
		self.playbutton.clicked.connect(self.playsongs)
		self.nextbutton.clicked.connect(self.playlist.next)
		self.prevbutton.clicked.connect(self.playlist.previous)
		self.pausebutton.clicked.connect(self.player.pause)
		self.stopbutton.clicked.connect(self.player.stop)
		self.viewer = VideoplayerWindow(self)
		self.viewer.setWindowFlags(self.viewer.windowFlags() | Qt.WindowStaysOnTopHint)
		self.viewer.setMinimumSize(QSize(720,360))
		videoWidget = QVideoWidget()
		self.viewer.setCentralWidget(videoWidget)
		self.player.setVideoOutput(videoWidget)
		self.ytdlwin = YtdownloadWindow(self)
		self.ytui = uic.loadUi('ytdl.ui', self.ytdlwin)
		self.ytdlwin.dlvid.clicked.connect(self.downloadvid)
		self.ytdlwin.dlaud.clicked.connect(self.downloadaud)
		self.songslider.sliderReleased.connect(self.seeksong)
		self.clearpl.triggered.connect(self.clearplaylist)
		self.voldial.valueChanged.connect(self.setvol)
		self.model = PList(self.playlist)
		self.songslist.setModel(self.model)
		self.playlist.currentIndexChanged.connect(self.plistposchange)
		selection_model = self.songslist.selectionModel()
		selection_model.selectionChanged.connect(self.plistselchange)
		self.cthread = ConvertorThread()
		self.cthread.signal.connect(self.cthreadend)
		self.ytdlwin.ytthread = ytdlThread()
		self.ytdlwin.ytthread.signal.connect(self.ytthreadend)
		self.ytdl.triggered.connect(self.openytwindow)
		self.player.positionChanged.connect(self.slidermove)
		self.player.durationChanged.connect(self.slidermax)
		self.convertsong.triggered.connect(self.sconvert)
		self.player.mediaStatusChanged.connect(self.vidplayer)
		self.videobut.setHidden(True)
		self.videobut.clicked.connect(self.showvideo)
		self.playlist.currentMediaChanged.connect(self.nplaying)
		self.loadinganim.setHidden(True)
		sys.stdout = Stream(newText=self.showmsg)
		self.conn = sqlite3.connect('TRB.sqlite3')
		self.curr = self.conn.cursor()
		try:
			self.curr.executescript(''' CREATE TABLE Data (Theme   varchar); ''')
			self.curr.execute('''INSERT INTO Data (Theme) VALUES ('dark_lightgreen')''')
			self.conn.commit()
		except:
			pass
		try:
			self.curr.execute('SELECT Theme FROM Data')
			currtheme = self.curr.fetchall()
			for i in currtheme:
				if (i[0] == "dark_blue"):
					apply_stylesheet(self.ui, theme='dark_blue.xml', extra={'font_family': 'Google Sans', })
				elif (i[0] == "dark_amber"):
					apply_stylesheet(self.ui, theme='dark_amber.xml', extra={'font_family': 'Google Sans', })
				elif (i[0] == "dark_lightgreen"):
					apply_stylesheet(self.ui, theme='dark_lightgreen.xml', extra={'font_family': 'Google Sans', })
				elif (i[0] == "dark_red"):
					apply_stylesheet(self.ui, theme='dark_red.xml', extra={'font_family': 'Google Sans', })
				elif (i[0] == "dark_yellow"):
					apply_stylesheet(self.ui, theme='dark_yellow.xml', extra={'font_family': 'Google Sans', })
		except:
			pass
		self.themes()
		self.ui.show()

	def themes(self):
		self.defaulttheme.triggered.connect(lambda: self.apply_stylesheet(self.ui, 'dark_lightgreen.xml', extra={'font_family': 'Google Sans', }))
		self.defaulttheme.triggered.connect(lambda: self.updatedbtheme("dark_lightgreen"))
		self.darkblue.triggered.connect(lambda: self.apply_stylesheet(self.ui, 'dark_blue.xml', extra={'font_family': 'Google Sans', }))
		self.darkblue.triggered.connect(lambda: self.updatedbtheme("dark_blue"))
		self.darkamber.triggered.connect(lambda: self.apply_stylesheet(self.ui, 'dark_amber.xml', extra={'font_family': 'Google Sans', }))
		self.darkamber.triggered.connect(lambda: self.updatedbtheme("dark_amber"))
		self.darkred.triggered.connect(lambda: self.apply_stylesheet(self.ui, 'dark_red.xml', extra={'font_family': 'Google Sans', }))
		self.darkred.triggered.connect(lambda: self.updatedbtheme("dark_red"))
		self.darkyellow.triggered.connect(lambda: self.apply_stylesheet(self.ui, 'dark_yellow.xml', extra={'font_family': 'Google Sans', }))
		self.darkyellow.triggered.connect(lambda: self.updatedbtheme("dark_yellow"))

	def updatedbtheme(self, color):
		self.color = color
		self.curr.execute('''DELETE FROM Data''')
		self.curr.execute('''INSERT INTO Data (Theme) VALUES (?)''', (self.color,))
		self.conn.commit()

	def getsongs(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		songs = QFileDialog.getOpenFileNames(self,"Add songs", "","", options=options)[0]
		for song in songs:
			self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(song)))
		self.model.layoutChanged.emit()

	def plcurradded(self):
		try:
			self.curr.executescript(''' CREATE TABLE Data (Playlist   varchar); ''')
		except:
			pass

	global i
	def plistselchange(self, ix):
		global i
		i = ix.indexes()[0].row()

	global ix
	def plistposchange(self, i):
		global ix
		if i > -1:
			ix = self.model.index(i)
			self.songslist.setCurrentIndex(ix)

	def sconvert(self):
		self.cthread.song = QFileDialog.getOpenFileName(self, "Convert a Song to MP3s", "","")[0]
		self.cthread.strippedname = os.path.split(self.cthread.song)[1]
		self.cthread.finalname = os.path.splitext(self.cthread.strippedname)[0]
		self.loading = QMovie("loading.gif", QByteArray(), self)
		self.loadinganim.setHidden(False)
		self.loadinganim.setMovie(self.loading)
		self.loading.start()
		self.cthread.start()

	def cthreadend(self):
		self.loading.stop()
		self.loadinganim.setHidden(True)
		QMessageBox.about(self, "Convertor", "Conversion Complete!")

	def playsongs(self):
		global i
		global ix
		if self.playlist.isEmpty() == False:
			self.player.play()
			self.playlist.setCurrentIndex(i)
			self.songslist.setCurrentIndex(ix)

	def vidplayer(self, status):
		if status == 6:
			if self.player.isVideoAvailable():
				self.videobut.setHidden(False)
			else:
				self.videobut.setHidden(True)

	def showvideo(self):
		self.viewer.show()

	def formattime(self, dur):
		hour, r = divmod(dur, 3600000)
		minute, r = divmod(r, 60000)
		second, _ = divmod(r, 1000)
		return ("%d:%02d:%02d" % (hour,minute,second)) if hour else ("%d:%02d" % (minute,second))

	def slidermove(self, position):
		self.songslider.setValue(position)
		self.infolabel.setText("{now} / {total}".format(now=self.formattime(position), total=self.formattime(self.player.duration())))
 
	def slidermax(self, duration):
		self.songslider.setRange(0, duration)

	def seeksong(self):
		self.songslider.setFocus()
		if self.player.state() == QMediaPlayer.PlayingState:
			seek = self.songslider.value()
			self.player.setPosition(seek)

	def clearplaylist(self):
		selection_model = self.songslist.selectionModel()
		self.player.stop()
		self.playlist.clear()
		selection_model.clear()

	def setvol(self):
		self.player.setVolume(self.voldial.value())

	def nplaying(self, media):
		if not media.isNull():
			url = media.canonicalUrl()
			self.nowplaying.setText("Now Playing:\n {}".format(url.fileName()))
			self.nowplaying.adjustSize()

	def openytwindow(self):
		self.ytdlwin.show()

	def downloadvid(self):
		self.ytdlwin.ytthread.url = self.ytdlwin.yturl.toPlainText()
		self.ytdlwin.ytthread.ydl_opts ={'format': 'bestvideo+bestaudio','outtmpl': '%(title)s.%(ext)s'}		
		self.ytdlwin.ytthread.start()
		self.ytdlwin.yturl.clear()

	def downloadaud(self):
		self.ytdlwin.ytthread.url = self.ytdlwin.yturl.toPlainText()
		self.ytdlwin.ytthread.ydl_opts ={
		'format': 'bestaudio/best',
		'outtmpl': '%(title)s.%(ext)s',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
			},
			{'key': 'FFmpegMetadata'},],
		}
		self.ytdlwin.ytthread.start()	
		self.ytdlwin.yturl.clear()

	def showmsg(self, text):
		if not self.ytdlwin.yturl.visibleRegion().isEmpty():
			self.ytdlwin.cursor = self.ytdlwin.yturl.textCursor()
			self.ytdlwin.cursor.movePosition(QTextCursor.End)
			self.ytdlwin.cursor.insertText(text)
			self.ytdlwin.yturl.setTextCursor(self.ytdlwin.cursor)
			self.ytdlwin.yturl.ensureCursorVisible()

	def ytthreadend(self):
		QMessageBox.about(self.ytdlwin, "Downloader", "Download Complete!")
		self.ytdlwin.yturl.clear()


app = QApplication(sys.argv)
window = TRB()
app.setStyle('QtCurve')
sys.exit(app.exec_())