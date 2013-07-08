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
        
        
        self.socket.bind((self.UDP_IP, 9002))
    
    def add_logger(self, logger):
        self.loggers.append(logger)
    
    def notify_all(self, message):
        time = datetime.time(datetime.now())
        for logger in self.loggers:
            logger.log(time, message)
    
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
            print "ok, pode comecar o a transmissão"    
    
    def next_packet(self, lose):
        switch_lose = lose
        
        for a_packet in self.list_of_packets:
            print "packet %d foi acked?: %s devo perder? %s" % (a_packet.sequence_number, a_packet.acked, lose)
            if (not a_packet.acked):
                if (switch_lose):
                    switch_lose = False 
                else:
                    print "proximo packet é %d" % a_packet.sequence_number
                    return a_packet
                    
                
        return False
            
        
    def send(self, data):
        self.send_start_transmission_request()
        # quebra data em pequenos pacotes
        bytes = len(data)
        size_to_split = self.packet_size
        self.list_of_packets = []
        for i in range(0, bytes, size_to_split):
            splitted_data = data[i:i+size_to_split]
            print "wtf: " + str(self.seq_num)
            a_packet = packet.Packet(splitted_data, self.seq_num)
            self.list_of_packets.append(a_packet)
            self.increments_sequence_number()
            # temos uma lista com todos os packets
        p = self.next_packet(False)
        
        while (p):
        
            dup = self.should_i_duplicate_this_packet()
            lose = self.should_i_lose_this_packet()
        
            if (lose):
                print "Vou perder esse pacote %d" % p.sequence_number
                p = self.next_packet(True)
                
                if (p):
                    self.send_packet(p)
                    print "enviei pacote %d" % p.sequence_number
                    r = self.receive_response()
                    print "recebi a resposta: %d é ack? %s" % (r.sequence_number, r.is_ACK())
                    if (r.is_ACK()):
                        print "isso nao deveria acontecer"
                    else:
                        print "NACK %d" % r.sequence_number
                    # r is ack
                    
                # if (p)
            # fim do if (lose)
            elif (dup):
                print "enviando duplicado o: %d" % p.sequence_number
                
                self.send_packet(p)
                self.send_packet(p)
                
                r = self.receive_response()
                if (r.is_ACK() and (r.sequence_number == p.sequence_number)):
                    print "recebi um ack com %d" % r.sequence_number
                    p.acked = True
                # end if is ack
                else:
                    print "recebi um nack de %d" % r.sequence_number
                # end else
            # end if dup
            else:
                print "enviei normalmente o %d" % p.sequence_number
                self.send_packet(p)
                received_packet = self.receive_response()
                if (received_packet.is_ACK()):
                    print "ACK do " + str(received_packet.sequence_number)
                    p.acked = True
            # else normalmente
            p = self.next_packet(False)
        # fim do while
        self.send_end_of_transmission()
            
    def send_end_of_transmission(self):
        p = packet.Packet("", -1)
        raw_end = p.pack()
        self.send_packet(p)
        self.socket.close()
    
    def send_packet(self, a_packet):
        raw_packet = a_packet.pack()
        self.socket.sendto(raw_packet, (self.UDP_IP, self.UDP_port))
        
    def should_i_duplicate_this_packet(self):
        if (self.duplicate_packets_mode):
            r = random.randint(1, 100)
            if (r <= self.duplicate_percentage): # duplicar
                return True
        else:
            return False
        
    def should_i_lose_this_packet(self):
        if (self.lose_packets_mode):
            r = random.randint(1, 100)
            if (r <= self.lost_percentage): # perdeu
                return True
            else:
                return False
        else:
            return False
        
        
    
    def receive_response(self):

        data = None
        while True:
            data, addr = self.socket.recvfrom(1024) # buffer size is 1024 bytes
            if (data):
                p = packet.Packet("", 0)
                p.unpack(data)
                return p;

    
    def increments_sequence_number(self):
        self.seq_num = self.seq_num + 1
        if self.seq_num == self.limit_seq_num:
            self.seq_num = 0
            
        
    

        
        
