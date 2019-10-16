import socket
import threading, _thread
import os
from resourceAllocation import resourceAllocation
import logging



#Resources Classes
resource_1_lock = threading.Lock()
resource_2_lock = threading.Lock()



#Resources Dict
availableResources = {
        'Resource1.txt': resource_1_lock,
        'Resource2.txt': resource_2_lock
    }



def checkAvailableResource(resourceName):
    for key in availableResources.keys():
        if key == resourceName:
            logging.info("Resource is exists . . .!")
            return 1
    logging.info("Resource is not available!!")
    return 0



def aquireResource(resourceName, socket):
    if availableResources[resourceName].acquire(timeout=12.5):
        logging.info("Resource: {}, Aquired: {}, By: {}".format(resourceName, True, socket))
        return 1
    logging.info("Resource: {}, Aquired: {}, By: {}".format(resourceName, False, socket))
    return 0


#Sends existing resources to caller client.
def displayResources(socket):
    displyMessage = ""
    for resource in availableResources.keys():
        displyMessage += "\n> {} currently exist".format(resource)
    socket.send(str.encode(str(displyMessage)))



def Main():
    host = "127.0.0.1"
    port = 5000
    s = socket.socket()
    s.bind((host, port))
    s.listen(5)
    print ("Context Manager Started . . . .")

    while True:
        c, addr = s.accept()
        print ("client: {} is connected to the context manager".format(str(addr)))

        #Send existing reousrces to new clients
        displayResources(c)

        #Recv: Resouce needed to access
        resourceRequired = c.recv(1024).decode()

        #Check needed resource availability
        if checkAvailableResource(resourceRequired):
            c.send(str.encode(str("Exists"))) #send accepted resource to client

            if aquireResource(resourceRequired, c) == 1:
                c.send(str.encode(str("!Locked")))
                resourceLock = availableResources[resourceRequired]
                t = threading.Thread(target = resourceAllocation.getResource, args=("retrRecource", resourceRequired, c, resourceRequired, resourceLock ))
                t.start()
            else:
                c.send(str.encode(str("Locked")))

        else: #Resource is not found
            logging.info("Client: {} is requesting a not existing resource!".format(str(addr)))
            c.close()


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    Main()