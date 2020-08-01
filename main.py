from tkinter import *
from tkinter import filedialog as fd
import tkinter.ttk as ttk
from lxml import etree
import urllib.request
import urllib
from urllib.request import urlopen, urlretrieve
from urllib.parse import quote_plus, urlencode
import youtube_dl
import pygame
from mutagen.mp3 import MP3
import time

# Create a tkinter instance
base = Tk()

# Initialize pygame
pygame.mixer.init()

# The title and resolution of the app
base.title("TheRagingBeast")
base.geometry("800x600")

# Create the main skeleton
main = Frame(base)
main.pack(pady=10)

# Fancy Image
canvas = Canvas(main, width=500, height=66)
canvas.grid(row=0, column=0)
img = PhotoImage(file="pics/logo.png")
canvas.create_image(250,36, image=img)

# Define about_player function
def about_player():
	about = Text(base)
	about.insert(INSERT, "A basic music player written in python by varunhardgamer")
	# Make the text widget read only
	about.configure(state='disabled')
	about.pack()
	# Destroy the widget
	about.after(2000, about.destroy)

def contact_tg():
	contact = Text(base)
	contact.insert(INSERT, "https://t.me/TheHardGamer")
	contact.configure(state='disabled')
	contact.pack()
	contact.after(2000, contact.destroy)

def contact_github():
	github = Text(base)
	github.insert(INSERT, "https://github.com/varunhardgamer")
	github.configure(state='disabled')
	github.pack()
	github.after(2000, github.destroy)

# Define add_song function
def add_song():
	song = fd.askopenfilename(title="Select a song")
	pl.insert(END, song)

def add_songs():
	# askopenfilenames returns a tuple of files selected
	songs = fd.askopenfilenames(title="Select songs", filetypes=[("Mp3 Files", "*.mp3")])
	# Iterate the tuple
	for song in songs:
			pl.insert(END, song)

# Define del_song function
def del_song():
	# ANCHOR is the selected item in the listbox widget
	pl.delete(ANCHOR)

# Define play_song function
def play_song():
	global isStopped
	isStopped = False
	song = pl.get(ACTIVE)
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)
	song_time()

# Define forward_song function
def forward_song():
	song_slider.config(value=0)
	global isStopped
	isStopped = False
	current_song = pl.curselection()
	upcoming_song = current_song[0] + 1
	song = pl.get(upcoming_song)
	if (song > ''):
		pygame.mixer.music.load(song)
		pygame.mixer.music.play(loops=0)
		pl.selection_clear(current_song[0])
		pl.activate(upcoming_song)
		pl.selection_set(upcoming_song)
	else:
		stop_song()

# Define previous_song function
def previous_song():
	song_slider.config(value=0)
	global isStopped
	isStopped = False
	current_song = pl.curselection()
	previous_song = current_song[0] - 1
	song = pl.get(previous_song)
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)
	pl.selection_clear(current_song[0])
	pl.activate(previous_song)
	pl.selection_set(previous_song)

# Define pause_song function
global isPaused
isPaused = False
def pause_song(is_paused):
	global isPaused
	isPaused = is_paused
	if isPaused:
		isPaused = False
		pygame.mixer.music.unpause()
	else:
		pygame.mixer.music.pause()
		isPaused = True

# Define stop_song function
global isStopped
isStopped = False
def stop_song():
	global isStopped
	pygame.mixer.music.stop()
	# Clear the selected song
	pl.selection_clear(ACTIVE)
	info_bar.config(text="00:00")
	song_slider.config(value=0)
	isStopped = True

def song_time():
	if (isStopped == True):
		return
	# Get currently playing song
	current_song = pl.get(ACTIVE)
	# Get song's current position
	sec = pygame.mixer.music.get_pos() / 1000
	# Convert it to MM:SS format
	formatted_time = time.strftime('%M:%S', time.gmtime(sec))
	# Invoke mutagen
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
	# Loop it every 1s to update time
	info_bar.after(1000, song_time)
	# Compare the sliders position and the length of the song and stop the song if they are equal
	if int(song_slider.get()) == int(length):
		forward_song()
	elif isPaused:
		pass
	else:
		# Move slider along every 1 second
		next_time = int(song_slider.get()) + 1
		song_slider.config(to=length, value=next_time)
		total_length = length_time
		# Format the time of slider's position
		slider_time = time.strftime('%M:%S', time.gmtime(int(song_slider.get()))) + "/" + length_time
		info_bar.config(text=slider_time)

def slider(x):
	# Check if the music is stopped and stop updating
	if (isStopped):
		return
	song = pl.get(ACTIVE)
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0, start=song_slider.get())

# playlist box
pl = Listbox(main, bg="black", fg="red", width=90, selectbackground="green")
pl.grid(row=1, column=0, pady=10)

# Song slider widget
song_slider = ttk.Scale(main, from_=0, orient=HORIZONTAL, length=500, command=slider)
song_slider.grid(row=2, column=0, pady=10)

# Create a menu skeleton
top_menu = Menu(base)
base.config(menu=top_menu)

# Add an entry to the menu skeleton, define tearoff to disable the ability to detach menus from main window
songs_menu = Menu(top_menu, tearoff=0)
# Add a sub-menu named "Add songs" under the menu skeleton and add an empty sub-menu under it
top_menu.add_cascade(label="Songs", menu=songs_menu)
# Populate the empty sub-menu
songs_menu.add_command(label="Add song", command=add_song)
songs_menu.add_command(label="Add songs", command=add_songs)
songs_menu.add_command(label="Delete song", command=del_song)

# Add a sub-menu under the menu skeleton
about_menu = Menu(top_menu, tearoff=0)
top_menu.add_cascade(label="About", menu=about_menu)
about_menu.add_command(label="The player", command=about_player)

contact_menu = Menu(top_menu, tearoff=0)
top_menu.add_cascade(label="Contact me", menu=contact_menu)
contact_menu.add_command(label="Telegram", command=contact_tg)
contact_menu.add_command(label="Github", command=contact_github)

# Frame for the play/pause buttons
buttonsframe = Frame(main)
buttonsframe.grid(row=3, column=0, pady=10)

# Back Button
backbuttonImage = PhotoImage(file="pics/back.png")
backbutton = Button(buttonsframe, image=backbuttonImage, height=64, width=64, borderwidth=0, command=previous_song)
backbutton.grid(row=0, column=0, padx=10, pady=10)

# Pause Button
pausebuttonImage = PhotoImage(file="pics/pause.png")
# We need to know if the song is paused or not and so we require a sort of boolean which is passed through lambda
pausebutton = Button(buttonsframe, image=pausebuttonImage, height=64, width=64, borderwidth=0, command=lambda: pause_song(isPaused))
pausebutton.grid(row=0, column=1, padx=10, pady=10)

# Play Button
playbuttonImage = PhotoImage(file="pics/play.png")
playbutton = Button(buttonsframe, image=playbuttonImage, height=64, width=64, borderwidth=0, command=play_song)
playbutton.grid(row=0, column=2, padx=10, pady=10)

# Stop Button
stopbuttonImage = PhotoImage(file="pics/stop.png")
stopbutton = Button(buttonsframe, image=stopbuttonImage, height=64, width=64, borderwidth=0, command=stop_song)
stopbutton.grid(row=0, column=3, padx=10, pady=10)

# Forward Button
forwardImage = PhotoImage(file="pics/forward.png")
forwardbutton = Button(buttonsframe, image=forwardImage, height=64, width=64, borderwidth=0, command=forward_song)
forwardbutton.grid(row=0, column=4, padx=10, pady=10)

# Bring the info bar into existence
info_bar = Label(base, text="", bd=2, relief=RAISED)
info_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Define yt_dl function
def yt():
	finallink = link.get("1.0","end")
	return finallink

def yt_dl():
	finallink = yt()
	print("k")
	print(finallink)
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


enter_url = Text(main, borderwidth=0)
enter_url.insert(INSERT, "Enter a youtube video URL in the following box")
enter_url.insert(INSERT, "\nTo convert it to audio and download it.")
enter_url.insert(INSERT, "\nAfter entering URL, Hit Parse URL and then Convert and Download")
enter_url.configure(height=3, state='disabled')
enter_url.grid(row=4, column=0, pady=10)

link = Text(base, bg="black", fg="red")
link.configure(height=1)
link.pack()
readlink = Button(base, text="Parse URL", command=yt)
readlink.pack()
ytdl_button = Button(base, text="Convert and Download", command=yt_dl)
ytdl_button.pack()

# Set app icon
icon = PhotoImage(file="pics/icon.png")
base.iconphoto(True, icon)

base.mainloop()