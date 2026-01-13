#listener_socket = create_tcp_server_socket(address, port, queue_size)
"""
Aplicações Distribuídas - Projeto 2 - sock_utils.py
Grupo: 23
Números de aluno: Maria Jerónimo 56887, Lara Ângelo 56945
"""
import socket as s

def create_tcp_server_socket(address, port, queue_size):
	sock = s.socket(s.AF_INET, s.SOCK_STREAM) 
	sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1) 
	sock.bind((address, port)) 
	sock.listen(queue_size) 
	return sock

def create_tcp_client_socket(address, port):
	sock = s.socket(s.AF_INET, s.SOCK_STREAM) 
	sock.connect((address, port))
	return sock


def receive_all(socket, length):
	data = bytearray()  #retorna um array de bytes
	while len(data) < length:
		packet = socket.recv(length - len(data))	
		data.extend(packet) # = a append	
	return data
