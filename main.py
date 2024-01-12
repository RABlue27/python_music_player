import tkinter as tk
from tkinter import ttk
import os
from playsound import playsound
import time
from pygame import mixer

def on_next_click():
    selected_index = listbox.curselection()
    
    if selected_index:
        next_index = (selected_index[0] + 1) % listbox.size()
        listbox.selection_clear(0, tk.END)
        listbox.selection_set(next_index)
        listbox.activate(next_index)
        selected_item = listbox.get(next_index)
        print(f"Playing next item: {selected_item}")
        play_audio(selected_item)
    else:
        print("No item selected.")

def on_pause_click():
    if mixer.music.get_busy():
        mixer.music.pause()
        print("Playback paused.")
    else:
        mixer.music.unpause()
        print("Playback resumed.")

def on_slider_change(event):
    volume = slider.get() / 100.0
    mixer.music.set_volume(volume)
    print(f"Volume set to: {volume}")

def on_list_select(event):
    selected_item = listbox.get(listbox.curselection())
    print(f"Selected Item: {selected_item}")
    play_audio(selected_item)

def play_audio(song):
    music_folder = "music"
    file_path = os.path.join(music_folder, song)
    
    mixer.init()

    mixer.music.load(file_path)
    duration = mixer.Sound(file_path).get_length()

    progress_bar['maximum'] = duration
    progress_bar['value'] = 0

    mixer.music.play()

    update_progress_bar(duration)

def update_progress_bar(duration):
    for i in range(int(duration)):
        progress_bar['value'] = i + 1
        root.update()
        time.sleep(1)

def load_songs():
    music_folder = "music" 
    audio_formats = [".mp3", ".wav", ".ogg", ".flac"]
    songs = [file for file in os.listdir(music_folder) if any(file.endswith(format) for format in audio_formats)]
    return songs

def load_songs_to_listbox():
    songs = load_songs()
    listbox.delete(0, tk.END)
    listbox.insert(tk.END, *songs)

root = tk.Tk()
root.title("Audio player")

next_button = ttk.Button(root, text="Next", command=on_next_click)
next_button.pack(pady=10)

pause_button = ttk.Button(root, text="Pause", command=on_pause_click)
pause_button.pack(pady=10)

slider = ttk.Scale(root, from_=0, to=100, orient="horizontal", command=on_slider_change)
slider.pack(pady=10)

text_box = ttk.Entry(root)
text_box.pack(pady=10)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
progress_bar.pack(pady=10)

listbox = tk.Listbox(root, selectmode=tk.SINGLE)
listbox.bind('<<ListboxSelect>>', on_list_select)
listbox.pack(pady=10)

load_songs_to_listbox()

root.mainloop()
