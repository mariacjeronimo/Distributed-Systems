README 
Grupo 23 
Números: Maria Jerónimo 56887, Lara Ângelo 56945

----------------------------------------------------------------------------------------------------
COMO EXECUTAR O PROGRAMA:
-> Abrir dois terminais na diretoria do trabalho, um na diretoria server e outro na diretoria client: 
	No primeiro executar o comando--> python3 servidor.py
	No segundo executar o comando--> python3 cliente.py
-> No terminal onde se executou o comando "python3 cliente.py" poderá executar todos os comandos apresentados no enunciado.

----------------------------------------------------------------------------------------------------
COMO TER ACESSO AO TOKEN QUE PERMITE OBTER INFORMAÇÕES VINDAS DA API DO SPOTIFY:
No browser aceder ao seguinte url: https://localhost:5000/login
Após ser redirecionado para o url do profile poderá começar a testar o nosso programa. No entanto este processo terá de ser repetido sempre que o token ficar indisponível (temporário).
----------------------------------------------------------------------------------------------------
Comandos possiveis e URLs dos recursos:

CREATE:
    UTILIZADOR <nome> <senha>                -> 'http://localhost:5000/utilizadores'                
    ARTISTA <id_spotify>                     -> 'http://localhost:5000/artistas'                    
    MUSICA <id_spotify>                      -> 'http://localhost:5000/musicas'                         
    <id_user> <id_musica> <avaliacao>        -> 'http://localhost:5000/utilizadores/playlist'          

READ:       
    UTILIZADOR <id_user>                     -> 'http://localhost:5000/utilizadores/id_user'           
    ARTISTA <id_artista>                     -> 'http://localhost:5000/artistas/id_artista'             
    MUSICA <id_musica>                       -> 'http://localhost:5000/musicas/id_musica'              
    ALL UTILIZADORES                         -> 'http://localhost:5000/utilizadores/all/'               
    ALL ARTISTAS                             -> 'http://localhost:5000/artistas/all/'                   
    ALL MUSICAS                              -> 'http://localhost:5000/musicas/all/'                   
    ALL MUSICAS_A <id_artista>               -> 'http://localhost:5000/musicas/all/artista/id_artista' 
    ALL MUSICAS_U <id_user>                  -> 'http://localhost:5000/musicas/all/utilizador/id_user'  
    ALL MUSICAS <avaliacao>                  -> 'http://localhost:5000/musicas/all/avaliacao'           

DELETE:       
    UTILIZADOR <id_user>                     -> 'http://localhost:5000/utilizadores/id_user'           
    ARTISTA <id_artista>                     -> 'http://localhost:5000/artistas/id_artista'            
    MUSICA <id_musica>                       -> 'http://localhost:5000/musicas/id_musica'             
    ALL UTILIZADORES                         -> 'http://localhost:5000/utilizadores/all/'              
    ALL ARTISTAS                             -> 'http://localhost:5000/artistas/all/'                  
    ALL MUSICAS                              -> 'http://localhost:5000/musicas/all/'                    
    ALL MUSICAS_A <id_artista>               -> 'http://localhost:5000/musicas/all/artista/id_artista'  
    ALL MUSICAS_U <id_user>                  -> 'http://localhost:5000/musicas/all/utilizador/id_user' 
    ALL MUSICAS <avaliacao>                  -> 'http://localhost:5000/musicas/all/avaliacao'        

UPDATE:
    MUSICA <id_musica> <avaliacao> <id_user> -> 'http://localhost:5000/utilizadores/playlist/id_user'  
    UTILIZADOR <id_user> <password>          -> 'http://localhost:5000/utilizadores/id_user'            
----------------------------------------------------------------------------------------------------
INFORMAÇÕES PERTINENTES (os outputs dos comandos READ que mostram informações vindas da API do Spotify):


-> Nos comandos READ MUSICA <id_musica>, READ ARTISTA <id_artista>, respetivamente:
	OUTPUT:
		Sobre a musica:
		 	Informações disponiveis APENAS NA base de dados (id da musica na TABELA MUSICAS)
			Informações disponiveis na API do Spotify 

		Sobre a artista:
		 	Informações disponiveis APENAS NA base de dados (id da musica na TABELA ARTISTAS)
			Informações disponiveis na API do Spotify 

-> Nos comandos READ ALL MUSICAS, READ ALL ARTISTAS:
	OUTPUT:		
		Sobre cada musica:
			Informações disponiveis na base de dados (TABELA MUSICAS)
			Informações disponiveis na API do Spotify

		Sobre cada artista:
			Informações disponiveis na base de dados (TABELA ARTISTAS)
			Informações disponiveis na API do Spotify

			
-> Nos comandos READ ALL MUSICAS_A <id_artista>, READ ALL MUSICAS_U <id_user, READ ALL MUSICAS <avaliacao>:
	OUTPUT:
			Informações disponiveis na base de dados (TABELA MUSICAS, TABELA PLAYLIST (onde na avaliação não mostra o id mas sim a string correspondente))
			Informações disponiveis na API do Spotify