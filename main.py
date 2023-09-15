from tkinter import *
import pandas as pd
import random
import os

BG_COLOR = "#b1ddc6"
english_word = ""
french_word = ""
knows = {}

# -------------------------------------------- FETCH READ DATASET -------------------------------------------------------- #


# def get_words():
#     if os.path.isfile("words_to_learn.csv"):
#         return pd.read_csv("words_to_learn.csv").to_dict("records")
#     else:
#         return pd.read_csv("french_to_english.csv").to_dict("records")
#
#
# WORDS = get_words()

try:
    WORDS = pd.read_csv("words_to_learn.csv").to_dict("records")
except FileNotFoundError:
    WORDS = pd.read_csv("french_to_english.csv").to_dict("records")


# -------------------------------------------- FETCH RANDOM WORDS -------------------------------------------------------- #
def select_word():
    global WORDS, flip_timer, english_word, french_word, knows
    window.after_cancel(flip_timer)
    rows_count = len(WORDS)
    random_row = random.randint(0, rows_count)
    french_word = WORDS[random_row]["French"]
    english_word = WORDS[random_row]["English"]
    if english_word in knows:
        select_word()
    else:
        knows = {"French": french_word, "English": english_word}
        canvas.itemconfig(canvas_image, image=card_front_img)
        canvas.itemconfig(title_front, text="French", fill="black")
        canvas.itemconfig(word_front, text=french_word, fill="black")
        flip_timer = window.after(3000, back)


def back():
    canvas.itemconfig(canvas_image, image=card_back_img)
    canvas.itemconfig(title_front, text="English", fill="white")
    canvas.itemconfig(word_front, text=english_word, fill="white")


def ok_clicked():
    global WORDS
    if knows in WORDS:
        WORDS.remove(knows)
    pd.DataFrame(WORDS).to_csv("words_to_learn.csv", index=False)

    select_word()


# ------------------------------------------------------ UI -------------------------------------------------------- #
window = Tk()
window.title("Flash Card Game")
window.config(padx=50, pady=50, bg=BG_COLOR)
window.minsize(width=200, height=200)
flip_timer = window.after(3000, back)

# --------------------- Images --------------------------- #
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
ok_image = PhotoImage(file="./images/right.png")
cancel_image = PhotoImage(file="./images/wrong.png")

# --------------------- Canvas -------------------------- #
canvas = Canvas(width=800, height=526, bg=BG_COLOR, borderwidth=0, highlightthickness=0)
canvas_image = canvas.create_image(400, 263, image=card_front_img)
title_front = canvas.create_text(400, 180, text="Title", fill="blue", font=("Arial", 40, "italic"))
word_front = canvas.create_text(400, 300, text="Word", fill="Black", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# --------------------- Buttons ----------------------------- #
ok_button = Button(image=ok_image, borderwidth=0, highlightthickness=0, command=ok_clicked)
ok_button.grid(row=1, column=0)

cancel_button = Button(image=cancel_image, borderwidth=0, highlightthickness=0, command=select_word)
cancel_button.grid(row=1, column=1)

window.mainloop()
