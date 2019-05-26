# Acknowledgement
# part of this code is adapted from: Matthew

import socket
import json
import sys
from dbLogic import LocalUser
from datetime import datetime
import socket_utils


class RPMenu:

    db = None
    isRunnig = True
    display_menu = "1.Login Using Credentials\n2.Login Using FR\n3.Register\n4.Quit\n"
    username_promt = "Please enter your username\n"
    password_promt = "Please enter your password\n"
    firstName_promt = "Please enter your first name\n"
    lastName_promt = "Please enter your last name\n"
    email_promt = "Please enter your email\n"
    HOST = '10.132.5.156'
    PORT = 63000
    ADDRESS = (HOST, PORT)

    def __init__(self):
        self.db = LocalUser('UsersRP.db')

        while(self.isRunnig):
            choice = input(self.display_menu)

            if (choice == '1'):
                username = input(self.username_promt)
                password = input(self.password_promt)

                if (self.db.loginUsingCredentials(username, password)):
                    # We would send a msg using socket to MP
                    print("--login success")
                    self.connectToMp(username)
                else:
                    print('--Invalid Username and/or password')

            elif(choice == '2'):
                username = self.db.loginUsingFR()
                if (username):
                    # We would send a msg using socket to MP
                    print("--login success")
                    self.connectToMp(username)
                else:
                    print('--User not found or Face not detected')

            elif (choice == '3'):
                username = input(self.username_promt)
                password = input(self.password_promt)
                firstName = input(self.firstName_promt)
                lastName = input(self.lastName_promt)
                email = input(self.email_promt)

                if (self.db.registerUser(username, password, firstName, lastName, email)):
                    # We would send a msg using socket to MP
                    print("--Register success")
                    self.connectToMp(username)
                else:
                    print('--Please try again')
            elif (choice == '4'):
                self.isRunnig = False
            else:
                print("--Invalid Choice")

    def connectToMp(self, username):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("Connecting to {}...".format(self.ADDRESS))
            s.connect(self.ADDRESS)
            print("Connected.")

            print("Logging in as {}".format(username))
            # Sending information to the master pi
            socket_utils.sendJson(s, username)

            print("Waiting for Master Pi...")
            # Loop to wait for the master pi to send logout = True
            while(True):
                object = socket_utils.recvJson(s)
                if("logout" in object):
                    print("Master Pi logged out.")
                    print()
                    break


start = RPMenu()
