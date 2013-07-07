# coding=UTF-8

from collections import namedtuple
from struct import *

DATA_ID =   0b0101010101010111
ACK_ID =    0b1010101010101010
NACK_ID =   0b0101010101011111
START_ID =  0b1010101110111010
HEADER_LEN = 6  # Bytes

class Packet:
    
    packet = namedtuple("packet", ["seq_num", "packet_type", "data", "acked"])
    ack = namedtuple("packet", ["seq_num", "packet_type"])
    
    def __init__(self, data, sequence_number):
        self.data = data
        self.data_size = len(data)
        self.sequence_number = sequence_number
        self.type = DATA_ID
        self.acked = False
        
    def pack(self):
        raw_pkt = pack('iH' + str(len(self.data)) + 's', self.sequence_number, self.type, self.data)
        # print "pack sequence number" + str(self.sequence_number)
        return raw_pkt
    
    def unpack(self, raw_packet):
        s = len(raw_packet)
        pkt_unpacked = unpack('iH' + str(len(raw_packet) - HEADER_LEN) + 's', raw_packet) + (False,)
        p = self.packet._make(pkt_unpacked)
        
        self.sequence_number = p.seq_num
        # print "p.seqnum: " + str(p.seq_num)
        # print "unpack" + str(self.sequence_number)
        self.data = p.data
        self.data_size = len(self.data)
        self.type = p.packet_type
        self.acked = p.acked
        
    def create_raw_start(self, seq_num):
        self.data = ""
        self.type = START_ID
        self.acked = False
        
        # print "no ack seq_num %d " % seq_num
        self.sequence_number = seq_num
        
        return self.pack()
    
    

    def create_raw_ACK(self, seq_num):
        self.data = ""
        self.type = ACK_ID
        self.acked = False
        
        # print "no ack seq_num %d " % seq_num
        self.sequence_number = seq_num
        
        return self.pack()
    
    def create_raw_NACK(self, seq_num):
        self.data = ""
        self.type = NACK_ID
        self.acked = False
        
        # print "no ack seq_num %d " % seq_num
        self.sequence_number = seq_num
        
        return self.pack()
    
    def is_start(self):
        if self.type == START_ID:
            return True
        else:
            return False
    
    def is_ACK(self):
        if self.type == ACK_ID:
            return True
        else:
            return False
            