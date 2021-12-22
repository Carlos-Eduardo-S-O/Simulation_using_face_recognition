import sys
from time import sleep
# Control variables 
TYPE_SPEED = 0.06

def typewriter_colorful(msg, color):
    for caracter in msg:
        if color == 1: #green
            sys.stdout.write(f"\033[32m{caracter}\033[m")
            sys.stdout.flush()
        else: # red
            sys.stdout.write(f"\033[31m{caracter}\033[m")
            sys.stdout.flush()
        seconds = TYPE_SPEED
        sleep(seconds)
    print()

def typewriter(msg):
    for caracter in msg:
        sys.stdout.write(caracter)
        sys.stdout.flush()
        seconds = TYPE_SPEED
        sleep(seconds)
    print()   

def separator(type, size):
    if type == 1: # top separator
        print()
        print("*"*size)
    else:         # bottom separator
        print(("*"*size))

def align_center(text, size):
    spaces = round((size - len(text)) / 2)
    text_size = len(text)

    if text_size < size:
        if text_size%2 == 1 and size %2 != 1:
            separator(0, size+1)
            separator(1, size+1)
            print(" " * (spaces+1)+text)
            separator(0, size+1)
            separator(1, size+1)
        else: 
            separator(0, size)
            separator(1, size)
            print(" " * spaces+text)
            separator(0, size)
            separator(1, size)
    else:
        if text_size <= 120:
            separator(0, text_size)
            separator(1, text_size)
            print(text)
            separator(0, text_size)
            separator(1, text_size)
        else:
            separator(0, 120)
            separator(1, 120)
            print(text)
            separator(0, 120)
            separator(1, 120)

def clean_align_center(text, size):
    spaces = round((size - len(text)) / 2)
    text_size = len(text)

    if text_size < size:
        if text_size%2 == 1 and size %2 != 1:
            separator(0, size)
            print(" " * (spaces+1)+text)
            separator(0, size)
        else:
            separator(0, size) 
            print(" " * spaces+text)
            separator(0, size)
    else:
        if text_size <= 120:
            separator(0, text_size)
            print(text)
            separator(0, text_size)
        else:
            separator(0, 120)
            print(text)
            separator(0, 120)

