import socket
import threading, _thread
import os
import time
import logging

class resourceAllocation:
    def getResource(self, name, sock, resource, resourceLock):
        try:
            with resourceLock and open(resource, 'a') as f:
                inputData = sock.recv(1024).decode()
                logging.info("New Data: {}".format(inputData))
                while inputData != "q" and inputData != "":
                    logging.info("Recived Data: {}".format( inputData))
                    f.write(inputData)
                    inputData = sock.recv(1024).decode()
                logging.info("Resource editing completed . . ")
                sock.close()
            logging.info(" releaseing lock . . ")
        except: #Error occured when using resource
            resourceLock.release()
            logging.info("Unexpected error occured while using resource . . . ")
        
        resourceLock.release()
        logging.info("Resource allocation closing . . .")
