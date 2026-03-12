import tkinter as tk
from PIL import Image, ImageTk
import random
from tkinter import messagebox as mbox


class HangmanApp(tk.Tk):

    def __init__(self, bg_path, hangman_paths, title_path, blankSpace_path, missedLetter_Path):
        super().__init__()

        self.title("Western Hangman, YeeHaw!")
        self.geometry("800x600")

        self.word_anchor_x_ratio = 0.58
        self.word_anchor_y_ratio = 0.35

        # =========================
        # WORD LIST
        # =========================
        self.words = [
            "COWBOY",
            "DESERT",
            "SALOON",
            "HORSE",
            "SHERIFF",
            "CACTUS",
            "WAGON",
            "MUSTANG",
            "SADDLE",
            "OUTLAW",
            "HOLSTER",
            "REVOLVER"
        ]

        self.word = random.choice(self.words)
        self.guessed_letters = set()
        self.wrong_guesses = 0

        # =========================
        # Load Images
        # =========================
        self.bg_original = Image.open(bg_path).convert("RGBA")
        self.title_original = Image.open(title_path).convert("RGBA")
        self.blankSpace_original = Image.open(blankSpace_path).convert("RGBA")
        self.missedLetters = Image.open(missedLetter_Path).convert("RGBA")

        self.hangman_original = [
            Image.open(path).convert("RGBA") for path in hangman_paths
        ]

        self.stage = 0

        # =========================
        # Canvas
        # =========================
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # =========================
        # Canvas Image Layers
        # =========================
        self.bg_item = self.canvas.create_image(0, 0, anchor="nw")
        self.title_item = self.canvas.create_image(0, 0, anchor="center")
        self.missedLetters_item = self.canvas.create_image(0, 0, anchor="center")
        self.hangman_item = self.canvas.create_image(0, 0, anchor="center")

        # guessed letters display
        self.guess_item = self.canvas.create_text(
            1280, 170,
            text="",
            font=("Goudy Old Style", 24),
            fill="black",
            anchor='nw',
        )

        # result text
        self.result_item = self.canvas.create_text(
            400, 350,
            text="",
            font=("Courier", 40, "bold"),
            fill="black",
            anchor='nw',
        )

        # blank tile storage
        self.blank_tiles = []
        self.letter_items = []

        # =========================
        # Bind Resize
        # =========================
        self.bind("<Configure>", self.on_resize)

        # =========================
        # Keyboard Input
        # =========================
        self.bind("<Key>", self.key_pressed)

        self.update_word_display()


    # =========================
    # Draw Wood Tiles
    # =========================
    def update_word_display(self):

        for tile in self.blank_tiles:
            self.canvas.delete(tile)

        for letter in self.letter_items:
            self.canvas.delete(letter)

        self.blank_tiles.clear()
        self.letter_items.clear()

        width = self.winfo_width()
        height = self.winfo_height()

        tile_width = max(40, int(width * 0.07))
        tile_height = tile_width
        spacing = int(tile_width * 0.2)

        word_length = len(self.word)

        anchor_x = int(width * self.word_anchor_x_ratio)
        anchor_y = int(height * self.word_anchor_y_ratio)

        start_x = anchor_x - ((tile_width + spacing) * word_length // 2)
        y = anchor_y

        resized_blank = self.blankSpace_original.resize(
            (tile_width, tile_height),
            Image.LANCZOS
        )

        self.tk_blank = ImageTk.PhotoImage(resized_blank)

        for i, letter in enumerate(self.word):

            x = start_x + i * (tile_width + spacing)

            tile = self.canvas.create_image(
                x,
                y,
                image=self.tk_blank,
                anchor="nw"
            )

            self.blank_tiles.append(tile)

            if letter in self.guessed_letters:
                letter_item = self.canvas.create_text(
                    x + tile_width // 2,
                    y - (tile_height * 0.000000000000001),
                    text=letter,
                    font=("Courier", int(tile_width * 0.7), "bold"),
                    fill="black"
                )
                
                self.letter_items.append(letter_item)

        guessed = "".join(sorted(self.guessed_letters))
        self.canvas.itemconfig(self.guess_item, text=guessed)


    # =========================
    # Handle Key Press
    # =========================
    def key_pressed(self, event):

        letter = event.char.upper()

        if not letter.isalpha():
            return

        if letter in self.guessed_letters:
            return

        self.guessed_letters.add(letter)

        if letter not in self.word:
            self.wrong_guesses += 1
            self.change_stage(self.wrong_guesses)

        self.update_word_display()
        self.check_game_over()


    # =========================
    # Win/Lose Check
    # =========================

    def winner_alert_and_close(self):
        mbox.showinfo("WINNER!", "You won the game!")
        app.destroy()
    
    def loser_alert_and_close(self):
        mbox.showinfo("LOSER!", "You lost the game.")
        app.destroy()

    def check_game_over(self):

        if all(l in self.guessed_letters for l in self.word):
            self.unbind("<Key>")
            self.winner_alert_and_close()

        if self.wrong_guesses >= len(self.hangman_original) - 1:
            self.unbind("<Key>")
            self.loser_alert_and_close()


    # =========================
    # Resize
    # =========================
    def on_resize(self, event):

        if event.width < 2 or event.height < 2:
            return

        resized_bg = self.bg_original.resize(
            (event.width, event.height),
            Image.LANCZOS
        )

        self.tk_bg = ImageTk.PhotoImage(resized_bg)
        self.canvas.itemconfig(self.bg_item, image=self.tk_bg)

        #Title

        title_width = int(event.width * 0.6)
        title_height = int(event.height * 0.2)

        resized_title = self.title_original.resize(
            (title_width, title_height),
            Image.LANCZOS
        )

        self.tk_title = ImageTk.PhotoImage(resized_title)

        self.canvas.itemconfig(self.title_item, image=self.tk_title)

        self.canvas.coords(
            self.title_item,
            event.width // 3.5,
            event.height // 7
        )

        #Missed Letters

        missedLetters_width = int(event.width * 0.3)
        missedLetters_height = int(event.height * 0.3)

        resized_missedLetters = self.missedLetters.resize(
            (missedLetters_width, missedLetters_height),
            Image.LANCZOS
        )

        self.tk_missedLetters = ImageTk.PhotoImage(resized_missedLetters)

        self.canvas.itemconfig(self.missedLetters_item, image=self.tk_missedLetters)

        self.canvas.coords(
            self.missedLetters_item,
            event.width // 1.42,
            event.height // 7
        )

        #Hangman

        hangman_size = int(min(event.width, event.height) * 0.4)

        resized_hangman = self.hangman_original[self.stage].resize(
            (hangman_size, hangman_size),
            Image.LANCZOS
        )

        self.tk_hangman = ImageTk.PhotoImage(resized_hangman)

        self.canvas.itemconfig(self.hangman_item, image=self.tk_hangman)

        self.canvas.coords(
            self.hangman_item,
            event.width // 1.8,
            event.height // 1.3
        )

        self.update_word_display()


    # =========================
    # Change Hangman Stage
    # =========================
    def change_stage(self, stage):

        if 0 <= stage < len(self.hangman_original):
            self.stage = stage

            width = self.winfo_width()
            height = self.winfo_height()

            hangman_size = int(min(width, height) * 0.4)

            resized_hangman = self.hangman_original[self.stage].resize(
                (hangman_size, hangman_size),
                Image.LANCZOS
            )

            self.tk_hangman = ImageTk.PhotoImage(resized_hangman)

            self.canvas.itemconfig(self.hangman_item, image=self.tk_hangman)


if __name__ == "__main__":

    hangman_stages = [
        f"C:/Users/rc3sk/OneDrive/Documents/School/hangmanStage{i}.png"
        for i in range(0, 8)
    ]

    app = HangmanApp(
        r"C:/Users/rc3sk/OneDrive/Documents/School/western-aesthetic.jpg",
        hangman_stages,
        r"C:/Users/rc3sk/OneDrive/Documents/School/Hangman-wordle App.png",
        r"C:/Users/rc3sk/OneDrive/Documents/School/wood.png",
        r"C:/Users/rc3sk/OneDrive/Documents/School/woodboard.png"
    )

    app.mainloop()

