"""
Aplicações Distribuídas - Projeto 2 - lock_server.py
Grupo: 23
Números de aluno: Maria Jerónimo 56887, Lara Ângelo 56945
"""
###############################################################################
import select
import lock_skel, sys, sock_utils, struct, argparse
# código do programa principal


parser = argparse.ArgumentParser(prog='lock_server')
parser.add_argument('host', type=str, nargs=1, help='o hostname do servidor que fornece os recursos')
parser.add_argument('port', type=int, nargs=1, help='o porto TCP onde escutará por pedidos de ligação')
parser.add_argument('N', type=int, nargs=1, help='numero de recursos q serao geridos pelo servidor')
parser.add_argument('K', type=int, nargs=1, help='numero de bloqueios permitidos em cada recurso')

argumentos = parser.parse_args()
# print(vars(argumentos))

HOST = argumentos.host[0] #'127.0.0.1'
PORT = argumentos.port[0] #9999
N = argumentos.N[0]
K = argumentos.K[0]

skeleton = lock_skel.lock_skel(N, K) #Definimos os recursos 
listen_socket  = sock_utils.create_tcp_server_socket(HOST, PORT, 1)
print("Starting to listen...\n")

socket_list = [listen_socket, sys.stdin] 

while True:
    try:
        R, W, X = select.select(socket_list, [], [])
        for sckt in R:
            if sckt is listen_socket: # Se for a socket de escuta... aceita uma nova ligacao
                conn_sock, addr = sckt.accept() 
                addr, port = conn_sock.getpeername() 
                print('Novo cliente ligado desde %s:%d' % (addr, port)) 
                socket_list.append(conn_sock)  # Adiciona ligação à lista 
            elif sckt is sys.stdin:
                msg = sckt.readline().strip()
                if msg == "EXIT":
                    sys.exit(0)
            else:
                skeleton.clear_expired_locks() #verifica se recursos já podem ser desbloqueados (se o seu tempo de bloqueio já passou ou não, se sim desbloquea os)
                #Recebe a msg do cliente
                req_size_byte = sckt.recv(4) #tamanho em bytes
                req_size = struct.unpack('i', req_size_byte)[0] #obtem tamanho
                req = sock_utils.receive_all(sckt, req_size) #recebe msg em bytes
                #obtem a resposta
                resposta = skeleton.processMessage(req)
                #envia a resposta
                resposta_size = struct.pack('i', len(resposta))
                sckt.sendall(resposta_size)
                sckt.sendall(resposta)
    
    except KeyboardInterrupt:
        print("\nLeaving...")
        sckt.close()
        sys.exit(0) 

    except struct.error:
        address, port = sckt.getpeername()
        print ("Client {0} disconnected.".format(str((address, port))))
        socket_list.remove(sckt)

    except:
        resposta = 'INVALID ARGUMENT'


    # finally:
    #     sckt.close()

listen_socket.close()