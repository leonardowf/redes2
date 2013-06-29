# coding=UTF-8

from datetime import datetime
import socket

class Client:
    loggers = []
    
    def __init__(self, UDP_IP, UDP_port):
        self.UDP_IP = UDP_IP
        self.UDP_port = UDP_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def add_logger(self, logger):
        self.loggers.append(logger)
    
    def notify_all(self, message):
        time = datetime.time(datetime.now())
        for logger in self.loggers:
            logger.log(time, message)
    
    def log(self, message):
        self.notify_all(message)
    
    def send(self, message):
        self.socket.sendto(message, (self.UDP_IP, self.UDP_port))
