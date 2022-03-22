
import sys
import time
import socket
import base64
import random
import threading
import tkinter.messagebox

from tkinter import *
from tkhtmlview import HTMLLabel
from cryptography.fernet import Fernet

global client_socket
global last_recieved
global student_id
global next_level
global b64_flag
global score

def quit(score):
    global root
    global student_id

    if score == 0:
        root.destroy()
        sys.exit()
    else:
        message = student_id + ':score:' + score
        message = base64.b64encode(message.encode())
        client_socket.send(message)
        client_socket.close()
        root.destroy()
        sys.exit()

root=Tk()
root.title("Traffic Capture 101")
text = Text(root, height=1, width=30)
text.pack()
text.insert(END, 'Your score: 100%')

def update_text(input):
    text.delete('1.0', END)
    text.insert(END, input)

def retrieve_input(get_string):
    global last_recieved
    global next_level
    global b64_flag
    global score
    user_input=get_string
    ent.delete(0, END)

    if user_input == last_recieved:
        update_text('Correct!')
        if b64_flag:
            print('Your score: ' + str(score) +'%')
            quit(str(score))
        else:
            next_level = True
    else:
        update_text('Too Slow!')

ent = Entry(root)
ent.bind("<Return>", (lambda event: retrieve_input(ent.get())))
ent.pack()
btn = Button(root,text="Submit", command=(lambda: retrieve_input(ent.get())))
btn.pack()

def client_program(ID_Number, IP_Addr):
    global client_socket
    global last_recieved
    global student_id
    global next_level
    global b64_flag
    global score

    student_id = ID_Number

    host = IP_Addr # pi IP address
    port = 5000  # socket server port number

    score = 100

    hex_flag = False
    b64_flag = False
    next_level = False

    word_file = "words"
    words = open(word_file).read().splitlines()

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = random.choice(words)  # take input

    while True:

        time.sleep(25)

        if next_level:
            message =  'get rekt'
            print('Next Level')
            if hex_flag and not b64_flag:
                hex_flag = False
                b64_flag = True
                message = '\\'.join(x.encode('utf-8').hex() for x in message)

            if not hex_flag and not b64_flag:
                hex_flag = True

            client_socket.send(message.encode()) # send message
            next_level = False

        elif hex_flag:
            message = '\\'.join(x.encode('utf-8').hex() for x in message)
            client_socket.send(message.encode())

        elif b64_flag:
            message = base64.b64encode(message.encode())
            client_socket.send(message) # Don't encode base64 message

        else:
            client_socket.send(message.encode()) # send message

        data = client_socket.recv(1024).decode()  # receive response

        if b64_flag:
            data = str(base64.b64decode(str(data)).decode("utf-8"))

        if hex_flag:
            data = bytearray.fromhex(data.replace('\\','')).decode()

        last_recieved = data

        if b64_flag or hex_flag:
            score -= 1
        else:
            score -= 2
        update_text('Your score: ' + str(score) +'%')

        message = random.choice(words)  # again take input


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Traffic Capture and Decode")
    
    parser.add_argument("-sid", help="Student ID Number", required = True)
    parser.add_argument("-ip", help="Server IP", required = True)

    args = parser.parse_args()
    ID_Number = args.sid
    IP_Addr = args.ip

    threading1 = threading.Thread(target=client_program, args=(ID_Number, IP_Addr))
    threading1.daemon = True
    threading1.start()

while True:
    Button(root, text="Quit", command= lambda: quit(0)).pack()
    root.title("Traffic Capture And Decode: " + student_id)
    root.mainloop()
