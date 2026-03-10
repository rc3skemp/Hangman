import tkinter as tk
from PIL import Image, ImageTk

class HangmanApp(tk.Tk):

    def __init__(self, bg_path, hangman_paths, title_path):
        super().__init__()

        self.title("Western Hangman, YeeHaw!")
        self.geometry("800x600")

        # -------------------------
        # Load Images
        # -------------------------
        self.bg_original = Image.open(bg_path).convert("RGBA")
        self.title_original = Image.open(title_path).convert("RGBA")

        self.hangman_original = [
            Image.open(path).convert("RGBA") for path in hangman_paths
        ]

        self.stage = 0

        # -------------------------
        # Canvas
        # -------------------------
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # -------------------------
        # Canvas Image Layers
        # -------------------------
        self.bg_item = self.canvas.create_image(0, 0, anchor="nw")
        self.title_item = self.canvas.create_image(0, 0, anchor="center")
        self.hangman_item = self.canvas.create_image(0, 0, anchor="center")

        # -------------------------
        # Bind Resize
        # -------------------------
        self.bind("<Configure>", self.on_resize)

        # -------------------------
        # Bind Keys for testing
        # -------------------------
        for i in range(8):
            self.bind(str(i+1), lambda e, s=i: self.change_stage(s))


    def on_resize(self, event):

        if event.width < 2 or event.height < 2:
            return

        # =========================
        # Background
        # =========================
        resized_bg = self.bg_original.resize(
            (event.width, event.height),
            Image.LANCZOS
        )

        self.tk_bg = ImageTk.PhotoImage(resized_bg)
        self.canvas.itemconfig(self.bg_item, image=self.tk_bg)

        # =========================
        # Title
        # =========================
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
            event.width // 2,
            event.height // 6
        )

        # =========================
        # Hangman Image
        # =========================
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


    def change_stage(self, stage):
        if 0 <= stage < len(self.hangman_original):
            self.stage = stage

            # get current window size
            width = self.winfo_width()
            height = self.winfo_height()

            # manually update hangman image
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
        r"C:/Users/rc3sk/OneDrive/Documents/School/Hangman-wordle App.png"
    )

    app.mainloop()
