#!/usr/bin/env python3
# Documentation: https://docs.python.org/3/library/socket.html
import socket, json, sys
sys.path.append("..")
import socket_utils

# Empty string means to listen on all IP's on the machine, also works with IPv6.
HOST = '131.170.239.9'
# Note "0.0.0.0" also works but only with IPv4.
PORT = 63000  # Port to listen on (non-privileged ports are > 1023).
ADDRESS = (HOST, PORT)


def main():
    #setting up the socket and listening on the Address
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(ADDRESS)
        s.listen()

        print("Listening on {}...".format(ADDRESS))
        while True:
            print("Waiting for Reception Pi...")
            conn, addr = s.accept()
            with conn:
                print("Connected to {}".format(addr))
                print()

                #recieving information from the reception pi
                user = socket_utils.recvJson(conn)
                #HERE IS WHERE OUR MENU WILL BE PLACED
                menu(user)

                #closing the connection by sending logout = True
                socket_utils.sendJson(conn, {"logout": True})


def menu(user):
    while(True):
        print("Welcome {}".format(user))
        print("1. Display user details")
        print("0. Logout")
        print()

        text = input("Select an option: ")
        print()

        if(text == "1"):
            print("Username  : {}".format(user))
            print()
        elif(text == "0"):
            print("Goodbye.")
            print()
            break
        else:
            print("Invalid input, try again.")
            print()


# Execute program.
if __name__ == "__main__":
    main()
