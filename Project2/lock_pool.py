#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 2 - lock_pool.py
Grupo: 23
Números de aluno: Maria Jerónimo 56887, Lara Ângelo 56945
"""

# Zona para fazer importação
import time
###############################################################################

tipo_recurso = '' #variavel global

class resource_lock:
    
    def __init__(self, resource_id): #inicializa um recurso (id,status,tempo,[clientes])
        """
        Define e inicializa as propriedades do recurso para os bloqueios.
        """
        self.resource_id = resource_id  
        self.status = 'UNLOCKED'
        self.time_limit = 0 #ultimo cliente
        self.clients_r = []
        self.clients_w = []
        self.bloqueios_escrita = []
        self.bloqueios_leitura = []
        self.contador_bloqueios_w = 0
        self.contador_bloqueios_r = 0

    def set_max_bloqueios(self, numero_maximo):
        self.max_bloqueios = numero_maximo

    def lock(self, type, client_id, time_limit):
        """
        Tenta bloquear o recurso pelo cliente client_id, durante time_limit 
        segundos. Retorna True ou False. O bloqueio pode ser de escrita (type=W)
        ou de leitura (type=R).
        """
        if type == "W": 
            if self.status == "UNLOCKED":
                if self.max_bloqueios > self.contador_bloqueios_w: 
                    self.status = "LOCKED-W"        
                    self.clients_w.append(client_id)
                    self.contador_bloqueios_w += 1
                    self.time_limit = time.time() + time_limit # deadline 
                    self.bloqueios_escrita.append((client_id, self.time_limit))
                    resposta = True
                else:
                    self.status = "DISABLED"
                    resposta = False
            elif self.status == "LOCKED-W" or self.status == "LOCKED-R" or self.status == "DISABLED":
                resposta = False
        elif type == "R": 
            if self.status == "LOCKED-R" or self.status == "UNLOCKED":
                self.time_limit = time.time() + time_limit # deadline
                self.contador_bloqueios_r += 1
                self.bloqueios_leitura.append((client_id,self.time_limit))
                self.status = "LOCKED-R"    
                if self.clients_r == []:
                    self.clients_r.append(client_id)
                else:
                    if client_id not in self.clients_r:
                        self.clients_r.append(client_id)
                resposta = True
            elif self.status == "LOCKED-W" or self.status == "DISABLED":
                resposta = False
        else:
            resposta = None
        return resposta


    def release(self):
        """
        Liberta o recurso incondicionalmente, alterando os valores associados
        ao bloqueio.
        """
        lista_indice = []
        if tipo_recurso == "LOCKED-W" and self.max_bloqueios > self.contador_bloqueios_w:
            self.status = "UNLOCKED"
            self.bloqueios_escrita = []
            self.time_limit = 0
        if tipo_recurso == "LOCKED-W" and self.max_bloqueios <= self.contador_bloqueios_w:
            self.status = "DISABLED"
        if tipo_recurso == "LOCKED-R":
            for tuplo_i in range(len(self.bloqueios_leitura)): # iterar indices dos tuplos de  bloqueios_leitura do recusro atual[(id_cliente1, deadline1),(id_cliente2, deadline2),...] 
                if self.bloqueios_leitura[tuplo_i][1] < time.time(): #se deadline  do tuplo atual expirou
                    lista_indice.append(tuplo_i) #guarda o indice do tuplo que se pretende eliminar
            for x in lista_indice: 
                cliente = self.bloqueios_leitura[x][0]  
                self.clients_r.remove(cliente) #remove o cliente da lista de clients_r
                self.bloqueios_leitura.pop(x) #remove o tuplo do indice respetivo da lista de bloqueios_leitura
                self.contador_bloqueios_r -= 1
                
            if len(self.bloqueios_leitura) == 0:
                    self.status = "UNLOCKED"



    def unlock(self, type, client_id):
        """
        Liberta o recurso se este está bloqueado pelo cliente client_id.
        Retorna True ou False.O desbloqueio pode ser relacionado a bloqueios 
        de escrita (type=W) ou de leitura (type=R), consoante o tipo.
        """

        if type == "W":
            if self.status == "LOCKED-W" and client_id in self.clients_w: 
                self.bloqueios_escrita.remove((client_id,self.time_limit))
                self.clients_w.remove(client_id)
                self.status = "UNLOCKED"
                resposta = True
            elif self.status == "UNLOCKED" or self.status == "DISABLED" or client_id not in self.clients_w: 
                resposta = False
        elif type == "R":
            if self.status == "LOCKED-R" and client_id in self.clients_r: 
                self.bloqueios_leitura=[tuplo for tuplo in self.bloqueios_leitura if tuplo[0]!=client_id] 
                self.contador_bloqueios_r -= 1
                self.clients_r.remove(client_id)
                resposta = True
                if self.bloqueios_leitura == []:
                    self.status = "UNLOCKED"   
            elif self.status == "LOCKED-W" or self.status == "UNLOCKED" or client_id not in self.clients_r: 
                resposta = False
        else:
            resposta = None
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
        if self.bloqueios_leitura != []:
            max_time_limit = []
            for tuplo in self.bloqueios_leitura:
                max_time_limit.append(tuplo[1])
            ultimo_deadline = max(max_time_limit)
        if self.bloqueios_escrita != []:
            tuplo_e  = self.bloqueios_escrita[0]
            cliente = tuplo_e[0]
            tempo = tuplo_e[1]
        if self.status == 'LOCKED-W':
            output += "R " + str(self.resource_id) + " LOCKED-W " + str(self.stats()) + " " + str(cliente) + " " + str(tempo)
        elif self.status == 'LOCKED-R':
            output += "R " + str(self.resource_id) + " LOCKED-R " + str(self.stats()) + " " + str(self.contador_bloqueios_r) + " " + str(ultimo_deadline)
        elif self.status == "UNLOCKED":
            output += "R " + str(self.resource_id) + " UNLOCKED"
        elif self.status == "DISABLED":
            output += "R " + str(self.resource_id) + " DISABLED"
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
        self.conjunto = [resource_lock(i) for i in range(1,self.n_recursos+1)] # definicao do array
        for recurso in self.conjunto:
            recurso.set_max_bloqueios(K)


    def clear_expired_locks(self):
        """
        Verifica se os recursos que estão bloqueados ainda estão dentro do tempo
        de concessão dos bloqueios. Remove os bloqueios para os quais o tempo de
        concessão tenha expirado.
        """
        global tipo_recurso
        for i in range(self.n_recursos):
            # print('Recurso {}: estado {}'.format(i+1,self.status(i+1)))
            if self.status(i+1) == 'LOCKED-W':
                if self.conjunto[i].time_limit < time.time(): 
                    tipo_recurso = 'LOCKED-W'
                    self.conjunto[i].release()
            if self.status(i+1) == "LOCKED-R":
                tipo_recurso = 'LOCKED-R'
                self.conjunto[i].release()              



    def lock(self, type, resource_id, client_id, time_limit):
        """
        Tenta bloquear (do tipo R ou W) o recurso resource_id pelo cliente client_id, 
        durante time_limit segundos. Retorna True, False ou None.
        """
        if resource_id <= self.n_recursos and resource_id > 0:
            return self.conjunto[resource_id-1].lock(type, client_id, time_limit) # acede ao indice ao qual o resource_id - 1 corresponde na lista  
        else:
            return None

    def unlock(self, type, resource_id, client_id):
        """
        Liberta o bloqueio (do tipo R ou W) sobre o recurso resource_id pelo cliente 
        client_id. Retorna True, Flase ou None.
        """
        if resource_id <= self.n_recursos and resource_id > 0:
            return self.conjunto[resource_id-1].unlock(type, client_id)
        else:
            return None        


    def status(self, resource_id):
        """
        Obtém o estado de um recurso. Retorna LOCKED, UNLOCKED,
        DISABLED ou None.
        """
        if resource_id <= self.n_recursos and resource_id > 0:
            return self.conjunto[resource_id-1].status
        else:
            return None             

    def stats(self, option, resource_id):
        """
        Obtém o estado do serviço de gestão de bloqueios. Se option for K, retorna <número de 
        bloqueios feitos no recurso resource_id> ou None. Se option for N, retorna 
        <número de recursos bloqueados atualmente>. Se option for D, retorna 
        <número de recursos desabilitados>
        """
        if option == 'K':
            if resource_id < 0 or resource_id > self.n_recursos:
                return None
            else: 
                return self.conjunto[resource_id-1].stats()      
                
        elif option == 'N':
            contador_unlocked = 0
            for i in range(self.n_recursos):
                if self.conjunto[i].status == "UNLOCKED":
                    contador_unlocked += 1
            return str(contador_unlocked)


        elif option == "D":
            contador_disabled = 0
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
            output += str(self.conjunto[i]) + "\n"
        return output