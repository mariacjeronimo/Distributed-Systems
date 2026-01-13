README Grupo23 Números: 56887, 56945

Existem 7 comandos à disposição: 

-> LOCK: <R|W> <número do recurso> <limite de tempo> Exemplo: LOCK-R 0 30

-> UNLOCK: <R|W> <número do recurso> Exemplo: UNLOCK-R 0

-> STATUS: <número do recurso> Exemplo: STATUS 0

-> STATS: K <número do recurso> Exemplo: STATS K 0; N	Exemplo: STATS N; D Exemplo: STATS D

-> PRINT: Exemplo: PRINT

-> EXIT: Exemplo: EXIT

-> SLEEP: <limite de tempo> Exemplo: SLEEP 30


Todos os comandos explicitos no enunciado estão a funcionar como pretendido, exceto um caso em especifico.


Limitações:
 -> Ao usar multiplos clientes (tentamos com 2), ambos conseguem fazer o bloqueio de leitura do mesmo recurso, o que é de esperar, porém, apenas o último cliente a fazer o bloqueio consegue desbloquear o recurso. 


Execução do servidor:

lock_server.py <hostname> <porto TCP> <número de recursos> <número máximo de bloqueios> 

- hostname: onde o servidor fornecerá os recursos;
- porto TCP: onde escutará por pedidos de ligação;
- número de recursos: número de recursos que serão geridos pelo servidor;
- número máximo de bloqueios: número máximo de bloqueios permitidos em cada recurso. 

Exemplo: python3 lock_server.py localhost 9999 4 3


Execução do cliente:

lock_client.py <número de cliente> <hostname> <porto TCP> 
 
- número de cliente: o id único do cliente;
- hostname: do servidor que fornece os recursos;
- porto TCP: onde o servidor recebe pedidos de ligação;

Exemplo: python3 lock_client.py 1 localhost 9999

Após iniciar o cliente ele ficará à espera do seguinte comando: 'comando > ', deve inserir um dos 7 comandos disponíveis: LOCK, UNLOCK, STATUS, STATS, PRINT, EXIT ou SLEEP.