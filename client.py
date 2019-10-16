import socket
import logging


def Main():

    try:
        host = "127.0.0.1"
        port = 5000

        s = socket.socket()
        s.connect((host, port))

    except ConnectionRefusedError:
        pass

    try:
        #Disply existing resources
        print( s.recv(1024).decode() )


        resourceNeeded = input("\n> Which resource do you need to access?\n> ")
        s.send(str.encode(resourceNeeded))

        #check resource existance
        if s.recv(1024).decode() == "Exists":
            print ("\n> Trying to aquire target resource...")

            if s.recv(1024).decode() != "!Locked":
                print("\n> Timeout: Aquire error for resource {}".format(resourceNeeded))
                print("> Another service is currently working with {}".format(resourceNeeded))

            else:
                print("> {} aquired before timeout".format(resourceNeeded))
                inputData = input("> Enter your data. (Hit q to quite!). \n\n> ")
                while inputData != 'q':
                    s.send(str.encode(inputData))
                    inputData = input("> ")
                print("> Socket is closing . . . ")
                s.close()

        else: #Resouce is not existing
            print("> Resource is not existing")
            print("> Socket is closing . . . ")
            s.close()
    except:
        print("\n> Error: Can't connect to the targeted server!")
        print("> Socket is closing . . . ")
        s.close()

if __name__ == '__main__':
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    Main()