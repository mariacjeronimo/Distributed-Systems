#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 3 - cliente.py
Grupo: 23
Números de aluno: Maria Jerónimo 56887, Lara Ângelo 56945
"""
# Zona para fazer imports
import sys, time, argparse
import requests
import json

# Programa principal

while True:
    mensagem = input('comando > ')
    info = mensagem.split()
    print(info)
    if len(mensagem) == 0:
        print('UNKNOWN COMMAND')
        
    elif info[0] == "EXIT" and len(info) == 1:
        sys.exit(0)

    elif info[0]== "CREATE":
        if info[1] == "UTILIZADOR" and len(info) == 4:
            nome = info[2]
            senha = info[3]
            utilizadores = {'nome': nome, 'senha': senha}
            url = ('http://localhost:5000/utilizadores')
            dados = json.dumps(utilizadores)
            print ("Dados enviados: " + dados)
            resp = requests.put(url, data = dados, headers = {'Content-type': 'application/json'})

            print("-----TESTES CREATE UTILIZADOR------")
            print("STATUS CODE = " + str(resp))
            print("URL =" + str(resp.url))
            print("RESPOSTA: " + str(resp.text))
            

        elif info[1] == "ARTISTA" and len(info) == 3:
            id_spotify = str(info[2])
            artistas = {'id_spotify': id_spotify}
            url = ('http://localhost:5000/artistas')
            dados = json.dumps(artistas)
            print ("Dados enviados: " + dados)
            resp = requests.put(url, data = dados, headers = {'Content-type': 'application/json'})

            print("-----TESTES CREATE ARTISTA------")
            print("STATUS CODE = " + str(resp))
            print("URL =" + str(resp.url))
            print("RESPOSTA: " + str(resp.text))

        
        elif info[1] == "MUSICA" and len(info) == 3:
            id_spotify = str(info[2])
            musicas = {'id_spotify': id_spotify}
            url = ('http://localhost:5000/musicas')
            dados = json.dumps(musicas)
            print ("Dados enviados: " + dados)
            resp = requests.put(url, data = dados, headers = {'Content-type': 'application/json'})


            print("-----TESTES CREATE MUSICA------")
            print("STATUS CODE = " + str(resp))
            print("URL =" + str(resp.url))
            print("RESPOSTA: " + str(resp.text))


        else: # CREATE avaliacoes
            if len(info) == 4:
                id_user = int(info[1])
                id_musica = int(info[2])
                avaliacao = info[3]
                avaliacoes = {'id_user': id_user, 'id_musica': id_musica, 'avaliacao': avaliacao}
                print(avaliacoes)
                url = ('http://localhost:5000/utilizadores/playlist') 
                dados = json.dumps(avaliacoes)
                print ("Dados enviados: " + dados)
                resp = requests.put(url, data = dados, headers = {'Content-type': 'application/json'})

                print("-----TESTES CREATE AVALIACAO------")
                print("STATUS CODE = " + str(resp))
                print("URL =" + str(resp.url))
                print("RESPOSTA: " + str(resp.text))

            else:
                print("UNKOWN COMMAND")


    elif info[0] == "READ":
        if len(info) == 3:
            if info[1] == "UTILIZADOR":
                id_user = int(info[2])
                utilizadores={'id_user' : id_user}
                url = ('http://localhost:5000/utilizadores/' + str(id_user))
                dados = json.dumps(utilizadores)
                print("Dados enviados: " + dados)
                resp = requests.get(url, data = dados, headers = {'Content-type': 'application/json'})


                print("-----TESTES READ UTILIZADOR------")
                print("STATUS CODE = " + str(resp))
                print("URL =" + str(resp.url))
                print("RESPOSTA: " + str(resp.text))


            elif info[1] == "ARTISTA":
                id_artista = int(info[2])
                artistas = {'id_artista' : id_artista}
                url = ('http://localhost:5000/artistas/' + str(id_artista))
                dados = json.dumps(artistas)
                print("Dados enviados: " + dados)
                resp = requests.get(url, data = dados, headers = {'Content-type': 'application/json'})


                print("-----TESTES READ ARTISTA------")
                print("STATUS CODE = " + str(resp))
                print("URL =" + str(resp.url))
                print("RESPOSTA: " + str(resp.text))


            elif info[1] == "MUSICA":
                try:
                    id_musica = int(info[2])
                    musicas = {'id_musica' : id_musica}
                    url = ('http://localhost:5000/musicas/' + str(id_musica))
                    dados = json.dumps(musicas)
                    print("Dados enviados: " + dados)
                    resp = requests.get(url, data = dados, headers = {'Content-type': 'application/json'})


                    print("-----TESTES READ MUSICA ------")
                    print("STATUS CODE = " + str(resp))
                    print("URL =" + str(resp.url))
                    print("RESPOSTA: " + str(resp.text))
                except ValueError:
                    print("O id da musica tem de ser um inteiro")
                

        
            elif info[1] == "ALL":
                if info[2] == "UTILIZADORES": 
                    url = ('http://localhost:5000/utilizadores/all')
                    resp = requests.get(url, headers = {'Content-type': 'application/json'})

                    print("-----TESTES READ ALL UTILIZADORES ------")
                    print("STATUS CODE = " + str(resp))
                    print("URL =" + str(resp.url))
                    print("RESPOSTA: " + str(resp.text))

                
                elif info[2] == "ARTISTAS":
                    url = ('http://localhost:5000/artistas/all')
                    resp = requests.get(url, headers = {'Content-type': 'application/json'})


                    print("-----TESTES READ ALL ARTISTAS ------")
                    print("STATUS CODE = " + str(resp))
                    print("URL =" + str(resp.url))
                    print("RESPOSTA: " + str(resp.text))


                
                elif info[2] == "MUSICAS":
                    url = ('http://localhost:5000/musicas/all')
                    resp = requests.get(url, headers = {'Content-type': 'application/json'})

                    print("-----TESTES READ ALL MUSICAS ------")
                    print("STATUS CODE = " + str(resp))
                    print("URL =" + str(resp.url))
                    print("RESPOSTA: " + str(resp.text))
                else:
                    print("UNKOWN COMMAND")
            else:
                print("UNKOWN COMMAND")


        
        elif len(info) == 4:
            
            if info[1] == "ALL":
                if info[2] == "MUSICAS_A":
                    id_artista = int(info[3])
                    musicas = {'id_artista' : id_artista}
                    url = ('http://localhost:5000/musicas/all/artista/' + str(id_artista) ) 
                    dados = json.dumps(musicas)
                    print("Dados enviados: " + dados)
                    resp = requests.get(url, data = dados, headers = {'Content-type': 'application/json'})


                    print("-----TESTES READ ALL MUSICAS_A <id_artista> ------")
                    print("STATUS CODE = " + str(resp))
                    print("URL =" + str(resp.url))
                    print("RESPOSTA: " + str(resp.text))



                elif info[2] == "MUSICAS_U":
                    id_user = int(info[3])
                    musicas = {'id_user' : id_user}
                    url = ('http://localhost:5000/musicas/all/utilizador/'+ str(id_user))
                    dados = json.dumps(musicas)
                    print("Dados enviados: " + dados)
                    resp = requests.get(url, data = dados, headers = {'Content-type': 'application/json'})


                    print("-----TESTES READ ALL MUSICAS_U <id_user> ------")
                    print("STATUS CODE = " + str(resp))
                    print("URL =" + str(resp.url))
                    print("RESPOSTA: " + str(resp.text))



                elif info[2] == "MUSICAS":
                    avaliacao = str(info[3]) 
                    musicas = {'avaliacao' : avaliacao}
                    url = ('http://localhost:5000/musicas/all/avaliacao')
                    dados = json.dumps(musicas)
                    print("Dados enviados: " + dados)
                    resp = requests.get(url, data = dados, headers = {'Content-type': 'application/json'})

                    print("-----TESTES READ ALL MUSICAS <avaliacao> ------")
                    print("STATUS CODE = " + str(resp))
                    print("URL =" + str(resp.url))
                    print("RESPOSTA: " + str(resp.text))

                else:
                    print("UNKOWN COMMAND")
            else:
                print("UNKOWN COMMAND")
        else:
            print("UNKNOWN COMMAND")

            


    elif info[0] == "DELETE":
        if len(info) == 3:
            if info[1] == "UTILIZADOR":
                id_user = int(info[2])
                utilizadores={'id_user' : id_user}
                url = ('http://localhost:5000/utilizadores/' + str(id_user))
                dados = json.dumps(utilizadores)
                print("Dados enviados: " + dados)
                resp = requests.delete(url, data = dados, headers = {'Content-type': 'application/json'})


                print("-----TESTES DELETE UTILIZADOR------")
                print("STATUS CODE = " + str(resp))
                print("URL =" + str(resp.url))
                print("RESPOSTA: " + str(resp.text))


            elif info[1] == "ARTISTA":
                id_artista = int(info[2])
                artistas = {'id_artista' : id_artista}
                url = ('http://localhost:5000/artistas/' + str(id_artista))
                dados = json.dumps(artistas)
                print("Dados enviados: " + dados)
                resp = requests.delete(url, data = dados, headers = {'Content-type': 'application/json'})


                print("-----TESTES DELETE ARTISTA------")
                print("STATUS CODE = " + str(resp))
                print("URL =" + str(resp.url))
                print("RESPOSTA: " + str(resp.text))


            elif info[1] == "MUSICA":
                id_musica = int(info[2])
                musicas = {'id_musica' : id_musica}
                url = ('http://localhost:5000/musicas/' + str(id_musica))
                dados = json.dumps(musicas)
                print("Dados enviados: " + dados)
                resp = requests.delete(url, data = dados, headers = {'Content-type': 'application/json'})

                
                print("-----TESTES DELETE MUSICA------")
                print("STATUS CODE = " + str(resp))
                print("URL =" + str(resp.url))
                print("RESPOSTA: " + str(resp.text))


            
            elif info[1] == "ALL":
                if info[2] == "UTILIZADORES":
                    url = ('http://localhost:5000/utilizadores/all/')
                    resp = requests.delete(url, headers = {'Content-type': 'application/json'})

                    print("-----TESTES DELETE ALL UTILIZADORES------")
                    print("STATUS CODE = " + str(resp))
                    print("URL =" + str(resp.url))
                    print("RESPOSTA: " + str(resp.text))


                elif info[2] == "ARTISTAS":
                    url = ('http://localhost:5000/artistas/all/')
                    resp = requests.delete(url,  headers = {'Content-type': 'application/json'})

                    print("-----TESTES DELETE ALL ARTISTAS------")
                    print("STATUS CODE = " + str(resp))
                    print("URL =" + str(resp.url))
                    print("RESPOSTA: " + str(resp.text))

                elif info[2] == "MUSICAS":
                    url = ('http://localhost:5000/musicas/all/')
                    resp = requests.delete(url,  headers = {'Content-type': 'application/json'})

                    print("-----TESTES DELETE ALL MUSICAS------")
                    print("STATUS CODE = " + str(resp))
                    print("URL =" + str(resp.url))
                    print("RESPOSTA: " + str(resp.text))
                    


        elif len(info) == 4:
            
            if info[1] == "ALL":
                if info[2] == "MUSICAS_A":
                    id_artista = int(info[3])
                    musicas = {'id_artista' : id_artista}
                    url = ('http://localhost:5000/musicas/all/artista/' + str(id_artista) ) 
                    dados = json.dumps(musicas)
                    print("Dados enviados: " + dados)
                    resp = requests.delete(url, data = dados, headers = {'Content-type': 'application/json'})



                    print("-----TESTES DELETE ALL MUSICAS_A <id_artista>------")
                    print("STATUS CODE = " + str(resp))
                    print("URL =" + str(resp.url))
                    print("RESPOSTA: " + str(resp.text))


                elif info[2] == "MUSICAS_U":
                    id_user = int(info[3])
                    musicas = {'id_user' : id_user}
                    url = ('http://localhost:5000/musicas/all/utilizador/'+ str(id_user))
                    dados = json.dumps(musicas)
                    print("Dados enviados: " + dados)
                    resp = requests.delete(url, data = dados, headers = {'Content-type': 'application/json'})

                    print("-----TESTES DELETE ALL MUSICAS_U <id_user>------")
                    print("STATUS CODE = " + str(resp))
                    print("URL =" + str(resp.url))
                    print("RESPOSTA: " + str(resp.text))


                elif info[2] == "MUSICAS":
                    avaliacao = str(info[3]) 
                    musicas = {'avaliacao' : avaliacao}
                    url = ('http://localhost:5000/musicas/all/avaliacao')
                    dados = json.dumps(musicas)
                    print("Dados enviados: " + dados)
                    resp = requests.delete(url, data = dados, headers = {'Content-type': 'application/json'})

                    print("-----TESTES DELETE ALL MUSICAS <avaliacao>------")
                    print("STATUS CODE = " + str(resp))
                    print("URL =" + str(resp.url))
                    print("RESPOSTA: " + str(resp.text))

                else:
                    print("UNKOWN COMMAND")
            else:
                print("UNKOWN COMMAND")
        else:
            print("UNKNOWN COMMAND")

    elif info[0] == "UPDATE":
        if info[1] == "MUSICA" and len(info) == 5:
            id_musica = int(info[2])
            avaliacao = info[3]
            id_user = int(info[4])
            avaliacao = {'id_musica' : id_musica, 'avaliacao' : avaliacao, 'id_user' : id_user}
            url = ('http://localhost:5000/utilizadores/playlist/'+ str(id_user))

            dados = json.dumps(avaliacao)
            print ("Dados enviados: " + dados)
            resp = requests.put(url, data = dados, headers = {'Content-type': 'application/json'})

            print("-----TESTES UPDATE MUSICA <id_musica> <avaliacao> <id_user>------")
            print("STATUS CODE = " + str(resp))
            print("URL =" + str(resp.url))
            print("RESPOSTA: " + str(resp.text))

        
        elif info[1] == "UTILIZADOR" and len(info) == 4: 
            id_user = info[2]
            password = info[3]
            utilizadores = {'id_user': id_user, 'password': password}
            url = ('http://localhost:5000/utilizadores/'+ str(id_user))
            dados = json.dumps(utilizadores)
            print ("Dados enviados: " + dados)
            resp = requests.put(url, data = dados, headers = {'Content-type': 'application/json'})

            print("-----TESTES UPDATE UTILIZADOR ------")
            print("STATUS CODE = " + str(resp))
            print("URL =" + str(resp.url))
            print("RESPOSTA: " + str(resp.text))        
        else:
            print("UNKNOWN COMMAND")
    else:
        print("UNKOWN COMMAND")
                