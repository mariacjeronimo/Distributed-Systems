"""
Aplicações Distribuídas - Projeto 2 - lock_skel.py
Grupo: 23
Números de aluno: Maria Jerónimo 56887, Lara Ângelo 56945
"""
import pickle
from lock_pool import lock_pool

class lock_skel: 
	def __init__(self, N, K):
		self.pool = lock_pool(N, K)
	
	def bytesToList(self, msg_bytes):
		return pickle.loads(msg_bytes)

	def listToBytes(self, resposta):
		return pickle.dumps(resposta) 

	def clear_expired_locks(self):
		self.pool.clear_expired_locks()

	def processMessage(self, msg_bytes):
		pedido = self.bytesToList(msg_bytes)

		print("Pedido do cliente: ", pedido)

		resposta = []

		if pedido == None or len(pedido) == 0:
			resposta.append('INVALD MESSAGE')
		else:
			if pedido[0] == 10: #lock [10, tipo, num_recurso, time_limit, client_id]
				tipo = pedido[1]				
				id_recurso = int(pedido[2])
				id_cliente = int(pedido[4])
				limite_tempo = int(pedido[3]) 
				resposta.append(11)
				resposta.append(self.pool.lock(tipo, id_recurso, id_cliente, limite_tempo)) 

			elif pedido[0] == 20: #unlock 
				tipo = pedido[1]
				id_recurso = int(pedido[2])
				id_cliente = int(pedido[3])
				resposta.append(21)
				resposta.append(self.pool.unlock(tipo, id_recurso, id_cliente))

			elif pedido[0] == 30: #status
				id_recurso = int(pedido[1])
				resposta.append(31)
				resposta.append(self.pool.status(id_recurso))
			
			elif pedido[0] == 40: #stats k
				id_recurso = int(pedido[1])
				resposta.append(41)
				resposta.append(self.pool.stats('K', id_recurso)) 
			
			elif pedido[0] == 50: #stats N
				resposta.append(51)
				resposta.append(self.pool.stats('N',0)) 
			
			elif pedido[0] == 60: #stats D
				resposta.append(61)
				resposta.append(self.pool.stats('D',0)) 
			
			elif pedido[0] == 70: #print
				resposta.append(71)
				resposta.append(str(self.pool))


			else:
				resposta.append('INVALID MESSAGE')

		print("Resposta do servidor: ", resposta)
		return self.listToBytes(resposta)