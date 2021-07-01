from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import os
import threading
from pydub import AudioSegment
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from qt_material import apply_stylesheet, QtStyleTools

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
		self.playbutton.clicked.connect(self.playsongs)
		self.nextbutton.clicked.connect(self.playlist.next)
		self.prevbutton.clicked.connect(self.playlist.previous)
		self.pausebutton.clicked.connect(self.player.pause)
		self.stopbutton.clicked.connect(self.player.stop)
		self.songslider.sliderReleased.connect(self.seeksong)
		self.model = PList(self.playlist)
		self.songslist.setModel(self.model)
		self.playlist.currentIndexChanged.connect(self.plistposchange)
		selection_model = self.songslist.selectionModel()
		selection_model.selectionChanged.connect(self.plistselchange)
		self.cthread = ConvertorThread()
		self.cthread.signal.connect(self.cthreadend)
		self.player.positionChanged.connect(self.slidermove)
		self.player.durationChanged.connect(self.slidermax)
		self.convertsong.triggered.connect(self.sconvert)
		self.loadinganim.setHidden(True)
		apply_stylesheet(self.ui, theme='dark_lightgreen.xml', extra={'font_family': 'Google Sans', })
		self.themes()
		self.ui.show()

	def themes(self):
		self.defaulttheme.triggered.connect(lambda: self.apply_stylesheet(self.ui, 'dark_lightgreen.xml', extra={'font_family': 'Google Sans', }))
		self.darkblue.triggered.connect(lambda: self.apply_stylesheet(self.ui, 'dark_blue.xml', extra={'font_family': 'Google Sans', }))
		self.darkamber.triggered.connect(lambda: self.apply_stylesheet(self.ui, 'dark_amber.xml', extra={'font_family': 'Google Sans', }))
		self.darkred.triggered.connect(lambda: self.apply_stylesheet(self.ui, 'dark_red.xml', extra={'font_family': 'Google Sans', }))
		self.darkyellow.triggered.connect(lambda: self.apply_stylesheet(self.ui, 'dark_yellow.xml', extra={'font_family': 'Google Sans', }))

	def getsongs(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		songs = QFileDialog.getOpenFileNames(self,"Add songs", "","", options=options)[0]
		for song in songs:
			self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(song)))
		self.model.layoutChanged.emit()

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
		self.player.play()
		self.playlist.setCurrentIndex(i)
		self.songslist.setCurrentIndex(ix)

	def slidermove(self, position):
		self.songslider.setValue(position)
 
	def slidermax(self, duration):
		self.songslider.setRange(0, duration)

	def seeksong(self):
		if self.player.state() == QMediaPlayer.PlayingState:
			seek = self.songslider.value()
			self.player.setPosition(seek)

app = QApplication(sys.argv)
window = TRB()
app.setStyle('QtCurve')
sys.exit(app.exec_())