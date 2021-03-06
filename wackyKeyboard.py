# from tkinter.ttk import * 
# from tkinter import *
# def add_one():
#     value.set(value.get()+1)

# def wow(event):
#     label2.config(text="WWWWOOOOWWWW")

# window = Tk()
# value = IntVar(0)
# label = Label(window, textvariable=value)
# label.pack()
# label2 = Label(window)
# label2.pack()
# button = Button(window, text="Add one", command=add_one)
# button.bind("<Shift-Double-Button-1>", wow)
# button.pack()
# window.mainloop()

# from tkinter import *
# from tkinter.ttk import * 
# def change(value, n):
#     value.set(value.get()+n)

# window = Tk()
# # initialise a variable to store the current counts
# value = IntVar(0)
# # display the value in the label widget
# label = Label(window, textvariable=value)
# label.pack()
# # initialise the button
# button = Button(window, text="Left +1, Right -1")
# # binding what each buttons do
# button.bind("<Button-1>", lambda event: change(value, 1))
# button.bind("<Button-2>", lambda event: change(value, -1))
# # pack the button into the window
# button.pack()
# # start app
# window.mainloop()

from tkinter import *
from tkinter.ttk import *
from random import random, choice
from time import time

#@@@@@@@@@@@@@ I N I T I A L I S E R S @@@@@@@@@@@@@
# root window
window = Tk()
start = time()

# base frameA
frameA = Frame(window)
frameA.pack()

# second frameB
frameB = Frame(frameA)
frameB.pack()

# generate random strings
generate_random_strings = 'abcdefghijklmnopqrstuvwxyz'
correct_strings = []
for i in range(0, 6):
    temp = ''
    for j in range(0,6):
        temp += choice(generate_random_strings)

    correct_strings.append(temp)


# correct_strings =  ["lambda",
#                     "heroic",
#                     "legacy",
#                     "hyphen",
#                     "syntax",
#                     "teapot"]

# keyboard layout
board = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']

# globals
STRING = 0
INDEX = 0
IS_DYNAMIC = False

data = StringVar()
data.set(correct_strings[STRING][INDEX])

''' frames '''
# entry widget into frameB
entry = Entry(frameB, textvariable=data, width=40)
entry.pack(side="left")

# clear button into frameB
# clearBtn = Button(frameB, text="Clear", command=lambda: btn_clear(data))
# clearBtn.pack(side="left")

# counts for use with the log fn
counts = []

# dynamic keyboard toggle
toggleBtn = Checkbutton(frameB, text="Dynamic", command=lambda: btn_dynamic(IS_DYNAMIC))
toggleBtn.pack()

''' base keyboard frame '''
baseKBFrame = Frame(frameA, relief=RAISED)


#@@@@@@@@@@@@@@@@@@ M E T H O D S @@@@@@@@@@@@@@@@@@
# def btn_clear(data):
#     data.set("")

def btn_dynamic(toggle):
    global IS_DYNAMIC
    global baseKBFrame
    global board

    IS_DYNAMIC = not toggle
    if IS_DYNAMIC:
        for i in range(len(board)):
            joiner = ''
            shuffled_list = sorted(board[i], key=lambda shuffle: random())
            board[i] = joiner.join(shuffled_list)
        # forget and destroy existing frame
        baseKBFrame.pack_forget()
        baseKBFrame.destroy()
        # create new frame
        baseKBFrame = Frame(frameA, relief=RAISED)
        create_keys()
    else:
        board = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']
        # forget and destroy existing frame
        baseKBFrame.pack_forget()
        baseKBFrame.destroy()
        # create new frame
        baseKBFrame = Frame(frameA, relief=RAISED)
        create_keys()

def is_correct(word):
    global INDEX
    global STRING
    global IS_DYNAMIC
    global start

    toggleBtn.config(state=DISABLED)

    if IS_DYNAMIC:
        IS_DYNAMIC = not IS_DYNAMIC
        btn_dynamic(IS_DYNAMIC)

    if (INDEX < 6 and word == entry.get()):
        total_time = (time() - start) * 1000
        log(total_time, word)
        start = time() # restart clock
        if INDEX == 5: # if end of the word, go to next
            INDEX = 0
            STRING += 1
            if STRING != 6:
                data.set(correct_strings[STRING][INDEX])
            else:
                window.destroy()
            
        elif word == entry.get(): # else keep incrementing
            INDEX += 1
            data.set(correct_strings[STRING][INDEX]) 


def log(time, word):
    global IS_DYNAMIC
    global counts

    static = ''

    counts.append(word)

    if IS_DYNAMIC:
        static = "dynamic"
    else:
        static = "static"

    file = open("experiment_" + static + "_log.txt", 'a')
    file.write("Sam " + static + " " + word + " " + str(counts.count(word)) + " " + str(round(time, 1)) + "\n")



def create_keys():
    global board

    baseKBFrame.pack(padx=5, pady=5)
    for eachLine in board:
        lineFrame = Frame(baseKBFrame) # generate a frame for each line in the board
        lineFrame.pack(padx=5, pady=2)
        for eachWord in eachLine:
            btnFrame = Frame(lineFrame, relief=RIDGE)
            btn = Button(btnFrame, text=eachWord, width=1, command=lambda x=eachWord: is_correct(x))
            btn.pack(padx=1, side="left")        
            btnFrame.pack(side="left", padx=2, pady=5)        

create_keys()

start = time()

# start app
window.mainloop()