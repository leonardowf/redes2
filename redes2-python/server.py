# coding=UTF-8

import socket
from datetime import datetime

class Server:
    loggers = []
    
    def __init__(self, UDP_IP, UDP_port):
        self.UDP_IP = UDP_IP
        self.UDP_port = UDP_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.UDP_IP, self.UDP_port))
    
    def add_logger(self, logger):
        self.loggers.append(logger)
    
    def notify_all(self, message):
        time = datetime.time(datetime.now())
        for logger in self.loggers:
            logger.log(time, message)
    
    def log(self, message):
        self.notify_all(message)
        
    def listen(self):
        while True:
            data, addr = self.socket.recvfrom(1024) # buffer size is 1024 bytes
            print "received message:", data + "with addr: ", addr
        
        

