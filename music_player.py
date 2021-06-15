from tkinter import *
import random
import mutagen
import pygame
from mutagen.mp3 import MP3
from tkinter import filedialog, ttk
import re
import time
import eyed3

root = Tk()
root.title('Rythmic Mp3 player')
root.resizable(height=False, width=False)
root.configure(background='#1c383d')
root.geometry("700x400")
#root.iconbitmap('images/play_1.png')

# for dynamic background
random_bg = random.randint(1, 4)
song_length = 0

canvas = Canvas(root, width=700, height=400, bg="#1c383d", bd=0, highlightthickness=0)

BACKGROUND = PhotoImage(file="images/logo.png")
my_bck = canvas.create_image(0, 0, image=BACKGROUND, anchor=NW)

current_song = False
pygame.mixer.init()
song_locator_diary = {}
theme_is_changed = False

# add many songs
def add_many_songs():
    global theme_is_changed
    global sorted_song, song_locator_diary, my_bck, BACKGROUND
    songs = filedialog.askopenfilenames(initialdir='music/', title="choose a song", filetypes=(("mp3 Files", "*.mp3"),))
    for song in songs:
        sorted_song = re.split(': |/|.mp3', song)
        song_box.insert(END, sorted_song[-2])
        song_locator_diary[sorted_song[-2]] = song
    if not theme_is_changed:
        print(theme_is_changed)
        BACKGROUND = PhotoImage(file="images/floral.png")
        my_bck = canvas.create_image(-300, 0, image=BACKGROUND, anchor=NW)


def play():
    global isplaying, current_song, about__to_play, current_time
    current_time = 0
    seek.set(0)
    try:
        current_time_lbl.after_cancel(clock)
    except:
        pass
    is_song_selected = song_box.curselection()
    # as initialy the first song is active after add song to list .so this check
    if is_song_selected != ():
        get_song = song_box.get(ACTIVE)
        if get_song != "":
            # get original file location and name
            about__to_play = song_locator_diary[get_song]
            pygame.mixer.music.load(about__to_play)
            pygame.mixer.music.play(loops=0)
            # queing_next_song()

            current_song = song_box.curselection()

            get_song_info(about__to_play)
            get_current_time()
            seek.config(to=song_length)


def pause():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()

    else:
        pygame.mixer.music.unpause()


def stop():
    current_time_lbl.after_cancel(clock)
    pygame.mixer.music.stop()
    seek.set(0)
    # song_box.selection_clear(ACTIVE)
    current_time_lbl.config(text="00:00")


# def rewind1():
#     next_music_no = song_box.curselection()
#     # initially no music is selected and playing then pressing this throw error
#     if next_music_no != () and next_music_no[0]!=0:
#         next_music_no = next_music_no[0] - 1
#         next_music = song_box.get(next_music_no)
#         about__to_play = song_locator_diary[next_music]
#         pygame.mixer.music.load(about__to_play)
#         pygame.mixer.music.play(loops=0)
#         # change active bar
#         song_box.selection_clear(0, END)
#         # activate the bar to next song
#         song_box.activate(next_music_no)
#         song_box.selection_set(next_music_no, last=None)
#         print(next_music_no)


# def forword1():
#     next_music_no = song_box.curselection()
#     # initially no music is selected and playing then pressing this throw error
#     if next_music_no != False and next_music_no[-1]!=len(song_locator_diary) - 1:
#         next_music_no = next_music_no[0] - 1
#         next_music = song_box.get(next_music_no)
#         about__to_play = song_locator_diary[next_music]
#         pygame.mixer.music.load(about__to_play)
#         pygame.mixer.music.play(loops=0)
#         # change active bar
#         song_box.selection_clear(0, END)
#         # activate the bar to next song
#         song_box.activate(next_music_no)
#         song_box.selection_set(next_music_no, last=None)
#         print(next_music_no)

# def queing_next_song():
#     global current_song
#     if current_song != False and current_song[-1] != len(song_locator_diary) - 1:
#         temp1 = current_song
#         temp1 = temp1[0] + 1
#         next_music = song_box.get(temp1)
#         about__to_play = song_locator_diary[next_music]
#         pygame.mixer.music.queue(about__to_play)
#         print(about__to_play)


def check_if_finished(slide_time=0):
    global current_time, song_length

    if int(current_time) + 1 >= int(song_length) or int(slide_time) + 1 >= int(song_length):
        current_time_lbl.config(text="00:00")
        seek.set(0)
        print("hello")
        forword()


def forword():
    global current_song
    if current_song != False and current_song[-1] != len(song_locator_diary) - 1:
        temp1 = current_song
        temp1 = temp1[0] + 1
        next_music = song_box.get(temp1)
        about__to_play = song_locator_diary[next_music]
        pygame.mixer.music.load(about__to_play)
        pygame.mixer.music.play(loops=0)
        # change active bar
        song_box.selection_clear(0, END)
        song_box.activate(temp1)
        song_box.selection_set(temp1, last=None)
        current_song = song_box.curselection()
        get_song_info(about__to_play)
        seek.set(0)


def rewind():
    global current_song
    if current_song != False and current_song[0] != 0:
        temp1 = current_song
        temp1 = temp1[0] - 1
        next_music = song_box.get(temp1)
        about__to_play = song_locator_diary[next_music]
        pygame.mixer.music.load(about__to_play)
        pygame.mixer.music.play(loops=0)
        # change active bar
        song_box.selection_clear(0, END)
        song_box.activate(temp1)
        song_box.selection_set(temp1, last=None)
        current_song = song_box.curselection()
        get_song_info(about__to_play)
        seek.set(0)


def delete_playlist():
    global title, artist, album, current_song, my_bck, current_time, about_to_play, BACKGROUND
    pygame.mixer.music.stop()
    song_box.delete(0, END)
    # clear the dictionary
    song_locator_diary.clear()
    current_song = False
    canvas.delete(title)
    canvas.delete(artist)
    canvas.delete(album)
    seek.set(0)
    current_time = 0
    # BACKGROUND = PhotoImage(file="images/logo.png")
    # my_bck = canvas.create_image(0, 0, image=BACKGROUND, anchor=NW)
    # canvas.pack()


def delete_song():
    # if its playing do not delete
    global current_song, song_locator_diary, isplaying
    if len(song_locator_diary):
        x = song_box.get(ACTIVE)
        if pygame.mixer.music.get_busy():
            delete_it = song_box.get(current_song[0])
            if delete_it != x:
                # REMOVE IT FROM DICTIONAY
                del song_locator_diary[x]
                song_box.delete(ACTIVE)
        else:
            del song_locator_diary[x]
            song_box.delete(ACTIVE)
    stop()
    if len(song_locator_diary) == 0:
        delete_playlist()


# get current time of song
l = 0


def get_current_time():
    global clock, current_time, l, slide_time

    current_time = 0
    slide_time = 0
    if int(seek.get() + 1) == int(pygame.mixer.music.get_pos() / 1000):
        current_time = pygame.mixer.music.get_pos() / 1000
        print(current_time, seek.get())
        temp_current_time = time.strftime('%M:%S', time.gmtime(current_time))
        current_time_lbl.config(text=temp_current_time)
        seek.set(current_time)
    else:
        # current_time = pygame.mixer.music.get_pos() / 1000
        if pygame.mixer.music.get_busy():
            slide_time = seek.get() + 1
            temp_current_time = time.strftime('%M:%S', time.gmtime(slide_time))
            current_time_lbl.config(text=temp_current_time)
            seek.set(slide_time)
    check_if_finished(slide_time)

    clock = current_time_lbl.after(1000, get_current_time)


def get_song_info(about__to_play):
    global song_length
    try:
        temp_song_info = mutagen.File(about__to_play)
        song_length = temp_song_info.info.length
        temp_song_length = time.strftime('%M:%S', time.gmtime(song_length))
        song_time_lbl.config(text=temp_song_length)
    except:
        pass
    audio = eyed3.load(about__to_play)
    song_details = {"Title:": audio.tag.title, "Artist:": audio.tag.artist, "Album:": audio.tag.album}

    update_title_artist_album(song_details)


def update_title_artist_album(song_details):
    global title, artist, album
    canvas.delete(title)
    canvas.delete(artist)
    canvas.delete(album)
    title = canvas.create_text(190, 140, text=" Title :{}".format(song_details['Title:']), fill="#ebf8ff",
                               font=('Helvetica 10 bold'))
    artist = canvas.create_text(190, 160, text=" Artist :{}".format(song_details['Artist:']), fill="#d1efff",
                                font=('Helvetica 9 '))
    album = canvas.create_text(190, 180, text=" Album :{}".format(song_details['Album:']), fill="#fff8e3",
                               font=('Helvetica 8 '))


def change_theme(thms):
    global BACKGROUND, about__to_play, my_bck,theme_is_changed
    if thms == 7:
        BACKGROUND = PhotoImage(file="images/cycle.png")
        my_bck = canvas.create_image(0, 0, image=BACKGROUND, anchor=NW)
    elif thms == 6:
        BACKGROUND = PhotoImage(file="images/love.png")
        my_bck = canvas.create_image(-20, 30, image=BACKGROUND, anchor=NW)
    elif thms == 5:
        BACKGROUND = PhotoImage(file="images/guiter.png")
        my_bck = canvas.create_image(0, 0, image=BACKGROUND, anchor=NW)
    elif thms == 4:
        BACKGROUND = PhotoImage(file="images/spark.png")
        my_bck = canvas.create_image(0, 0, image=BACKGROUND, anchor=NW)
    elif thms == 3:
        BACKGROUND = PhotoImage(file="images/disk.png")
        my_bck = canvas.create_image(-250, 0, image=BACKGROUND, anchor=NW)
    elif thms == 2:
        BACKGROUND = PhotoImage(file="images/floral.png")
        my_bck = canvas.create_image(-300, 0, image=BACKGROUND, anchor=NW)
    elif thms == 1:
        BACKGROUND = PhotoImage(file="images/abstract.png")
        my_bck = canvas.create_image(-70, 0, image=BACKGROUND, anchor=NW)

    else:
        BACKGROUND = PhotoImage(file="images/vintage.png")
        my_bck = canvas.create_image(0, -50, image=BACKGROUND, anchor=NW)
    try:
        theme_is_changed =True
        get_song_info(about__to_play)
    except:
        pass


def vol_control(event):
    pygame.mixer.music.set_volume(vol_slide.get() / 10)


def seek_control(event):
    global current_time, clock, l
    # current_time_lbl.after_cancel(clock)
    current_time = seek.get()
    seek.set(seek.get())
    # print(current_time)
    pygame.mixer.music.set_pos(seek.get())
    l = 100
    # get_current_time()


# create plalist box
song_box = Listbox(root, fg="white", width=50, height=20, bg="#1c383d", selectforeground="#e6f5ff", font="Helvetica 8",
                   selectbackground="#36789e", bd=10, highlightthickness=0, relief='flat')
song_box.pack(side=LEFT)

# create a song seek slider
# seek = ttk.Scale(root,orient=HORIZONTAL,length=295,value=0,command="seek_song")
seek = Scale(root, orient=HORIZONTAL, width=8, bd=0, highlightthickness=0, length=185, showvalue=0, bg="#1c383d",
             fg="yellow", troughcolor="#36789e", variable=0)
seek.place(anchor='sw', x=12, y=382)

# #create volume silder
vol_lbl = Label(root, text="Vol", bg="#1c383d", fg='#e6f5ff')
vol_lbl.place(x=210, y=368)
vol_slide = Scale(root, orient=HORIZONTAL, to=10, width=8, bd=0, highlightthickness=0, length=85, bg="#1c383d",
                  fg="yellow", troughcolor="#e6f5ff", showvalue=0, command="vol_control")
vol_slide.set(10)
vol_slide.place(anchor='se', x=320, y=382)

# create music control button
PLAY_IMG = PhotoImage(file="images/play_1.png")
PAUSE_IMG = PhotoImage(file="images/pause.png")
STOP_IMG = PhotoImage(file="images/stop.png")
FORWARD_IMG = PhotoImage(file="images/forword.png")
REWIND_IMG = PhotoImage(file="images/rewind.png")

control_frame = Frame(root)
control_frame.config(bg="#1c383d")
control_frame.pack(side=BOTTOM, pady=5)

play_btn = Button(control_frame, image=PLAY_IMG, bg="#1c383d", borderwidth=0, command=play)
pause_btn = Button(control_frame, image=PAUSE_IMG, bg="#1c383d", borderwidth=0, command=pause)
stop_btn = Button(control_frame, image=STOP_IMG, bg="#1c383d", borderwidth=0, command=stop)
forward_btn = Button(control_frame, image=FORWARD_IMG, bg="#1c383d", borderwidth=0, command=forword)
rewind_btn = Button(control_frame, image=REWIND_IMG, bg="#1c383d", borderwidth=0, command=rewind)
song_time_lbl = Label(control_frame, text="", bg="#1c383d", fg="#d1efff")
current_time_lbl = Label(control_frame, text="", bg="#1c383d", fg="#d1efff")

title = canvas.create_text(150, 140, text=" ", fill="#ffff51", font=('Helvetica 10 bold'))
artist = canvas.create_text(150, 160, text=" ", fill="#7d0051", font=('Helvetica 9'))
album = canvas.create_text(150, 180, text=" ", fill="#7d0051", font=('Helvetica 8 '))
play_btn.grid(row=0, column=3, padx=10)
pause_btn.grid(row=0, column=2, padx=10)
stop_btn.grid(row=0, column=4, padx=10)
forward_btn.grid(row=0, column=5, padx=10)
rewind_btn.grid(row=0, column=1, padx=10)
song_time_lbl.grid(row=0, column=6, padx=10)
current_time_lbl.grid(row=0, column=0, padx=10)

# create menu
my_menu = Menu(root)
root.config(menu=my_menu)
add_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="add_song", menu=add_song_menu)
# add_song_menu.add_command(label = "add one song" ,command=add_song)
add_song_menu.add_command(label="add many song", command=add_many_songs)

# delete song menu
remove_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Remove songs", menu=remove_song_menu)
remove_song_menu.add_command(label="delete song", command=delete_song)
remove_song_menu.add_command(label="delete playlist", command=delete_playlist)

change_theme_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Themes", menu=change_theme_menu)
change_theme_menu.add_command(label="Abstract", command=lambda: change_theme(1))
change_theme_menu.add_command(label="Floral", command=lambda: change_theme(2))
change_theme_menu.add_command(label="Disk", command=lambda: change_theme(3))
change_theme_menu.add_command(label="Spark", command=lambda: change_theme(4))
change_theme_menu.add_command(label="Guiter", command=lambda: change_theme(5))
change_theme_menu.add_command(label="Love", command=lambda: change_theme(6))
change_theme_menu.add_command(label="Vintage", command=lambda: change_theme(8))
change_theme_menu.add_command(label="Street", command=lambda: change_theme(7))
canvas.pack()
# w = Scale(control_frame, from_=0, to=200, orient=HORIZONTAL)
# w.grid(row=0,column=0,columnspan=2)
vol_slide.bind("<Button-1>", vol_control)
vol_slide.bind('<Motion>', vol_control)
seek.bind("<Button-1>", seek_control)
seek.bind('<ButtonRelease>', seek_control)

root.mainloop()
