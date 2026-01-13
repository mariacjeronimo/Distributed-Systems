README 
Grupo 23 
Números: Maria Jerónimo 56887, Lara Ângelo 56945

----------------------------------------------------------------------------------------------------
Existem 7 comandos à disposição: 
-> LOCK: <R|W> <número do recurso> <limite de tempo> Exemplo: LOCK R 1 30

-> UNLOCK: <R|W> <número do recurso> Exemplo: UNLOCK R 1

-> STATUS: <número do recurso> Exemplo: STATUS 1

-> STATS: K <número do recurso> Exemplo: STATS K 1; 
-> STATS: N 			Exemplo: STATS N; 
-> STATS: D 			Exemplo: STATS D

-> PRINT: Exemplo: PRINT

-> EXIT: Exemplo: EXIT

-> SLEEP: <limite de tempo> Exemplo: SLEEP 30

----------------------------------------------------------------------------------------------------
Tendo em conta os testes efetuados, todos os comandos explicitos no enunciado estão a funcionar como pretendido.

----------------------------------------------------------------------------------------------------

--->Melhoramentos de implementação do Projeto1 para o Projeto2:

>No projeto 1, ao usar multiplos clientes (tentamos com 2), ambos conseguiam fazer o bloqueio de leitura do mesmo recurso, o que é de esperar, porém, apenas o último cliente a fazer o bloqueio conseguia desbloquear o recurso. 
 No projeto 2 esta limitação foi resolvida.

>No projeto 1 não validavamos os argumentos passados aos programas.
 No projeto 2 já ocorre esta validação, utilizando o módulo argparse.

>No projeto 1 os recursos estavam numerados de 0 a N-1.
 No projeto 2, como pretendido, os recursos estão numerados de 1 a N

>No projeto 1 chamavamos objeto.__repr__() das classes lock_pool e resource_lock
 No projeto 2 alteramos para chamar o str(objeto)


--->Limitações na implementação:

Segundo os diversos testes que realizamos, não detetamos qualquer anomalia.


--->Implementação de outras funcionalidades que acharam pertinentes

Apenas implementamos o que achamos necessário para a alcançar o objetivo do trabalho.


----------------------------------------------------------------------------------------------------
--->Execução do servidor:

lock_server.py <hostname> <porto TCP> <número de recursos> <número máximo de bloqueios> 

- hostname: onde o servidor fornecerá os recursos;
- porto TCP: onde escutará por pedidos de ligação;
- número de recursos: número de recursos que serão geridos pelo servidor;
- número máximo de bloqueios: número máximo de bloqueios permitidos em cada recurso. 

Exemplo: python3 lock_server.py localhost 9999 4 3


--->Execução do cliente:

lock_client.py <número de cliente> <hostname> <porto TCP> 
 
- número de cliente: o id único do cliente;
- hostname: do servidor que fornece os recursos;
- porto TCP: onde o servidor recebe pedidos de ligação;

Exemplo: python3 lock_client.py 1 localhost 9999

Após iniciar o cliente ele ficará à espera do seguinte comando: 'comando > ', deve inserir um dos 7 comandos disponíveis: LOCK, UNLOCK, STATUS, STATS, PRINT, EXIT ou SLEEP.