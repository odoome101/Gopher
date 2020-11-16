'''
A simple Gopher "echo" server written in Python.

author:  Amy Csizmar Dalal and Eric Odoom, Etienne Richart, Aishee B. Mukherji
CS 331, Fall 2020

PORT: 62535
'''

import sys, socket

class TCPServer:
    def usage():
        print ("Usage:  python SimpleTCPClient <server IP> 62535 <message>")
        sys.exit()

    def __init__(self, port=62535):
        self.port = port
        self.host = ""
        self.startServer()

    def startServer(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        print("Listening on port 62535\n")
        self.sock.listen(5)

        while True:
            clientSock, clientAddr = self.sock.accept()
            print ("Connection received from ",  clientSock.getpeername())
            while True:
                data = clientSock.recv(1024)
                if not len(data):
                    break
                message = self.getMessage(data.decode("ascii"))
                data = message.encode("ascii")
                print("Received message:  " + data.decode("ascii"))
                clientSock.sendall(data)
                clientSock.shutdown(socket.SHUT_RDWR)
        clientSock.close()

    def getMessage(self, msg):
        message = ""
        data = msg.strip()
        if data == "not valid":
            pass
        elif msg == "\r\n":
            message = self.getLinks(self.open(".links"))
        elif msg.strip()[-1] == "/":
            message = self.getLinks(self.open(data + ".links"))
        else:
            message = self.open(data)
        message += "\r\n."
        return message

    def open(self,dir):
        try:
            resource = open(dir)
            data = self.getData(resource)
            resource.close()
            return content
        except:
            return "This resource cannot be located \r\n"

    def getData(self, file):
        data = ""
        for line in file:
            data += line
        return data

    def getLinks(self, file):
        dict = {}
        for line in file.split("\n"):
            data = line.split("\t")

            """ Max key length set to 100"""
            key = self.length(data[0], 100)
            value = data[1:]

            """ Max selector string set to 300 """
            value[0] = self.length(value[0], 300)
            dict[key] = value

        key_string = ""
        for key in dict:
            key_string += key + "\t"
            for item in dict[key]:
                key_string += item + "\t"
            key_string += "\n"

        return s

    def length(self, key_string, cap):
        if len(key_string) > cap:
            return key_string[:cap-1]
        return key_string

def main():
    if len(sys.argv) > 1:
        try:
            server = TCPServer(int(sys.argv[1]))
        except ValueError:
            print ("Error in specifying port. Creating server on default port.\n")
            server = TCPServer()
    else:
        server = TCPServer()

    print ("Listening on port " + str(server.port))
    server.listen()

main()
