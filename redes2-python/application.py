# coding=UTF-8

import client
import logger
import server
import socket


def interface_choose_mode():
#     print "Escolha o modo:"
#     print "1) Cliente."
#     print "2) Servidor."
#     print "q) Sair."
#     
#     mode = raw_input()
#     
#     if mode == "1":
#         print "Modo <Cliente> selecionado."
#         start_client_mode()
#     elif mode == "2":
#         print "Modo <Servidor> selecionado."
#         start_server_mode()
#     elif mode == "q":
#         print "Saindo."
#     else:
#         print "Modo inválido. Tente novamente."
#         interface_choose_mode()

    start_server_mode()

def start_client_mode():
#     print "IP"
#     UDP_IP = raw_input()
#     print "PORT"
#     UDP_port = raw_input()
    
    connection_info = {'IP': "", 'port': ""}
    
    complete_with_default(connection_info)
    
    print connection_info['IP']
    
    if not valid_IP(connection_info['IP']):
        print "IP inválida."
        start_client_mode()
        return
    if not valid_port(connection_info['port']):
        print "Porta inválida."
        start_client_mode()
        return
    
    c_client = client.Client(connection_info['IP'], int(connection_info['port']))
    
    while True:
        message = raw_input()
        c_client.send(message)
        
def start_server_mode():
    s_server = server.Server("127.0.0.1", 9001)
    s_server.listen()

def valid_IP(IP):
    try:
        socket.inet_aton(IP)
        return True
    except socket.error:
        return False

def valid_port(port):
    # TODO
    return True

def complete_with_default(connection_info):
    default_IP = "127.0.0.1"
    default_port = "9001"
    
    if connection_info['IP'].__len__() < 7:
        connection_info['IP'] = default_IP
        connection_info['port'] = default_port
        
interface_choose_mode()

















# html = logger.LoggerHTML("testehtml.html")
# txt1 = logger.LoggerFile("teste1.txt")
# txt2 = logger.LoggerFile("teste2.txt")
# x = logger.Logger()
# 
# c = client.Client("127.0.0.1", 5005)
# s = server.Server("127.0.0.1", 5005)
# c.add_logger(html)
# c.add_logger(txt1)
# c.add_logger(txt2)
# c.add_logger(x)
# 
# c.log("as mensagens vão para todos os logs")
# c.log("e como se todos fossem 'observers'")
# c.log("mas não são")
# c.log("huhuhu")
# 
# c.send("banana")


















