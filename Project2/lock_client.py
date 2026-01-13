#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 2 - lock_client.py
Grupo: 23
Números de aluno: Maria Jerónimo 56887, Lara Ângelo 56945
"""
# Zona para fazer imports
import sys, time, lock_stub, argparse

# Programa principal
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog='lock_client')
    parser.add_argument('client_id', type=int, nargs=1, help=' define o id do cliente')
    parser.add_argument('host', type=str, nargs=1, help='o hostname do servidor que fornece os recursos')
    parser.add_argument('port', type=int, nargs=1, help='o porto TCP onde o servidor recebe os pedidos de ligação')

    argumentos = parser.parse_args()
    # print(vars(argumentos)) #imprime o dicionario com os argumentos passados no terminal

    ID = argumentos.client_id[0] #id unico do cliente 
    HOST = argumentos.host[0] #'127.0.0.1'
    PORT = argumentos.port[0] #9999

    stub = lock_stub.lock_stub(HOST, PORT)  #este abre a connection (class lock_stub do file lock_stub)

    while True:
        try:
            mensagem = input('comando > ')
            info = mensagem.split()
            if len(mensagem) == 0:
                print('UNKNOWN COMMAND')
                
            elif info[0] == "EXIT" and len(info) == 1:
                sys.exit(0)

            elif info[0] == 'LOCK' and len(info) <= 4:
                if len(info) < 4:
                    print('MISSING ARGUMENTS')
                else:
                    try: #para mudar o tipo de argumento de str para int
                        envia = list(map(int, [info[2],info[3]])) #n_recurso e time_limit [1,2]
                        envia.insert(0,info[0]) #LOCK ['LOCK', 1 ,2]
                        envia.insert(1,info[1]) #tipo ['LOCK', 'R', 1, 2]
                        envia.append(ID) #n_id  ['LOCK', 'R', 1, 2, 1]
                        resposta = stub.send_info(envia)
                        print('Resposta do servidor: ', resposta)
                    except:
                        print('INVALID COMMAND')
            
            elif info[0] == 'UNLOCK' and len(info) <= 3:
                if len(info) < 3:
                    print('MISSING ARGUMENTS')
                else:
                    try:
                        envia = list(map(int, [info[2]])) #n_recurso
                        envia.insert(0,info[0]) #UNLOCK
                        envia.insert(1,info[1]) #tipo
                        envia.append(ID) #n_id
                        resposta = stub.send_info(envia)
                        print('Resposta do servidor: ', resposta)
                    except:
                        print('INVALID COMMAND')
            
            elif info[0] == 'STATUS' and len(info) <= 2:
                if len(info) < 2:
                    print('MISSING ARGUMENTS')
                else:
                    try:
                        envia = list(map(int, [info[1]])) #n_recurso
                        envia.insert(0,info[0]) #STATUS
                        resposta = stub.send_info(envia)
                        print('Resposta do servidor: ', resposta)
                    except:
                        print('INVALID COMMAND')

            elif info[0] == 'STATS':
                if len(info) < 2:
                    print('MISSING ARGUMENTS')
                else:
                    if info[1] in ['K','N','D'] and len(info) <= 3:
                        if info[1] == 'K' and len(info) < 3:
                            print('MISSING ARGUMENTS')

                        if info[1] == 'K' and len(info) == 3: #Servidor retorna o número de bloqueios de escrita nesse recurso
                            try:
                                envia = list(map(int, [info[2]])) #n_recurso
                                envia.insert(0,info[0]) #STATS
                                envia.insert(1,info[1]) #tipo
                                resposta = stub.send_info(envia)
                                print('Resposta do servidor: ', resposta)
                            except:
                                print('INVALID COMMAND')
                        
                        if info[1] == 'N' and len(info) == 2: #Servidor retorna o nº total de recursos disponíveis atualmente (UNLOCKED)
                            try:
                                envia = []
                                envia.insert(0,info[0]) #STATS
                                envia.insert(1,info[1]) #tipo
                                resposta = stub.send_info(envia)
                                print('Resposta do servidor: ', resposta)
                            except:
                                print('INVALID COMMAND') 

                        if info[1] == 'D' and len(info) == 2: #Servidor retorna o número total de recursos debilitados atualmente (DISABLED)
                            try:
                                envia = []
                                envia.insert(0,info[0]) #STATS
                                envia.insert(1,info[1]) #tipo
                                resposta = stub.send_info(envia)
                                print('Resposta do servidor: ', resposta)
                            except:
                                print('INVALID COMMAND')
                    else:
                        print('UNKNOWN COMMAND')

            elif info[0] == 'PRINT' and len(info) == 1:
                envia = []
                envia.insert(0,info[0]) #PRINT
                resposta = stub.send_info(envia)
                print('Resposta do servidor: ', resposta)


            elif info[0] == 'SLEEP' and len(info) == 2:
                time.sleep(int(info[1]))

            else:
                print('UNKNOWN COMMAND')

        except ValueError:
            print ("ID must be an int value")

        except KeyboardInterrupt:
            print ('\nLeaving...')
            sys.exit(0)
            
    stub.disconnect()
