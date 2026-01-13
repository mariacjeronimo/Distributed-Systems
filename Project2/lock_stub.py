"""
Aplicações Distribuídas - Projeto 2 - lock_stub.py
Grupo: 23
Números de aluno: Maria Jerónimo 56887, Lara Ângelo 56945
"""
import socket as s
import net_client
class lock_stub: 

    def __init__(self, adress, port):
        self.server = net_client.server_connection(adress, port)
        self.server.connect()

    def disconnect(self): 
        self.server.close()

    def send_info(self, msg):
        if msg[0] == 'LOCK':     #tipo  n_recurso limite  id_cliente
            resposta = self.lock(msg[1], msg[2], msg[3], msg[4])
        elif msg[0] == 'UNLOCK': #tipo  n_recurso id_cliente
            resposta = self.unlock(msg[1], msg[2], msg[3])
        elif msg[0] == 'STATUS': #n_recurso
            resposta = self.status(msg[1])
        elif msg[0] == 'STATS':
            if msg[1] == "K":		#n_recurso
                resposta = self.statsK(msg[2])
            elif msg[1] == "N":
                resposta = self.statsN()
            else:
                resposta = self.statsD()
        elif msg[0] == 'PRINT':   
            resposta = self.print()
        return resposta
        
    def lock(self, tipo, num_recurso, time_limit, client_id): 
        info = [10, tipo, num_recurso, time_limit, client_id]
        print("Pedido do cliente: ", info)
        resposta = self.server.send_receive(info)
        return resposta
    
    def unlock(self, tipo, num_recurso, client_id):
        info = [20, tipo, num_recurso, client_id]
        print("Pedido do cliente: ", info)
        resposta = self.server.send_receive(info)
        return resposta
    
    def status(self, num_recurso):
        info = [30, num_recurso]
        print("Pedido do cliente: ", info)
        resposta = self.server.send_receive(info)
        return resposta
    
    def statsK(self, num_recurso):
        info = [40, num_recurso]
        print("Pedido do cliente: ", info)
        resposta = self.server.send_receive(info)
        return resposta
    
    def statsN(self):
        info = [50]
        print("Pedido do cliente: ", info)
        resposta = self.server.send_receive(info)
        return resposta

    def statsD(self):
        info = [60]
        print("Pedido do cliente: ", info)
        resposta = self.server.send_receive(info)
        return resposta
    
    def print(self):
        info = [70]
        print("Pedido do cliente: ", info)
        resposta = self.server.send_receive(info)
        return resposta
