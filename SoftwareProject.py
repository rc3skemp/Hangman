import tkinter as tk
from PIL import Image, ImageTk
import ttkbootstrap as tb
#Test

# pil_logo1 = Image.open(r"C:/Users/rc3sk/OneDrive/Documents/School/Hangman Structure.png").resize((400, 400))


class HangmanApp(tk.Tk):
    def __init__(self, image_path):
        super().__init__()

        self.title("Resizable Fade Background")
        self.geometry("800x600")

        # Load original image once
        self.original_image = Image.open(image_path).convert("RGBA")

        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Canvas image placeholders
        self.bg_item = self.canvas.create_image(0, 0, anchor="nw")
        # self.fade_item = self.canvas.create_image(0, 0, anchor="nw")

        self.current = 0
        self.resized_base = None

        # Detect window resize
        self.bind("<Configure>", self.on_resize)

        # self.fade_in()

        # self.packers_logo = ImageTk.PhotoImage(pil_logo1)
        # self.logo_label = tk.Label(root, image=self.packers_logo)
        # self.logo_label.grid(row=1, column=0, pady=(15, 5))

    # -----------------------------
    # Resize images with window
    # -----------------------------
    def on_resize(self, event):
        if event.width < 2 or event.height < 2:
            return

        # Resize image to window
        self.resized_base = self.original_image.resize(
            (event.width, event.height),
            Image.LANCZOS
        )

        # Background image
        self.tk_bg = ImageTk.PhotoImage(self.resized_base)
        self.canvas.itemconfig(self.bg_item, image=self.tk_bg)

    # -----------------------------
    # Fade overlay image
    # -----------------------------
    # def fade_in(self):
    #     if self.resized_base is not None and self.current_alpha <= 255:

    #         temp = self.resized_base.copy()
    #         temp.putalpha(self.current_alpha)

    #         self.tk_fade = ImageTk.PhotoImage(temp)
    #         self.canvas.itemconfig(self.fade_item, image=self.tk_fade)

    #         self.current_alpha += 5

    #     self.after(20, self.fade_in)


if __name__ == "__main__":

    # root = tb.Window()

    app = HangmanApp(
        "C:/Users/rc3sk/OneDrive/Documents/School/western-aesthetic.jpg"

    )

    app.mainloop()
