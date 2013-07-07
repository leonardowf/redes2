# coding=UTF-8

import socket
import packet
from datetime import datetime

class Server:
    loggers = []
    expected_sequence_number = 0
    limit_seq_num = 256
    data = ""
    
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
            # print "received message:", data + "with addr: ", addr
            a_packet = packet.Packet("", 0)
            a_packet.unpack(data)
            
            if (a_packet.is_start()):
                self.expected_sequence_number = a_packet.sequence_number
                self.transmission_started()
            
            
            an_ACK = packet.Packet("", 0)
            raw_ACK = an_ACK.create_raw_ACK(a_packet.sequence_number)
            self.socket.sendto(raw_ACK, (self.UDP_IP, 9002))
        
        
        
    def transmission_started(self):
        print "recebi um pedido de transmissão"
        
        self.list_of_packets = []
        
        an_ACK = packet.Packet("", 0)
        raw_ACK = an_ACK.create_raw_ACK(self.expected_sequence_number)
        self.socket.sendto(raw_ACK, (self.UDP_IP, 9002))
        
        while True:
            data, addr = self.socket.recvfrom(1024) # buffer size is 1024 bytes
            a_packet = packet.Packet("", 0)
            a_packet.unpack(data)
            
            print "pacote esperado é %d" % self.expected_sequence_number
            print "recebi o %d" % a_packet.sequence_number
            
            if (a_packet.sequence_number == self.expected_sequence_number):
                # significa que o pacote tá na ordem certa
                self.list_of_packets.append(a_packet)
                self.data = self.data + a_packet.data
                self.send_ACK(self.expected_sequence_number)
                print "beleza recebi o pacote esperado enviei ack do %d" % self.expected_sequence_number
                self.increments_expected_sequence_number()

            else:
                if (a_packet.sequence_number == -1):
                    self.finalizes_transmission()
                    return
                    
                elif (self.ja_tenho(a_packet)):
                    print "ja tenho o %d" % a_packet.sequence_number
                else:
                    self.send_NACK(self.expected_sequence_number)
    
    def finalizes_transmission(self):
        self.expected_sequence_number = 0
        print self.data
        self.data = ""
        print "finalizar"
                
    def ja_tenho (self, a_packet):
        for p in self.list_of_packets:
            if a_packet.sequence_number == p.sequence_number and a_packet.data == p.data:
                return True
        return False
        
        
        
    
    
    def send_ACK(self, sequence_number):
        an_ACK = packet.Packet("", 0)
        raw_ACK = an_ACK.create_raw_ACK(sequence_number)
        self.socket.sendto(raw_ACK, (self.UDP_IP, 9002))
    
    def send_NACK(self, sequence_number):
        an_NACK = packet.Packet("", 0)
        raw_NACK = an_NACK.create_raw_NACK(sequence_number)
        self.socket.sendto(raw_NACK, (self.UDP_IP, 9002))
        
    
    def increments_expected_sequence_number(self):
        self.expected_sequence_number = self.expected_sequence_number + 1
        if self.expected_sequence_number == self.limit_seq_num:
            self.expected_sequence_number = 0
        
        
        
        
        
        
                
            
            
            
            
        
        
        
        

