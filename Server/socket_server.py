import socket
import base64
import random
import time
import os

from cryptography.fernet import Fernet

def write_key():

    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():

    return open("key.key", "rb").read()

def create_encrypt(student_id, score, key):

    f = Fernet(key)

    encrypted_data = f.encrypt(score)
    # write the encrypted file
    if not os.path.isfile(student_id +'_score.txt'):
        with open(student_id +'_score.txt', "wb") as file:
            file.write(encrypted_data)

def server_program():
    # get the hostname
    host = ''
    port = 5000  # initiate port no above 1024

    score = 100

    b64_flag = False
    hex_flag = False

    word_file = "/usr/share/dict/words"
    words = open(word_file).read().splitlines()

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        if b64_flag:
            output = str(base64.b64decode(data).decode("utf-8"))
        elif hex_flag:
            output = str(bytearray.fromhex(data.replace('\\','')).decode())

        else:
            output = str(data)

        if b64_flag:
            score -= 1
        else:
            score -= 2

        if output == 'get rekt':
            if not hex_flag:
                hex_flag = True
            else:
                hex_flag = False
                b64_flag = True

        if output.__contains__('score'):

            score_txt = str(base64.b64decode(data).decode("utf-8"))
            student_details = score_txt.split(':')
            student_id = student_details[0]
            score = student_details[2]
            score = score.encode('utf-8')

            write_key()
            key = load_key()

            create_encrypt(student_id, score, key)

        message = random.choice(words)
        if b64_flag:
            message = base64.b64encode(message.encode())
            conn.send(message)  # send data to the client
        elif hex_flag:
            message = '\\'.join(x.encode('utf-8').hex() for x in message)
            conn.send(message.encode())
        else:
            conn.send(message.encode())

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()
