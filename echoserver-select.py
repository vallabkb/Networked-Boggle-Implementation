#!/usr/bin/env python

"""
Authors: Killian Bailey & Vallab Kunigal Badrish
An echo server that uses select to handle multiple clients at a time.
Entering any line of input at the terminal will exit the server.
"""

import select
import socket
import sys
import random
import time

host = ''
port = 65120
backlog = 5
size = 1024
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen(5)
print("Waiting for Clients to connect")
inputList = [server]

running = 1

board = ["AAEEGN",  "ABBJOO",  "ACHOPS", "AFFKPS", "AOOTTW", "CIMOTU", "DEILRX",
               "DELRVY", "DISTTY",  "EEGHNW",  "EEINSU",  "EHRTVW", "EIOSST",
                "ELRTTY", "HIMNQuL", "HLNNRZ" ]
workingboard = board

count = 0

boardStr = ""

for index in range (0,4):

    for index2 in range (0,4):

        letterDie = workingboard[count]
        randomIndex = random.randint(0,len(letterDie)-1)
        letter = letterDie[randomIndex]

    
        if letter == "u" or letter == "Q":
            letter = "Qu"

        boardStr = boardStr + letter + " "
        
        count += 1

    boardStr = boardStr + "\n"

client1_words = set()
client2_words = set()

while running:
    inputready,outputready,exceptready = select.select(inputList,[],[],1)

    for s in inputready:
        if len(inputList) > 3:
            inputList.remove(client1)
            print("Only two players allowed!")
            s.close()
              #Someone tried to connect to the server for the first time.
	#Let's accept.
        elif s == server:
            # handle the server socket
            client1, address = server.accept()
            inputList.append(client1)
            print("Player 1 has joined the game")
            client2,address = server.accept()
            inputList.append(client2)
            print("Player 2 has joined the game")
       
            client1.send(bytes(boardStr, 'ascii'))
            client2.send(bytes(boardStr, 'ascii'))

            end = time.time() + 180
            #This is a client sending messages!    
        elif s in inputList and time.time() < end:
            # handle all other sockets

	    # try to read
            data = s.recv(size)
            
            if not data:
               s.close()
            elif s == client1:
                client1_words.add( data.decode().strip() )
            elif s == client2:
                client2_words.add( data.decode().strip() )
            else:
                s.close()
                print("Removing a client")
                inputList.remove(s)
                break
            print(client1_words,client2_words)
        elif time.time() >= end:
            
            unique1 = client1_words - client2_words
            unique2 = client2_words - client1_words

            score1 = 0
            score2 = 0

            for word in unique1:
                if 3 <= len(word) <= 4:
                    score1 = score1 + 1
                elif len(word) == 5:
                    score1 = score1 + 2
                elif len(word) == 6:
                    score1 = score1 + 3
                elif len(word) == 7:
                    score1 = score1 + 5
                elif len(word) >= 8:
                    score1 = 11

            for word in unique2:
                if 3 <= len(word) <= 4:
                    score2 = score2 + 1
                elif len(word) == 5:
                    score2 = score2 + 2
                elif len(word) == 6:
                    score2 = score2 + 3
                elif len(word) == 7:
                    score2 = score2 + 5
                elif len(word) >= 8:
                    score2 = 11
                    

            result = 'Unique words for Player 1: ' + str(unique1) + '\n'
            result += 'Unique words for Player 2: ' + str(unique2) + '\n'
            result += "Player 1's score: " + str(score1) + '\n'
            result += "Player 2's score: " + str(score2) + '\n'

            if score1 > score2:
                result += 'Player 1 wins!\n'
            elif score1 < score2:
                result += 'Player 2 wins!\n'
            else:
                result += 'A tie!\n'

            client1.send(bytes( result, 'ascii' ))
            client2.send(bytes( result, 'ascii' ))
            server.close()
            
server.close()
