# coding=UTF-8

from datetime import datetime
import socket
import packet
import random


class Client:
    loggers = []
    start_identifier = 0
    limit_seq_num = 256
    packet_size = 1
    lost_percentage = 20
    duplicate_percentage = 20
    lose_packets_mode = True
    duplicate_packets_mode = True
    
    def __init__(self, UDP_IP, UDP_port):
        self.UDP_IP = UDP_IP
        self.UDP_port = UDP_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.loggers = []
        
        self.socket.bind((self.UDP_IP, 9002))
    
    def add_logger(self, logger):
        self.loggers.append(logger)
    
    def notify_all(self, message):
        time = datetime.time(datetime.now())
        for logger in self.loggers:
            logger.log(time, message)
        nop = 0
    
    def log(self, message):
        self.notify_all(message)
        
        
    def send_start_transmission_request(self):
        self.start_identifier = random.randint(0, 255)
        self.seq_num = self.start_identifier
        
        p = packet.Packet("", 0)
        raw_start = p.create_raw_start(self.start_identifier)
        self.socket.sendto(raw_start, (self.UDP_IP, self.UDP_port))
        
        response = self.receive_response()
        if response.is_ACK():
            msg = "Iniciando transmissão"
            self.notify_all(msg)
            # print "ok, pode comecar o a transmissão"    
    
    def next_packet(self, lose):
        switch_lose = lose
        
        for a_packet in self.list_of_packets:
            # print "packet %d foi acked?: %s devo perder? %s" % (a_packet.sequence_number, a_packet.acked, lose)
            if (not a_packet.acked):
                if (switch_lose):
                    switch_lose = False 
                else:
                    # print "proximo packet é %d" % a_packet.sequence_number
                    return a_packet
                    
                
        return False
            
        
    def send(self, data):
        self.send_start_transmission_request()
        # quebra data em pequenos pacotes
        bytes = len(data)
        size_to_split = self.packet_size
        self.list_of_packets = []
        for i in range(0, bytes, size_to_split):
            splitted_data = data[i:i + size_to_split]
            a_packet = packet.Packet(splitted_data, self.seq_num)
            self.list_of_packets.append(a_packet)
            self.increments_sequence_number()
            # temos uma lista com todos os packets
        p = self.next_packet(False)
        
        while (p):
        
            dup = self.should_i_duplicate_this_packet()
            lose = self.should_i_lose_this_packet()
        
            if (lose):
                # print "Vou perder esse pacote %d" % p.sequence_number
                msg = "Perdendo o pacote %d" % p.sequence_number
                self.notify_all(msg)
                p = self.next_packet(True)
                
                if (p):
                    self.send_packet(p)
                    msg = "Enviei pacote %d" % p.sequence_number
                    self.notify_all(msg)
                    r = self.receive_response()
                    if (r.is_ACK()):
                        print "isso nao deveria acontecer"
                    else:
                        msg = "NACK %d" % r.sequence_number
                        self.notify_all(msg)
                    # r is ack
                    
                # if (p)
            # fim do if (lose)
            elif (dup):
                msg = "Enviando duplicado o: %d" % p.sequence_number
                self.notify_all(msg)
                
                self.send_packet(p)
                self.send_packet(p)
                
                r = self.receive_response()
                if (r.is_ACK() and (r.sequence_number == p.sequence_number)):
                    msg = "Recebi um ack com %d" % r.sequence_number
                    self.notify_all(msg)
                    p.acked = True
                # end if is ack
                else:
                    msg = "recebi um nack de %d" % r.sequence_number
                    self.notify_all(msg)
                # end else
            # end if dup
            else:
                msg = "Enviei normalmente o %d" % p.sequence_number
                self.notify_all(msg)
                self.send_packet(p)
                received_packet = self.receive_response()
                if (received_packet.is_ACK()):
                    msg = "ACK do " + str(received_packet.sequence_number)
                    self.notify_all(msg)
                    p.acked = True
            # else normalmente
            p = self.next_packet(False)
        # fim do while
        self.send_end_of_transmission()
            
    def send_end_of_transmission(self):
        p = packet.Packet("", -1)
        raw_end = p.pack()
        self.send_packet(p)
        self.loggers = []
        self.socket.close()
    
    def send_packet(self, a_packet):
        raw_packet = a_packet.pack()
        self.socket.sendto(raw_packet, (self.UDP_IP, self.UDP_port))
        
    def should_i_duplicate_this_packet(self):
        if (self.duplicate_packets_mode):
            r = random.randint(1, 100)
            if (r <= self.duplicate_percentage):  # duplicar
                return True
        else:
            return False
        
    def should_i_lose_this_packet(self):
        if (self.lose_packets_mode):
            r = random.randint(1, 100)
            if (r <= self.lost_percentage):  # perdeu
                return True
            else:
                return False
        else:
            return False
        
        
    
    def receive_response(self):

        data = None
        while True:
            data, addr = self.socket.recvfrom(1024)  # buffer size is 1024 bytes
            if (data):
                p = packet.Packet("", 0)
                p.unpack(data)
                return p;

    
    def increments_sequence_number(self):
        self.seq_num = self.seq_num + 1
        if self.seq_num == self.limit_seq_num:
            self.seq_num = 0
            
        
    

        
        
