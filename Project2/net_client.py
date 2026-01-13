# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 2 - net_client.py
Grupo: 23
Números de aluno: Maria Jerónimo 56887, Lara Ângelo 56945
"""

# zona para fazer importação

import sock_utils, pickle, struct

# definição da classe server_connection 

class server_connection:
    """
    Abstrai uma ligação a um servidor TCP. Implementa métodos para: estabelecer 
    a ligação; envio de um comando e receção da resposta; terminar a ligação.
    """
    def __init__(self, address, port):
        """
        Inicializa a classe com parâmetros para funcionamento futuro.
        """
        self.address = address
        self.port = port
        
    def connect(self):
        """
        Estabelece a ligação ao servidor especificado na inicialização.
        """
        self.sock = sock_utils.create_tcp_client_socket(self.address, self.port)
        # pq o create_tcp_client_socket ja tem o connect 

    def send_receive(self, data):
        """
        Envia os dados contidos em data para a socket da ligação, e retorna
        a resposta recebida pela mesma socket.
        """
        #Recebe a msg do cliente
        dados = pickle.dumps(data,-1) #[10, tipo, num_recurso, time_limit, client_id] 
        #Envia a msg ao servidor
        dados_size = struct.pack('i', len(dados)) #tamanho da msg
        self.sock.sendall(dados_size) #envias o tamanho da msg
        self.sock.sendall(dados) #envias a msg

        #Recebe a resposta do servidor
        resp_size_bytes = self.sock.recv(4) #tamanho em bytes
        resp_size = struct.unpack('i', resp_size_bytes)[0] #obtem o tamanho
        resposta_bytes = sock_utils.receive_all(self.sock, resp_size) #recebe a msg em bytes
        resposta = pickle.loads(resposta_bytes) #traduz a mensagem
        #---------------------------------
        return resposta
    
    def close(self):
        """
        Termina a ligação ao servidor.
        """
        self.sock.close()