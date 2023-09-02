import sys
from tkinter import *
from tkinter import messagebox
import numpy as np
import countries_list
import settings
import utils

window = Tk()

'''Overwriting the default settings of the window'''
window.configure(bg='black')
window.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')
window.title('WORDLE Game')
window.resizable(True, True)
windowWidth = window.winfo_reqwidth()
windowHeight = window.winfo_reqheight()
positionRight = int(window.winfo_screenwidth() / 3 - windowWidth / 3)
positionDown = int(window.winfo_screenheight() / 3 - windowHeight / 3)
window.geometry('+{}+{}'.format(positionRight, positionDown))

input_word = StringVar()

'''Instantiating different frames of the window'''
right_frame = Frame(
    window,
    bg = 'white',
    width = utils.width_prct(settings.WIDTH, 50),
    height = settings.HEIGHT
)
left_top_frame = Frame(
    window,
    bg = 'black',
    width = utils.width_prct(settings.WIDTH, 50),
    height = utils.height_prct(settings.HEIGHT, 50)
)
left_entry_frame = Frame(
    window,
    bg = 'black',
    width = utils.width_prct(left_top_frame.winfo_reqwidth(), 75),
    height = utils.height_prct(left_top_frame.winfo_reqheight(), 75),
)
left_bottom_frame = Frame(
    window,
    bg = 'black',
    width = utils.width_prct(settings.WIDTH, 50),
    height = utils.height_prct(settings.HEIGHT, 50)
)

'''Placing the frames on the window'''
right_frame.place(x = utils.width_prct(settings.WIDTH, 50), y = 0)
left_top_frame.place(x = 0, y = 0)
left_bottom_frame.place(x = 0, y = utils.height_prct(settings.HEIGHT, 50))
left_entry_frame.place(x = utils.width_prct(left_top_frame.winfo_reqwidth(), 25), y = utils.height_prct(left_top_frame.winfo_reqheight(), 25))

'''Placing the input field for the entered word'''
word_label = Label(left_entry_frame, text = 'Type the country guess in the box below:', font = ('calibre', 10))
word_entry = Entry(left_entry_frame, textvariable = input_word, font=('calibre', 15))
word_label.grid(row = 0, column = 0)
word_entry.grid(row = 2, column = 0)

'''Message box object used to keep the count of the attempts on screen'''
msg = Label(left_top_frame, text = 'Current attempts: 6', font = ('calibre', 10))
msg.grid(row = 3, column = 0)

'''##############Validation process settings##############'''
number_of_attempts = 0

'''Storing all 5 letter countries'''
all_countries = countries_list.get_all_countries()
all_np = np.array(list(all_countries))
all_arr = [item for item in enumerate(all_np)]

'''Storing the randomly picked country'''
random_word = countries_list.get_country()
random_np = np.array(list(random_word))
random_arr = [item for item in enumerate(random_np)]

tried_all_countries = []

prioritize_error = False
user_has_won = False

'''This method gets called whenever the user clicks the Play button'''
def play():


    global random_word, number_of_attempts, msg, word_entry, all_entered_words, tried_all_countries, prioritize_error, user_has_won
    print(f'<!>For testing purposes<!>\nCorrect word: {random_word}')
    input_word = word_entry.get()

    if user_has_won:
        messagebox.showinfo('Not so fast.', f'You already won. \nThe word was: {random_word}')
        return

    '''Verifying the input_word is a valid country'''
    is_valid_country = False

    for index, country in all_arr:
        if str(country).lower() == input_word.lower():
            is_valid_country = True

    if str(input_word) in tried_all_countries and not prioritize_error:
        messagebox.showwarning('Invalid entry.', f'You tried {input_word} before.')
        return

    if is_valid_country: number_of_attempts += 1

    tried_all_countries.append(str(input_word))

    msg.config(text=f'Current attempts: {6 - number_of_attempts}')

    if number_of_attempts <= 6:
        if len(input_word) == 5:
            if is_valid_country:
                if input_word.lower() == random_word.lower():
                    for index, letter in enumerate(input_word):
                        lbl = Label(right_frame, text = letter.upper(), width = int(settings.WIDTH /2 /5 /10))
                        lbl.grid(
                            row = number_of_attempts, column = index,
                            padx = 9, pady = 10
                        )
                        lbl.config(bg = 'green')

                    user_has_won = True
                    messagebox.showinfo('Correct!!', f'The word was: {random_word}.\nPress Play again / Skip country to play again.')
                else:
                    '''Setting up each label object that corresponds to each letter from the input'''
                    letters_arr = [letter for [i, letter] in enumerate(input_word)]
                    app_number_arr = [random_word.lower().count(letter.lower()) for [i, letter] in enumerate(input_word)]


                    colors_arr = [None] * 5

                    print(f'Appereance number for each letter:')
                    for i, item in enumerate(app_number_arr):
                        print(f'Letter {input_word[i]}: {item} appereances')

                    mark_letter = [None] * 5

                    #for index, letter in enumerate(input_word):
                    #    if letter.lower() == random_word[index].lower():
                    #        colors_arr[index] = 'green'
                    #    if letter.lower() in random_word.lower() and not letter.lower() == random_word[index].lower():




                    for index, letter in enumerate(input_word):
                        lbl = Label(right_frame, text = letter.upper(), width = int(settings.WIDTH /2 /5 /10))
                        lbl.grid(
                            row = number_of_attempts, column = index,
                            padx = 9, pady = 10
                        )

                        if letter.lower() == random_word[index].lower():
                            lbl.config(bg = 'green')
                        if letter.lower() in random_word.lower() and not letter.lower() == random_word[index].lower():
                            lbl.config(bg = 'orange')
                        if letter.lower() not in random_word.lower():
                            lbl.config(bg = 'grey')

                    if number_of_attempts == 6:
                        prioritize_error = True
                        messagebox.showerror('You lost', f'The word was: {random_word}')
                        return
            else:
                messagebox.showwarning('Invalid entry.', 'Please enter a valid country name.')
                return
        else:
            messagebox.showwarning('5 Characters needed.', 'Please use only 5 characters.')
            return
    else:
        msg.config(text=f'Current attempts: 0')
        messagebox.showerror('You lost', f'The word was: {random_word}')



'''This method gets called whenever the user clicks the Play again/Skip country button'''
def skip():


    global number_of_attempts, input_word, msg, user_has_won, tried_all_countries
    global random_word, random_np, random_arr

    user_has_won = False
    number_of_attempts = 0
    tried_all_countries = []

    for item in right_frame.winfo_children():
        item.destroy()

    random_word = countries_list.get_country()
    random_np = np.array(list(random_word))
    random_arr = [item for item in enumerate(random_np)]

    msg.config(text = 'Current attempts: 6')

    input_word.set("")




'''Instantiating submit button'''
submit_btn = Button(
    left_bottom_frame,
    width = 15,
    height = 4,
    text = 'Play',
    command = play
)

'''Instantiating skip button'''
skip_word_btn = Button(
    left_bottom_frame,
    width = 15,
    height = 4,
    text = 'Play again/\nSkip country',
    command = skip
)

'''Adding the buttons in the window'''
submit_btn.grid(row = 0, column = 0)
skip_word_btn.grid(row = 1, column = 0)

'''Running main window'''
window.mainloop()