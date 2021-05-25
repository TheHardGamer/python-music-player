from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox
import tkinter.ttk as ttk
from ttkthemes import ThemedTk
from ttkthemes import ThemedStyle
import openal
from openal import *
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
import ast
import webbrowser

pyglet.font.add_file('googlesans.ttf')

# Create a tkinter instance
base = Tk()

# Initialize pygame
pygame.mixer.init()

# The title and resolution of the app
base.title("TheRagingBeast")
base.geometry("800x600")
base.configure(bg="#04030F")
base.resizable(0,0)

# Create the main skeleton
main = Frame(base)
main.pack(pady=10)
main.configure(bg="#04030F")
theme = ThemedStyle(main)

# I hav arriv
canvas = Canvas(main, width=500, height=66)
canvas.grid(row=0, column=0)
img = PhotoImage(file="pics/logo.png")
canvas.create_image(250,36, image=img)
canvas.configure(bg="#04030F", highlightthickness=0)

# Define about_player function
def about_player():
	about = Text(main)
	about.insert(INSERT, "A music player written in python by TheHardGamer")
	# Make the text widget read only
	about.configure(state='disabled', font=("Google Sans",10))
	about.grid(row=4, column=0)
	# Destroy the widget
	about.after(2000, about.destroy)

def contact_tg():
	webbrowser.open("https://t.me/TheHardGodGamer")

def contact_github():
	webbrowser.open("https://github.com/TheHardGamer")

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
	global islooping
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
	if (islooping):
		return
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
	if (islooping):
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
	if (islooping):
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
	if (isStopped):
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
	filename = fd.askopenfilename(title="Select file to convert to mp3")
	strippedname = os.path.split(filename)[1]
	finalname = os.path.splitext(strippedname)[0]
	AudioSegment.from_file(filename).export(finalname + ".mp3", format="mp3", bitrate="192k")
	messagebox.showinfo(title="Conversion status", message="Conversion Complete!")

def playlist_save():
	f = fd.asksaveasfile(mode='w', defaultextension=".txt")
	if f is None:
		return
	text2save = str(pl.get(0, END))
	f.write(text2save)
	f.close()

def playlist_import():
	file = fd.askopenfile(mode ='r', filetypes =[('Text', '*.txt')])
	if file is not None:
		content = file.read()
		data_list = ast.literal_eval(content)
		for song in data_list:
			pl.insert(END, song)

# playlist box
pl = Listbox(main, bg="#04030F", fg="white", width=90, selectbackground="#FF495C")
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
songs_menu.add_command(label="Create a playlist of currently added songs", command=playlist_save)
songs_menu.add_command(label="Import a playlist", command=playlist_import)
songs_menu.configure(font=("Google Sans",9))

# Add a sub-menu under the menu skeleton
about_menu = Menu(top_menu, tearoff=0)
top_menu.add_cascade(label="About", menu=about_menu, font=("Google Sans",9))
about_menu.add_command(label="The player", command=about_player)
about_menu.configure(font=("Google Sans",9))

convertor_menu= Menu(top_menu, tearoff=0)
top_menu.add_cascade(label="MP3 convertor", menu=convertor_menu, font=("Google Sans",9))
#convertor_menu.add_command(label="Help", command=convertor_help)
convertor_menu.add_command(label="Convert", command=convert_song)
convertor_menu.configure(font=("Google Sans",9))

contact_menu = Menu(top_menu, tearoff=0)
top_menu.add_cascade(label="Contact me", menu=contact_menu, font=("Google Sans",9))
contact_menu.add_command(label="Github", command=contact_github)
contact_menu.add_command(label="Telegram", command=contact_tg)
contact_menu.configure(font=("Google Sans",9))

# Frame for the play/pause buttons
buttonsframe = Frame(main)
buttonsframe.grid(row=3, column=0, pady=10)
buttonsframe.configure(bg="#04030F")

# Back Button
backbuttonImage = PhotoImage(file="pics/back.png")
backbutton = Button(buttonsframe, image=backbuttonImage, height=64, width=64, borderwidth=0, command=previous_song)
backbutton.grid(row=0, column=0, padx=10, pady=10)
backbutton.configure(bg="#04030F")

# Pause Button
pausebuttonImage = PhotoImage(file="pics/pause.png")
# We need to know if the song is paused or not and so we require a sort of boolean which is passed through lambda
pausebutton = Button(buttonsframe, image=pausebuttonImage, height=64, width=64, borderwidth=0, command=lambda: pause_song(isPaused))
pausebutton.grid(row=0, column=1, padx=10, pady=10)
pausebutton.configure(bg="#04030F")

# Play Button
playbuttonImage = PhotoImage(file="pics/play.png")
playbutton = Button(buttonsframe, image=playbuttonImage, height=64, width=64, borderwidth=0, command=play_song)
playbutton.grid(row=0, column=2, padx=10, pady=10)
playbutton.configure(bg="#04030F")

# Stop Button
stopbuttonImage = PhotoImage(file="pics/stop.png")
stopbutton = Button(buttonsframe, image=stopbuttonImage, height=64, width=64, borderwidth=0, command=stop_song)
stopbutton.grid(row=0, column=3, padx=10, pady=10)
stopbutton.configure(bg="#04030F")

# Forward Button
forwardImage = PhotoImage(file="pics/forward.png")
forwardbutton = Button(buttonsframe, image=forwardImage, height=64, width=64, borderwidth=0, command=forward_song)
forwardbutton.grid(row=0, column=4, padx=10, pady=10)
forwardbutton.configure(bg="#04030F")

# Bring the info bar into existence
info_bar = Label(base, text="", bd=2, relief=RAISED)
info_bar.pack(fill=X, side=BOTTOM, ipady=2)
info_bar.configure(bg='#04030F', fg='#73EEDC', font=("Google Sans",9))

# Define yt_dl function
def yt():
	finallink = link.get("1.0","end")
	return finallink

def yt_dl():
	finallink = yt()
	ydl_opts = {
	'format': 'bestaudio/best',
	'outtmpl': '%(title)s.%(ext)s',
	'postprocessors': [{
		'key': 'FFmpegExtractAudio',
		'preferredcodec': 'mp3',
		'preferredquality': '192',
		}],
	}
	youtube_dl.YoutubeDL(ydl_opts).download([finallink])
	messagebox.showinfo(title="Youtube to MP3", message="Download Complete!")

def vid_dl():
	finallink = yt()
	youtube_dl.YoutubeDL.download([finallink])

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
enter_url.insert(INSERT, "Enter a video URL supported by youtube_dl in the following box")
enter_url.insert(INSERT, "\nAnd stream/download it with the respective buttons")
enter_url.configure(height=2, state='disabled', bg="#04030F")
enter_url.configure(font=("Google Sans", 10, "normal"), fg="#0FFF95")
enter_url.grid(row=4, column=0, pady=3)

link = Text(main, bg="#04030F", fg="#73EEDC")
link.configure(height=1)
link.grid(row=5, column=0, pady=5)

# Frame for YT buttons
ytframe = Frame(main)
ytframe.grid(row=6, column=0, pady=5)
ytframe.configure(bg="#04030F")
ytdl_button = Button(ytframe, text="Download the video", font=("Google Sans",9), command=vid_dl, bg="#0FFF95")
ytdl_button.grid(row=1, column=0, padx=2)
ytdl_button = Button(ytframe, text="Download video as MP3", font=("Google Sans",9), command=yt_dl, bg="#0FFF95")
ytdl_button.grid(row=1, column=1, padx=2)
ytdl_button = Button(ytframe, text="Stream The above YT link", font=("Google Sans",9), command=stream, bg="#0FFF95")
ytdl_button.grid(row=1, column=2, padx=2)
ytdl_button = Button(ytframe, text="Pause/Resume the stream", font=("Google Sans",9), command=pause_stream, bg="#0FFF95")
ytdl_button.grid(row=1, column=3, padx=2)
ytdl_button = Button(ytframe, text="Stop the stream", font=("Google Sans",9), command=stop_stream, bg="#0FFF95")
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

showeq_button = Button(main, text="Show visualizer", font=("Google Sans",9), command=show_eq, bg="#0FFF95")
showeq_button.grid(row=7, column=0)

# Set app icon
icon = PhotoImage(file="pics/icon.png")
base.iconphoto(True, icon)

base.mainloop()