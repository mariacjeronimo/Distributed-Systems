#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - lock_server.py
Grupo: 23
Números de aluno: 56887, 56945
"""

# Zona para fazer importação
import time, sys, sock_utils
###############################################################################
class resource_lock:
    contador_bloqueios_w = 0
    contador_bloqueios_r = 0
    
    def __init__(self, resource_id):
        """
        Define e inicializa as propriedades do recurso para os bloqueios.
        """
        self.resource_id = resource_id  
        self.status = 'UNLOCKED'
        self.time_limit = 0
        self.clients = []
        # self.client_id = 0 

    def set_max_bloqueios(self, numero_maximo):
        self.max_bloqueios = numero_maximo

    def lock(self, type, client_id, time_limit):
        """
        Tenta bloquear o recurso pelo cliente client_id, durante time_limit 
        segundos. Retorna OK ou NOK. O bloqueio pode ser de escrita (type=W)
        ou de leitura (type=R).
        """
        if type == "W": 
            if self.status == "UNLOCKED":
                if self.max_bloqueios > self.contador_bloqueios_w: 
                    self.status = "LOCKED-W"        
                    self.clients.append(client_id)
                    self.contador_bloqueios_w += 1
                    self.time_limit = time.time() + time_limit # deadline 
                    bloqueios_escrita.append((client_id, self.time_limit))
                    resposta = "OK"
                else:
                    self.status = "DISABLED"
                    resposta = "NOK"
            elif self.status == "LOCKED-W" or self.status == "LOCKED-R" or self.status == "DISABLED":
                resposta = "NOK"
        elif type == "R": 
            if self.status == "LOCKED-R" or self.status == "UNLOCKED":
                self.time_limit = time.time() + time_limit # deadline
                self.contador_bloqueios_r += 1
                bloqueios_leitura.append((client_id,self.time_limit))
                self.status = "LOCKED-R"    
                if self.clients == []:
                    self.clients.append(client_id)
                else:
                    if client_id not in self.clients:
                        self.clients.append(client_id)
                resposta = "OK"
            elif self.status == "LOCKED-W" or self.status == "DISABLED":
                resposta = "NOK"
        else:
            resposta = "UNKNOWN RESOURCE"
        return resposta


    def release(self):
        """
        Liberta o recurso incondicionalmente, alterando os valores associados
        ao bloqueio.
        """
        self.status = "UNLOCKED"
        self.time_limit = 0
        self.contador_bloqueios_r -= 1

    def unlock(self, type, client_id):
        """
        Liberta o recurso se este está bloqueado pelo cliente client_id.
        Retorna OK ou NOK.O desbloqueio pode ser relacionado a bloqueios 
        de escrita (type=W) ou de leitura (type=R), consoante o tipo.
        """
        if type == "W":
            if self.status == "LOCKED-W" and client_id in self.clients: 
                bloqueios_escrita.remove((client_id,self.time_limit))
                self.clients.remove(client_id)
                self.status = "UNLOCKED"
                resposta = "OK"
            elif self.status == "UNLOCKED" or self.status == "DISABLED" or client_id not in self.clients: 
                resposta = "NOK"
        elif type == "R":
            if self.status == "LOCKED-R" and client_id in self.clients: 
                bloqueios_leitura.remove((client_id,self.time_limit))
                self.contador_bloqueios_r -= 1
                self.clients.remove(client_id)
                resposta = "OK"
                if bloqueios_leitura == []:
                    self.status = "UNLOCKED"   
            elif self.status == "LOCKED-W" or self.status == "UNLOCKED" or client_id not in self.clients: 
                resposta = "NOK"
        else:
            resposta = "UNKNOWN RESOURCE"
        return resposta


    def status(self):
        """
        Obtém o estado do recurso. Retorna LOCKED-W ou LOCKED-R ou UNLOCKED 
        ou DISABLED.
        """
        return self.status


    def stats(self):
        """
        Retorna o número de bloqueios de escrita feitos neste recurso. 
        """
        return str(self.contador_bloqueios_w)

   
    def disable(self):
        """
        Coloca o recurso como desabilitado incondicionalmente, alterando os 
        valores associados à sua disponibilidade.
        """
        self.status = "DISABLED"

    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print ou str.
        """
        output = ""
        # Se o recurso está bloqueado para a escrita:
        # R <num do recurso> LOCKED-W <vezes bloqueios de escrita> <id do cliente> <deadline do bloqueio de escrita>
        # Se o recurso está bloqueado para a leitura:
        # R <num do recurso> LOCKED-R <vezes bloqueios de escrita> <num bloqueios de leitura atuais> <último deadline dos bloqueios de leitura>
        # Se o recurso está desbloqueado:
        # R <num do recurso> UNLOCKED
        # Se o recurso está inativo:
        # R <num do recurso> DISABLED
        if bloqueios_leitura != []:
            max_time_limit = []
            for tuplo in bloqueios_leitura:
                max_time_limit.append(tuplo[1])
            ultimo_deadline = max(max_time_limit)
        if self.status == 'LOCKED-W':
            output += "R " + str(self.resource_id + 1) + " LOCKED-W " + str(self.stats()) + " " + str(self.client_id) + " " + str(self.time_limit)
        elif self.status == 'LOCKED-R':
            output += "R " + str(self.resource_id + 1) + " LOCKED-R " + str(self.stats()) + " " + str(self.contador_bloqueios_r) + " " + str(ultimo_deadline)
        elif self.status == "UNLOCKED":
            output += "R " + str(self.resource_id + 1) + " UNLOCKED"
        elif self.status == "DISABLED":
            output += "R " + str(self.resource_id + 1) + " DISABLED"
        return output

###############################################################################

class lock_pool:
    def __init__(self, N, K):
        """
        Define um array com um conjunto de resource_locks para N recursos. 
        Os locks podem ser manipulados pelos métodos desta classe. 
        Define K, o número máximo de bloqueios de escrita permitidos para cada 
        recurso. Ao atingir K bloqueios de escrita, o recurso fica desabilitado.
        """
        self.n_recursos = N 
        self.conjunto = [resource_lock(i) for i in range(self.n_recursos)] # definicao do array
        for recurso in self.conjunto:
            recurso.set_max_bloqueios(K)

        
    def clear_expired_locks(self):
        """
        Verifica se os recursos que estão bloqueados ainda estão dentro do tempo
        de concessão dos bloqueios. Remove os bloqueios para os quais o tempo de
        concessão tenha expirado.
        """
        for i in range(self.n_recursos):
            if self.status(i) == 'LOCKED-R' or self.status(i) == 'LOCKED-W': 
                if self.conjunto[i].time_limit < time.time(): 
                    self.conjunto[i].release()


    def lock(self, type, resource_id, client_id, time_limit):
        """
        Tenta bloquear (do tipo R ou W) o recurso resource_id pelo cliente client_id, 
        durante time_limit segundos. Retorna OK, NOK ou UNKNOWN RESOURCE.
        """
        if resource_id <= self.n_recursos and resource_id >= 0:
            return self.conjunto[resource_id].lock(type, client_id, time_limit) # acede ao indice ao qual o resource_id corresponde na lista   
        else:
            return "UNKNOWN RESOURCE"

    def unlock(self, type, resource_id, client_id):
        """
        Liberta o bloqueio (do tipo R ou W) sobre o recurso resource_id pelo cliente 
        client_id. Retorna OK, NOK ou UNKNOWN RESOURCE.
        """
        if resource_id <= self.n_recursos and resource_id >= 0:
            return self.conjunto[resource_id].unlock(type, client_id)           


    def status(self, resource_id):
        """
        Obtém o estado de um recurso. Retorna LOCKED, UNLOCKED,
        DISABLED ou UNKNOWN RESOURCE.
        """
        if resource_id <= self.n_recursos and resource_id >= 0:
            return self.conjunto[resource_id].status               

    def stats(self, option, resource_id):
        """
        Obtém o estado do serviço de gestão de bloqueios. Se option for K, retorna <número de 
        bloqueios feitos no recurso resource_id> ou UNKNOWN RESOURCE. Se option for N, retorna 
        <número de recursos bloqueados atualmente>. Se option for D, retorna 
        <número de recursos desabilitados>
        """
        if option == 'K':
            if resource_id < 0 or resource_id > self.n_recursos:
                print("UNKNOWN RESOURCE")
            else: 
                return self.conjunto[resource_id].stats()      
                
        elif option == 'N':
            contador_unlocked = 0
            if resource_id < 0 or resource_id > self.n_recursos:
                print("INVALID COMMAND")
            else:
                for i in range(self.n_recursos):
                    if self.conjunto[i].status == "UNLOCKED":
                        contador_unlocked += 1
                return str(contador_unlocked)

        elif option == "D":
            contador_disabled = 0
            if resource_id < 0 or resource_id > self.n_recursos:
                print("INVALID COMMAND")
            else:
                for i in range(self.n_recursos):
                    if self.conjunto[i].status == "DISABLED":
                        contador_disabled += 1
                return str(contador_disabled)
            

    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print ou str.
        """
        output = ""
        #
        # Acrescentar no output uma linha por cada recurso
        #
        for i in range(self.n_recursos):
            output += self.conjunto[i].__repr__() + "\n"
        return output

###############################################################################

# código do programa principal

HOST = sys.argv[1] #'127.0.0.1'
PORT = int(sys.argv[2]) #9999
N = int(sys.argv[3])
K = int(sys.argv[4])

listen_socket  = sock_utils.create_tcp_server_socket(HOST, PORT, 1)
print("Starting to listen...\n")
pool =  lock_pool(N, K)

bloqueios_escrita = []
bloqueios_leitura = []

while True:
    try:
        resposta = ""
        (conn_sock, addr) = listen_socket.accept() #addr = (host, port)
        IP = addr[0]
        port = addr[1]
        print(f"Accepted connection to {IP} in {port}\n")

        pool.clear_expired_locks()

        # print("OLA")

        mensagem_cliente = conn_sock.recv(1024)
        mensagem_cliente_str = mensagem_cliente.decode()
        print("Cliente: " + mensagem_cliente_str)
        mensagem_split = mensagem_cliente_str.split(" ") #['LOCK-W', 0, 120, 1]


        if mensagem_split[0] == "LOCK-R" or mensagem_split[0] == "LOCK-W":
            tipo = mensagem_split[0].split("-")[1] #['LOCK', 'W'] neste acede ao W o type
            id_recurso = int(mensagem_split[1])
            id_cliente = int(mensagem_split[3])
            limite_tempo = int(mensagem_split[2])
            resposta = pool.lock(tipo, id_recurso, id_cliente, limite_tempo)
            print("Servidor: " + resposta)

        elif mensagem_split[0] == "UNLOCK-R" or mensagem_split[0] == "UNLOCK-W":
            tipo = mensagem_split[0].split("-")[1] #['LOCK', 'W'] neste acede ao W o type
            id_recurso = int(mensagem_split[1])
            id_cliente = int(mensagem_split[2])
            resposta = pool.unlock(tipo, id_recurso, id_cliente)
            print("Servidor: " + resposta)

        elif mensagem_split[0] == "STATUS":
            id_recurso = int(mensagem_split[1])
            resposta = pool.status(id_recurso)
            print("Servidor: " + resposta)
        
        elif mensagem_split[0] == "STATS":
            if mensagem_split[1] == "K":
                tipo = mensagem_split[1]
                id_recurso = int(mensagem_split[2])
                resposta = pool.stats(tipo, id_recurso)
                print("Servidor: " + resposta)
            elif mensagem_split[1] == "N" or mensagem_split[1] == "D":
                tipo = mensagem_split[1]
                resposta = pool.stats(tipo, 0)
                print("Servidor: " + resposta)

        elif mensagem_split[0] == "PRINT":
            resposta = pool.__repr__()
            print("Servidor: " + resposta)

        conn_sock.sendall(resposta.encode('utf-8'))
        conn_sock.close()
    
    except KeyboardInterrupt:
        print("\nLeaving...")
        sys.exit(0) 

    except:
        resposta = 'INVALID ARGUMENT'
        conn_sock.sendall(resposta.encode('utf-8'))

    finally:
        conn_sock.close()

listen_socket.close()