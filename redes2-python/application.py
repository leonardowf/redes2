# coding=UTF-8

import client
import logger
import server
import socket


def interface_choose_mode():
    print "Escolha o modo:"
    print "1) Cliente."
    print "2) Servidor."
    print "q) Sair."
     
    mode = raw_input()
     
    if mode == "1":
        print "Modo <Cliente> selecionado."
        start_client_mode()
    elif mode == "2":
        print "Modo <Servidor> selecionado."
        start_server_mode()
    elif mode == "q":
        print "Saindo."
    else:
        print "Modo inválido. Tente novamente."
        interface_choose_mode()


def start_client_mode():
#     print "IP"
#     UDP_IP = raw_input()
#     print "PORT"
#     UDP_port = raw_input()
    
    print "Digite o ip do servidor"
    server_IP = raw_input()
    
    print "Digite a porta do servidor"
    server_port = raw_input()
        
    if not valid_IP(server_IP):
        print "IP inválida."
        start_client_mode()
        return
    
    # c_client = client.Client(connection_info['IP'], int(connection_info['port']))
    a_logger = logger.Logger()
    a_logger_file = logger.LoggerFile("log_cliente.txt")
    
    print "Perder mensagens com % (exemplo: 20)"
    lost_percent = int(raw_input())
    
    print "Duplicar mensagens com % (exemplo: 20)"
    duplicate_percent = int(raw_input())
    
    while True:
        print ">",
        message = raw_input()
        c_client = client.Client(server_IP, int(server_port))
        c_client.lost_percentage = lost_percent
        c_client.duplicate_percentage = duplicate_percent
        c_client.add_logger(a_logger)
        c_client.add_logger(a_logger_file)
        c_client.send(message)
        
def start_server_mode():
    s_server = server.Server("127.0.0.1", 9001)
    a_logger = logger.Logger()
    a_logger_file = logger.LoggerFile("log_servidor.txt")
    s_server.add_logger(a_logger)
    s_server.add_logger(a_logger_file)
    
    s_server.listen()

def valid_IP(IP):
    try:
        socket.inet_aton(IP)
        return True
    except socket.error:
        return False
        
interface_choose_mode()





























