#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - lock_client.py
Grupo: 23
Números de aluno: 56887, 56945
"""
# Zona para fazer imports
import sys, time, net_client

# Programa principal

ID = sys.argv[1] # id unico do cliente   
HOST = sys.argv[2] #'127.0.0.1'
PORT = int(sys.argv[3]) #9999

cliente = net_client.server_connection(HOST, PORT)

while True:
	try:

		mensagem = input('comando > ')
		info = mensagem.split()

		if info[0] == "EXIT" and len(info) == 1:
			sys.exit(0)

		elif len(mensagem) == 0:
			print('UNKNOWN COMMAND')
		
		elif info[0] == 'LOCK-W' or info[0] == 'LOCK-R' and len(info) <= 3:
			if len(info) < 3:
				print('MISSING ARGUMENTS')
			else:
				envia = info[0] + ' ' + info[1] + ' ' + info[2] + ' ' + ID
				print ("Cliente: " + str(envia))
				cliente.connect()   
				resposta = cliente.send_receive(envia)
				print("Servidor: " + resposta.decode())
				cliente.close()

		elif info[0] == 'UNLOCK-W' or info[0] == 'UNLOCK-R' and len(info) <= 2:
			if len(info) < 2:
				print('MISSING ARGUMENTS')
			else:
				envia = info[0] + ' ' + info[1] + ' ' + ID
				print ("Cliente: " + str(envia))
				cliente.connect()
				resposta = cliente.send_receive(envia)
				print("Servidor: " + resposta.decode())
				cliente.close()

		elif info[0] == 'STATUS' and len(info) <= 2: #Servidor retorna o estado de um determinado recurso (UNLOCKED, LOCKED-W, LOCKED-R, DISABLED)
			if len(info) < 2:
				print('MISSING ARGUMENTS')
			else:
				envia = info[0] + ' ' + info[1]
				print ("Cliente: " + str(envia))
				cliente.connect()
				resposta = cliente.send_receive(envia)
				print("Servidor: " + resposta.decode())
				cliente.close()

		elif info[0] == 'STATS': 
			if len(info) < 2: 
				print('MISSING ARGUMENTS')
			else:
				if info[1] in ['K','N','D'] and len(info) <= 3:
					if info[1] == 'K' and len(info) != 3 :
						print('MISSIG ARGUMENTS')

					if info[1] == 'K' and len(info) == 3: #Servidor retorna o número de bloqueios de escrita nesse recurso
						recurso = info[2]
						envia = info[0] + ' ' + info[1] + ' ' + recurso
						print ("Cliente: " + str(envia))
						cliente.connect()
						resposta = cliente.send_receive(envia)
						print("Servidor: " + resposta.decode())
						cliente.close()
					
					if info[1] == 'N' and len(info) == 2: #Servidor retorna o nº total de recursos disponíveis atualmente (UNLOCKED)
						envia = info[0] + ' ' + info[1]
						print ("Cliente: " + str(envia))
						cliente.connect()
						resposta = cliente.send_receive(envia)
						print("Servidor: " + resposta.decode())
						cliente.close()
					
					if info[1] == 'D' and len(info) == 2:#Servidor retorna o número total de recursos debilitados atualmente (DISABLED)
						envia = info[0] + ' ' + info[1]
						print ("Cliente: " + str(envia))
						cliente.connect()
						resposta = cliente.send_receive(envia)
						print("Servidor: " + resposta.decode())
						cliente.close()
				else:
					print('UNKNOWN COMMAND')

		elif info[0] == 'PRINT' and len(info) == 1:
			envia = info[0] 
			print ("Cliente: " + str(envia))
			cliente.connect()
			resposta = cliente.send_receive(envia)
			print("Servidor: " + resposta.decode())
			cliente.close()

		elif info[0] == 'SLEEP' and len(info) == 2:
			time.sleep(int(info[1]))

		else:
			print('UNKNOWN COMMAND')


	except KeyboardInterrupt:
		print ('\nLeaving...')
		sys.exit(0)
