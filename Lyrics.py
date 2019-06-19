#! python3
from tkinter import *
import requests
from bs4 import BeautifulSoup


# takes an artist and song and finds the lyrics online
class LyricsScraper:

    def __init__(self):
        self.URL = ""
        self.lyrics = ""
        self.width = 0

    # formats the URL with the given artist and song name
    def make_url(self, artist, song):

        dashed_artist = artist.replace(" ", "-")
        dashed_song = song.replace(" ", "-")
        URL = "https://genius.com/" + dashed_artist + "-" + dashed_song + "-lyrics"
        self.URL = URL

    # grabs the lyrics from the given URL
    def make_lyrics(self):
        r = requests.get(self.URL)
        html = BeautifulSoup(r.text, "html.parser")
        try:
            lyrics = html.find("div", class_="lyrics").get_text()
            lyrics = lyrics.strip()
        except AttributeError:
            lyrics = "Lyrics not found"
        finally:
            self.lyrics = lyrics
            return lyrics

    def make_width(self):
        lines = self.lyrics.split("\n")
        self.width = 0
        for line in lines:
            if len(line) > self.width:
                self.width = len(line)

        return self.width


if __name__ == "__main__":

    ls = LyricsScraper()
    back_color = "#91959b"
    text_back = "#dadada"
    text_color = "#090909"
    highlight = "#2e9151"

    root = Tk()

    root.config(background=back_color)

    # uses Var for the variables changed within tkinter
    artist = StringVar(root)
    song = StringVar(root)
    lyrics = StringVar(root)
    width = IntVar()

    # on button press change lyrics
    def update():

        # update the lyrics and display them
        ls.make_url(artist.get(), song.get())
        ls.make_lyrics()
        lyrics_text.delete(1.0, END)
        lyrics_text.insert(END, ls.lyrics)

        # change window title and header
        root.title("Quick Lyrics: " + song.get().title() + " by " + artist.get().title())
        header.config(text=song.get().title() + " by " + artist.get().title())

        # change text width
        lyrics_text.config(width=ls.make_width() + 1)

    # song text box
    Label(root, text="Song", font="Calibri", background=back_color, fg=text_color).grid(row=2, column=1, sticky=W)
    song_entry = Entry(root, textvariable=song, font="Calibri", background=text_back, fg=text_color).grid(row=2, column=2, sticky=E)

    # artist text box
    Label(root, text="Artist", background=back_color, fg=text_color).grid(row=3, column=1,sticky=W)
    artist_entry = Entry(root, textvariable=artist, font="Calibri", background=text_back, fg=text_color).grid(row=3, column=2, sticky=E)

    # button calls update()
    update_button = Button(root, text="Update", command=update, font="Calibri", background=highlight, fg="white").grid(row=4, column=1, sticky=W)

    # displays the lyrics
    lyrics_text = Text(root,height=20, width=40, font="Calibri", background=text_back, fg=text_color)
    lyrics_text.grid(row=1, column=0, sticky=W)

    # scroll bar
    scrolly = Scrollbar(root, command=lyrics_text.yview, background=back_color)
    scrolly.grid(row=1, column=1, sticky='nsw')
    lyrics_text['yscrollcommand'] = scrolly.set

    # header
    header = Label(root, text="Song by Artist", font="Georgia 20", background=back_color, fg="black")
    header.grid(row=0,column=0, sticky="WE")
    Label(root, text="Lyrics from genius.com", background=back_color, fg=text_color).grid(row=0, column=2, sticky=W)

    # runs the display
    root.mainloop()

