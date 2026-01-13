#listener_socket = create_tcp_server_socket(address, port, queue_size)
"""
Aplicações Distribuídas - Projeto 1 - sock_utils.py
Grupo: 23
Números de aluno: 56887, 56945
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
	data = "" 
	count = 0
	while count < length:
		packet = socket.recv(length - count)	
		count += len(packet)	
		data += packet
	return data