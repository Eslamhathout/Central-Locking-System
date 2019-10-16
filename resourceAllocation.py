import socket
import threading, _thread
import os
import time
import logging


class resourceAllocation:
    def getResource(self, name, sock, resource, resourceLock):
        try:
            with resourceLock and open(resource, 'w+') as f:
                inputData = sock.recv(1024).decode()
                logging.info("New Data: {}".format(inputData))
                while inputData != "q" and inputData != "":
                    logging.info("Recived Data: {}".format( inputData))
                    f.write(inputData)
                    inputData = sock.recv(1024).decode()
                logging.info("Resource editing completed . . ")
                f.close()
                sock.close()
        except: #Error occured when using resource
            resourceLock.release()
            logging.info("Unexpected error occured while using resource . . . ")
        resourceLock.release()
        logging.info("Resource allocation closing . . .")




























# class resourceAllocation:
#     resourceLock = threading.Lock()

#     def aquireResource(self):
#         resourceAllocation.resourceLock.acquire()
    
#     def setRelease(self):
#         resourceAllocation.resourceLock.release()

#     def getResource(self, name, sock, resource):
#         resourceAllocation.aquireResource(self)
#         logging.info(resourceAllocation.resourceLock)
#         logging.info("Above")
#         if resourceAllocation.resourceLock.locked():
#             logging.info("Currently locked by: {}".format(sock))

#             if os.path.isfile(resource):
#                 logging.info("Resource Exists!")
#                 with open(resource, 'w+') as f:
#                         inputData = sock.recv(1024).decode()
#                         logging.info("New Data: {}".format(inputData))
#                         while inputData != "q" and inputData != "":
#                             logging.info("Recived Data: {}".format( inputData))
#                             f.write(inputData)
#                             inputData = sock.recv(1024).decode()

#                         sock.close()
#                         resourceAllocation.setRelease(self)
#                         logging.info("End of method release with open")
#                         f.close()

#             else:
#                 sock.close()
#                 logging.info("Can't find resource!")
#                 resourceAllocation.setRelease(self)
#                 f.close()
#         sock.close()
#         logging.info("End of method release if locked")
