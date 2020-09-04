from tkinter import *
from tkinter import filedialog as fd
import tkinter.ttk as ttk
from ttkthemes import ThemedTk
from ttkthemes import ThemedStyle
from tkinter import ttk
import openal
from openal import *
import pyogg
from lxml import etree
import urllib.request
import urllib
from urllib.request import urlopen, urlretrieve
from urllib.parse import quote_plus, urlencode
import youtube_dl
import pygame
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from pydub import AudioSegment
import time
import pafy
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication
from qtwidgets import EqualizerBar
import random
import threading
import vlc
import pyglet

pyglet.font.add_file('googlesans.ttf')

# Create a tkinter instance
base = Tk()

# Initialize pygame
pygame.mixer.init()

# The title and resolution of the app
base.title("TheRagingBeast")
base.geometry("800x600")
base.configure(bg="black")

# Create the main skeleton
main = Frame(base)
main.pack(pady=10)
main.configure(bg="black")
theme = ThemedStyle(main)

# Fancy Image
canvas = Canvas(main, width=500, height=66)
canvas.grid(row=0, column=0)
img = PhotoImage(file="pics/logo.png")
canvas.create_image(250,36, image=img)
canvas.configure(bg="black", highlightthickness=0)

# Define about_player function
def about_player():
	about = Text(main)
	about.insert(INSERT, "A music player written in python by varunhardgamer")
	# Make the text widget read only
	about.configure(state='disabled', font=("Google Sans",10))
	about.grid(row=4, column=0)
	# Destroy the widget
	about.after(2000, about.destroy)

def contact_tg():
	contact = Text(main)
	contact.insert(INSERT, "https://t.me/TheHardGamer")
	contact.configure(state='disabled', font=("Google Sans",10))
	contact.grid(row=4, column=0)
	contact.after(2000, contact.destroy)

def contact_github():
	github = Text(main)
	github.insert(INSERT, "https://github.com/varunhardgamer")
	github.configure(state='disabled', font=("Google Sans",10))
	github.grid(row=4, column=0)
	github.after(2000, github.destroy)

def convertor_help():
	convertor = Text(main)
	convertor.insert(INSERT, "Convert the currently selected file in the List to MP3")
	convertor.insert(INSERT, "\nTap The Convert button under the Convert sub-menu to convert")
	convertor.insert(INSERT, "\nthe currently selected file in the box to MP3")
	convertor.configure(state='disabled', font=("Google Sans", 10))
	convertor.grid(row=4, column=0)
	convertor.after(5000, convertor.destroy)

def add_songs():
	# askopenfilenames returns a tuple of files selected
	songs = fd.askopenfilenames(title="Select songs")
	# Iterate the tuple
	for song in songs:
			pl.insert(END, song)

# Define del_song function
def del_song():
	# ANCHOR is the selected item in the listbox widget
	pl.delete(ANCHOR)

global curr_play
# Define play_song function
def play_song():
	global isStopped
	global curr_play
	isStopped = False
	song_slider.config(to=0, value=0)
	info_bar.config(text="0")
	song = pl.get(ACTIVE)
	curr_play = song
	extension = os.path.splitext(song)[1]
	if (extension == ".mp3"):
		oalQuit()
		pygame.mixer.music.stop()
		pygame.mixer.music.load(song)
		pygame.mixer.music.play(loops=0)
	else:
		oalQuit()
		pygame.mixer.music.stop()
		sauce = oalOpen(song)
		sauce.play()
	song_slider.config(to=0, value=0)
	info_bar.config(text="0")
	if (islooping == True):
		return
	else:
		song_time()

# Define forward_song function
def forward_song():
	song_slider.config(to=0, value=0)
	global isStopped
	global curr_play
	isStopped = False
	current_song = pl.curselection()
	upcoming_song = current_song[0] + 1
	song = pl.get(upcoming_song)
	curr_play = song
	extension = os.path.splitext(song)[1]
	pl.selection_clear(current_song[0])
	pl.activate(upcoming_song)
	pl.selection_set(upcoming_song)
	if (islooping == True):
		pass
	else:
		song_time()
	if (song > ''):
		if (extension == ".mp3"):
			oalQuit()
			pygame.mixer.music.stop()
			pygame.mixer.music.load(song)
			pygame.mixer.music.play(loops=0)
		else:
			oalQuit()
			pygame.mixer.music.stop()
			sauce = oalOpen(song)
			sauce.play()
		song_slider.config(to=0, value=0)
		info_bar.config(text="0")
	else:
		stop_song()

# Define previous_song function
def previous_song():
	global isStopped
	isStopped = False
	global curr_play
	current_song = pl.curselection()
	previous_song = current_song[0] - 1
	song = pl.get(previous_song)
	curr_play = song
	extension = os.path.splitext(song)[1]
	pl.selection_clear(current_song[0])
	pl.activate(previous_song)
	pl.selection_set(previous_song)
	if (islooping == True):
		pass
	else:
		song_time()
	if (extension == ".mp3"):
		oalQuit()
		pygame.mixer.music.stop()
		pygame.mixer.music.load(song)
		pygame.mixer.music.play(loops=0)
	else:
		oalQuit()
		pygame.mixer.music.stop()
		sauce = oalOpen(song)
		sauce.play()
	song_slider.config(to=0, value=0)
	info_bar.config(text="0")

# Define pause_song function
global isPaused
isPaused = False
def pause_song(is_paused):
	global isPaused
	global islooping
	isPaused = is_paused
	song = pl.get(ACTIVE)
	if isPaused:
		isPaused = False
		pygame.mixer.music.unpause()
	else:
		oalQuit()
		pygame.mixer.music.pause()
		isPaused = True
		islooping = False

# Define stop_song function
global isStopped
isStopped = False
def stop_song():
	global isStopped
	global islooping
	oalQuit()
	pygame.mixer.music.stop()
	# Clear the selected song
	pl.selection_clear(ACTIVE)
	info_bar.config(text="00:00")
	song_slider.config(value=0)
	isStopped = True
	islooping = False

global islooping
islooping = False
def song_time():
	if (isStopped == True):
		return
	global islooping
	islooping = True
	global curr_play
	# Get currently playing song
	current_song = curr_play
	if (str(curr_play) is pl.get(ACTIVE)):
		return
	extension = os.path.splitext(current_song)[1]
	# Get song's current position
	sec = pygame.mixer.music.get_pos() / 1000
	# Convert it to MM:SS format
	formatted_time = time.strftime('%M:%S', time.gmtime(sec))
	# Invoke mutagen
	if (extension == ".mp3"):
		mut = MP3(current_song)
		# Get the total length of currently playing song
		length = mut.info.length
		# Convert it to MM:SS format
		length_time = time.strftime('%M:%S', time.gmtime(length))
		final_time = formatted_time + "/" + length_time
		# Add an if check to avoid the function from recursing when music is "Stopped"
		if sec >= 0:
			# Add it as text to info bar
			info_bar.config(text=final_time)
		# Compare the sliders position and the length of the song and stop the song if they are equal
		if song_slider.get() >= int(length):
			islooping = True
			current_song = pl.curselection()
			upcoming_song = current_song[0] + 1
			song = pl.get(upcoming_song)
			if(song > ''):
				forward_song()
			else:
				pass
		elif isPaused:
			pass
		else:
			# Move slider along every 1 second
			song_slider.config(to=length)
			next_time = song_slider.get()+1
			song_slider.config(value=next_time)
			if(song_slider.get() > length):
				song_slider.config(value=length)
			total_length = length_time
			# Format the time of slider's position
			slider_time = time.strftime('%M:%S', time.gmtime(int(song_slider.get()))) + "/" + length_time
			info_bar.config(text=slider_time)
	else:
		# TEMP Disable stuff while playing flac for now
		mut = FLAC(current_song)
		length = mut.info.length
		length_time = time.strftime('%M:%S', time.gmtime(length))
		info_bar.config(text=length_time)
	islooping = True
	info_bar.after(1000, song_time)
	return

def slider(x):
	# Check if the music is stopped and stop updating
	if (isStopped):
		return
	# Do nothing if the music being played isnt mp3[WIP]
	song = pl.get(ACTIVE)
	extension = os.path.splitext(song)[1]
	if (extension == ".mp3"):
		pygame.mixer.music.load(song)
		pygame.mixer.music.play(loops=0, start=song_slider.get())
	else:
		# [TEMP] Disable the slider
		song_slider.config(state='disabled')

def convert_song():
	song = pl.get(ACTIVE)
	strippedname = os.path.split(song)[1]
	finalname = os.path.basename(strippedname)
	AudioSegment.from_file(song).export(finalname + ".mp3", format="mp3", bitrate="192k")

# playlist box
pl = Listbox(main, bg="black", fg="white", width=90, selectbackground="blue")
pl.grid(row=1, column=0, pady=10)
pl.configure(font=("Google Sans",10))

# Song slider widget
style = ttk.Style()
style.theme_use('equilux')
song_slider = ttk.Scale(main, from_=0, orient=HORIZONTAL, length=500, command=slider)
song_slider.grid(row=2, column=0, pady=10)

# Create a menu skeleton
top_menu = Menu(base)
base.config(menu=top_menu)

# Add an entry to the menu skeleton, define tearoff to disable the ability to detach menus from main window
songs_menu = Menu(top_menu, tearoff=0)
# Add a sub-menu named "Add songs" under the menu skeleton and add an empty sub-menu under it
top_menu.add_cascade(label="Songs", menu=songs_menu, font=("Google Sans",9))
# Populate the empty sub-menu
songs_menu.add_command(label="Add Songs", command=add_songs)
songs_menu.add_command(label="Delete selected song", command=del_song)
songs_menu.configure(font=("Google Sans",9))

# Add a sub-menu under the menu skeleton
about_menu = Menu(top_menu, tearoff=0)
top_menu.add_cascade(label="About", menu=about_menu, font=("Google Sans",9))
about_menu.add_command(label="The player", command=about_player)
about_menu.configure(font=("Google Sans",9))

convertor_menu= Menu(top_menu, tearoff=0)
top_menu.add_cascade(label="MP3 convertor", menu=convertor_menu, font=("Google Sans",9))
convertor_menu.add_command(label="Help", command=convertor_help)
convertor_menu.add_command(label="Convert", command=convert_song)
convertor_menu.configure(font=("Google Sans",9))

contact_menu = Menu(top_menu, tearoff=0)
top_menu.add_cascade(label="Contact me", menu=contact_menu, font=("Google Sans",9))
contact_menu.add_command(label="Telegram", command=contact_tg)
contact_menu.add_command(label="Github", command=contact_github)
contact_menu.configure(font=("Google Sans",9))

# Frame for the play/pause buttons
buttonsframe = Frame(main)
buttonsframe.grid(row=3, column=0, pady=10)
buttonsframe.configure(bg="black")

# Back Button
backbuttonImage = PhotoImage(file="pics/back.png")
backbutton = Button(buttonsframe, image=backbuttonImage, height=64, width=64, borderwidth=0, command=previous_song)
backbutton.grid(row=0, column=0, padx=10, pady=10)
backbutton.configure(bg="black")

# Pause Button
pausebuttonImage = PhotoImage(file="pics/pause.png")
# We need to know if the song is paused or not and so we require a sort of boolean which is passed through lambda
pausebutton = Button(buttonsframe, image=pausebuttonImage, height=64, width=64, borderwidth=0, command=lambda: pause_song(isPaused))
pausebutton.grid(row=0, column=1, padx=10, pady=10)
pausebutton.configure(bg="black")

# Play Button
playbuttonImage = PhotoImage(file="pics/play.png")
playbutton = Button(buttonsframe, image=playbuttonImage, height=64, width=64, borderwidth=0, command=play_song)
playbutton.grid(row=0, column=2, padx=10, pady=10)
playbutton.configure(bg="black")

# Stop Button
stopbuttonImage = PhotoImage(file="pics/stop.png")
stopbutton = Button(buttonsframe, image=stopbuttonImage, height=64, width=64, borderwidth=0, command=stop_song)
stopbutton.grid(row=0, column=3, padx=10, pady=10)
stopbutton.configure(bg="black")

# Forward Button
forwardImage = PhotoImage(file="pics/forward.png")
forwardbutton = Button(buttonsframe, image=forwardImage, height=64, width=64, borderwidth=0, command=forward_song)
forwardbutton.grid(row=0, column=4, padx=10, pady=10)
forwardbutton.configure(bg="black")

# Bring the info bar into existence
info_bar = Label(base, text="", bd=2, relief=RAISED)
info_bar.pack(fill=X, side=BOTTOM, ipady=2)
info_bar.configure(bg="black", font=("Google Sans",9))

# Define yt_dl function
def yt():
	finallink = link.get("1.0","end")
	return finallink

def yt_dl():
	finallink = yt()
	ydl_opts = {
	'format': 'bestaudio/best',
	'outtmpl': '%(id)s.%(ext)s',
	'postprocessors': [{
		'key': 'FFmpegExtractAudio',
		'preferredcodec': 'mp3',
		'preferredquality': '192',
		}],
	}
	youtube_dl.YoutubeDL(ydl_opts).download([finallink])

global player
def stream():
	global player
	finallink = yt()
	video = pafy.new(finallink)
	best = video.getbest()
	playurl = best.url
	Instance = vlc.Instance()
	player = Instance.media_player_new()
	Media = Instance.media_new(playurl)
	Media.get_mrl()
	player.set_media(Media)
	player.play()

def pause_stream():
	global player
	player.pause()

def stop_stream():
	global player
	player.stop()

enter_url = Text(main, borderwidth=0)
enter_url.insert(INSERT, "Enter a youtube video URL in the following box")
enter_url.insert(INSERT, "\nAnd stream/download it as mp3 with the respective buttons")
enter_url.configure(height=2, state='disabled', bg="black")
enter_url.configure(font=("Google Sans", 10, "normal"))
enter_url.grid(row=4, column=0, pady=3)

link = Text(main, bg="black", fg="red")
link.configure(height=1)
link.grid(row=5, column=0, pady=5)
# Frame for YT buttons
ytframe = Frame(main)
ytframe.grid(row=6, column=0, pady=5)
ytframe.configure(bg="black")
ytdl_button = Button(ytframe, text="Download YT as MP3", font=("Google Sans",9), command=yt_dl)
ytdl_button.grid(row=1, column=0, padx=2)
ytdl_button = Button(ytframe, text="Stream The above YT link", font=("Google Sans",9), command=stream)
ytdl_button.grid(row=1, column=1, padx=2)
ytdl_button = Button(ytframe, text="Pause/Resume the stream", font=("Google Sans",9), command=pause_stream)
ytdl_button.grid(row=1, column=2, padx=2)
ytdl_button = Button(ytframe, text="Stop the stream", font=("Google Sans",9), command=stop_stream)
ytdl_button.grid(row=1, column=4, padx=2)

def show_eq():
	if(song_slider.get() > 1):
		class Window(QtWidgets.QMainWindow):

			def __init__(self):
				super().__init__()

				self.equalizer = EqualizerBar(5, ['#0C0786', '#40039C', '#6A00A7', '#8F0DA3', '#B02A8F', '#CA4678', '#E06461',
											   '#F1824C', '#FCA635', '#FCCC25', '#EFF821'])

				self.setCentralWidget(self.equalizer)

				self._timer = QtCore.QTimer()
				self._timer.setInterval(100)
				self._timer.timeout.connect(self.update_values)
				self._timer.start()

			def update_values(self):
				self.equalizer.setValues([
					min(100, v+random.randint(0, 50) if random.randint(0, 5) > 2 else v)
					for v in self.equalizer.values()
					])

		app = QApplication(sys.argv)
		w = Window()
		w.show()
		k = app.exec_(sys.argv)
		t = threading.Thread(target=k)
		t.start()

showeq_button = Button(main, text="Show visualizer", font=("Google Sans",9), command=show_eq)
showeq_button.grid(row=7, column=0)

# Set app icon
icon = PhotoImage(file="pics/icon.png")
base.iconphoto(True, icon)

base.mainloop()