#!/usr/bin/env python3
# Documentation: https://docs.python.org/3/library/socket.html
import socket
import json
import sqlite3
import sys
import socket_utils

DB_NAME = "reception.db"

with open("config.json", "r") as file:
    data = json.load(file)

HOST = data["masterpi_ip"]  # The server's hostname or IP address.
PORT = 63000               # The port used by the server.
ADDRESS = (HOST, PORT)


def main():
    while(True):
        print("1. Login as Mahtab")
        print("0. Quit")
        print()

        text = input("Select an option: ")
        print()

        if(text == "1"):
            #Getting the user information
            user = "Mahtab"
            login(user)
        elif(text == "0"):
            print("Goodbye.")
            print()
            break
        else:
            print("Invalid input, try again.")
            print()


def login(user):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Connecting to {}...".format(ADDRESS))
        s.connect(ADDRESS)
        print("Connected.")

        print("Logging in as {}".format(user))
        #Sending information to the master pi
        socket_utils.sendJson(s, user)

        print("Waiting for Master Pi...")
        #Loop to wait for the master pi to send logout = True
        while(True):
            object = socket_utils.recvJson(s)
            if("logout" in object):
                print("Master Pi logged out.")
                print()
                break


# Execute program.
if __name__ == "__main__":
    main()
