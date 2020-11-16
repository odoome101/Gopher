'''
A simple Gopher client written in Python.

author:  Amy Csizmar Dalal and  Eric Odoom, Etienne Richart, Aishee B. Mukherji
CS 331, Fall 2020
'''

import re, sys, socket

HOSTNAME = socket.gethostname()

def connectToServer(server, port, message):
    try:
        serverSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        serverSock.connect((server, port))
        print ("Connected to server; sending message\n")
        serverSock.send(message.encode("ascii"))
        print ("Sent message; waiting for reply\n")

    except:
        print("No connection to server available.\n")
        sys.exit(0)

    rcvd = ""
    while True:
        data = serverSock.recv(1024)
        if not len(data):
            break
        rcvd += data.decode("ascii")
        print ("Received response: "+ rcvd.decode("ascii"))
    return rcvd

def getLinks(file):
    dict = {}
    for line in file.split("\n"):
        data = line.split("\t")
        dict[data[0]] = data[1:]
    return dict


def print_dir(links):
    for link in links:
        if link == "":
            pass
        elif link[0] == "0":
            print(link[1:])
        elif link[0] == "1":
            print(link[1:]+"....")
        else:
            pass

def requests(links):
    server= "localhost"
    port= "62535"
    request = input("\Choose one of the following  ")
    print()
    if request == "":
        return "not valid", "none", server, port
    try:
        for link in links:
            if request in link:
                server = links[link][1]
                port = links[link][2]
                message = links[link][0]
                if link[0] == "0":
                    type = "file"
                elif link[0] == "1":
                    type = "links"
                else:
                    type = "not valid"
                return message,type,port,server
    except IndexError:
        print("Invalid .links file \n")
    except TypeError:
        print("Input Error\n")

    return "", "links",port,server

def main():
    if len(sys.argv) >= 3:
        try:
            server = sys.argv[1]
            port = int(sys.argv[2])
            message = "\r\n"
            type = "links"
            links = {}
        except ValueError:
            print("Value Error\n")
    else:
        print("Input Error\n")

    while True:
        response = connectToServer(server, port, message)
        if type == "links":
            links = getLinks(response)

        elif type == "file":
            print(response)
            input("\n")
            print()
            message = ""
        else:
            pass
        message,type,port,server = requests(links)
        port = int(port)
        message += "\r\n"
        print_dir(links)


main()
