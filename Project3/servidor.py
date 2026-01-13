#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 3 - servidor.py
Grupo: 23
Números de aluno: Maria Jerónimo 56887, Lara Ângelo 56945
"""
# Zona para fazer imports

import spotify_requests
import sys, time, argparse
from flask import Flask, request, make_response, g 
import sqlite3, json
from os.path import isfile

# Programa principal
app = Flask(__name__)
@app.before_request
def before_request():
	g.db = connect_db('tabelas.db')

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_tabelas', None)
	if db is not None:
		db[0].close()

def connect_db(dbname):
	db_is_created = isfile(dbname)
	connection = sqlite3.connect('tabelas.db')
	cursor = connection.cursor()
	if not db_is_created:
		with app.open_resource('tabelas.sql', mode='r') as f:
			connection.cursor().executescript(f.read())
		connection.commit()
	else:
		connection.cursor().execute('PRAGMA foreign_keys = ON')
		connection.commit()
	return connection, cursor

#-------------GERAR TOKEN---------------
token = spotify_requests.generateNewOAuthToken()

#---------------------------VERIIFICAR OS METHODS------------------------------------
@app.route('/utilizadores', methods = ['PUT', 'GET', 'DELETE']) #CERTO
@app.route('/utilizadores/<int:id>', methods = ['PUT',"GET", 'DELETE']) #CERTO
@app.route('/utilizadores/all/', methods = ["GET", 'DELETE']) #CERTO
@app.route('/utilizadores/playlist', methods = ['PUT']) #CERTO
@app.route('/utilizadores/playlist/<int:id>', methods = ['PUT']) #CERTO


def utilizadores(id = None): 
	if request.method == "GET":
		if request.url == 'http://localhost:5000/utilizadores/' + str(id): #READ UTILIZADOR <id_user> 
			try:
				cur = g.db[1].execute("SELECT * FROM utilizadores WHERE id=?", (int(id),))
				linha = cur.fetchall()
				if linha is not None and len(linha) != 0:
					id_utilizador = linha[0][0]
					nome_utilizador = linha[0][1]
					senha_utilizador = linha[0][2]
					lista_resp = ["Informacoes relativas ao utilizador:"]
					lista_resp.append({'ID': id_utilizador, 'Nome': str(nome_utilizador), 'Senha': str(senha_utilizador)})
					resposta = json.dumps(lista_resp,indent=4)
					status = 200
				else:
					resposta = json.dumps({'describedBy' : 'http://localhost:5000/utilizadores/'+str(id),'httpStatus': 404, 'title' : 'Utilizador nao encontrado'},indent=4) 
					status = 404
			except sqlite3.OperationalError:
				resposta = json.dumps({'describedBy' : 'http://localhost:5000/utilizadores/'+str(id),'httpStatus': 500, 'title' : 'Ocorreu um erro na execucao da query'},indent=4)
				status = 500
			r = make_response((resposta, status, {'Content-Type': 'application/json'}))
			return r

		if request.url == 'http://localhost:5000/utilizadores/all/':#READ ALL UTILIZADORES 
			try:
				cur = g.db[1].execute("SELECT * FROM utilizadores")
				linha = cur.fetchall()
				lista_utilizadores = ["Todos os utilizadores presentes na base de dados:"]
				if linha is not None and len(linha) != 0:
					for info in linha:
						id_utilizador = info[0]
						nome_utilizador = info[1]
						senha_utilizador = info[2]
						lista_utilizadores.append({'ID':str(id_utilizador),'Nome': str(nome_utilizador),'Senha': str(senha_utilizador)})
					resposta = json.dumps(lista_utilizadores, indent=4)
					status = 200
				else:
					resposta = json.dumps({'describedBy' : 'http://localhost:5000/utilizadores/all/','httpStatus': 404, 'title': 'Nao existem utilizadores atualmente!'},indent=4)
					status = 404
			except sqlite3.OperationalError:
				resposta = json.dumps({'describedBy' : 'http://localhost:5000/utilizadores/all/','httpStatus': 500, 'title' : 'Ocorreu um erro na execucao da query'},indent=4)
				status = 500
			r = make_response((resposta, status, {'Content-Type': 'application/json'}))
			return r
	if request.method == "PUT":
		if request.url == 'http://localhost:5000/utilizadores': #CREATE UTILIZADOR <nome> <senha> 
			dados = json.loads(request.data)
			informacao = (dados['nome'], dados['senha'],)
			try:
				g.db[1].execute('INSERT INTO utilizadores VALUES(NULL,?,?)', informacao) 
				g.db[0].commit()
			except sqlite3.OperationalError:
				resposta = json.dumps({'describedBy' : 'http://localhost:5000/utilizadores','httpStatus': 500, 'title' : 'Ocorreu um erro na execucao da query'},indent=4)
				status = 500
			else:
				cur_id = g.db[1].execute('SELECT id FROM utilizadores WHERE nome=?', (str(dados['nome']),)) 
				id_user = cur_id.fetchone()[0]
				resposta = json.dumps({'status': 'Utilizador ' + str(dados['nome']) +' adicionado com sucesso'},indent=4)
				status = 201
			r = make_response((resposta, status, {'Content-Type': 'application/json'}))

			return r 

		if request.url == 'http://localhost:5000/utilizadores/'+ str(id): #UPDATE UTILIZADOR <id_user> <password>
			dados = json.loads(request.data)
			informacao = (dados['password'], dados['id_user'],)
			try:
				g.db[1].execute('UPDATE utilizadores SET senha = ? WHERE id = ?', informacao) 
				g.db[0].commit()
			except sqlite3.OperationalError:
				resposta = json.dumps({'describedBy' : 'http://localhost:5000/utilizadores/'+str(id),'httpStatus': 500, 'title' : 'Ocorreu um erro na execucao da query'},indent=4)
				status = 500
			else:
				resposta = json.dumps({'status': 'A senha do utilizador com id ' + str(dados['id_user']) +' foi alterada com sucesso!'},indent=4)
				status = 200

			r = make_response((resposta, status, {'Content-Type': 'application/json'}))
			return r
			
		if request.url == 'http://localhost:5000/utilizadores/playlist': #<id_user><id_musica><avaliacao> 
			dados = json.loads(request.data)
			cur_id_avaliacao = g.db[1].execute('SELECT id FROM avaliacoes WHERE sigla = ?', (str(dados['avaliacao']),))
			id_avaliacao = cur_id_avaliacao.fetchone()[0]
			informacao = (dados['id_user'],dados["id_musica"],int(id_avaliacao),)
			try:
				g.db[1].execute('INSERT INTO playlists VALUES (?, ?, ?)', informacao) 
				g.db[0].commit()
			except sqlite3.IntegrityError:
				resposta = json.dumps({'describedBy' : 'http://localhost:5000/utilizadores/playlist','httpStatus': 500, 'title' : 'Ocorreu um erro na execucao da query'},indent=4)
				status = 500
			except sqlite3.OperationalError:
				resposta = json.dumps({'describedBy' : 'http://localhost:5000/utilizadores/playlist','httpStatus': 500, 'title' : 'Ocorreu um erro na execucao da query'},indent=4)
				status = 500
			else:
				resposta = json.dumps({'status': "O utilizador com id= " + str(dados['id_user']) + " avaliou a musica com id= " + str(dados['id_musica'])+ " com a avaliacao de sigla= " + str(dados['avaliacao'])},indent=4)
				status = 200
			r = make_response((resposta, status, {'Content-Type': 'application/json'}))
			return r

		if request.url == 'http://localhost:5000/utilizadores/playlist/' + str(id): # UPDATE MUSICA <id_musica> <avaliacao> <id_user> 
			dados = json.loads(request.data)
			informacao = (dados['avaliacao'], dados['id_user'] ,dados['id_musica'],)
			try:
				g.db[1].execute('UPDATE playlists SET id_avaliacao = (SELECT id FROM avaliacoes WHERE sigla = ?) WHERE id_user = ? AND id_musica = ?', informacao) 
				g.db[0].commit()
			except sqlite3.OperationalError:
				resposta = json.dumps({'describedBy' : 'http://localhost:5000/utilizadores/playlist','httpStatus': 500, 'title' : 'Ocorreu um erro na execucao da query'},indent=4)
				status = 500
			else:
				resposta = json.dumps({'status': "O utilizador com id= "+ str(dados['id_user']) + " alterou a avaliacao da musica com id=" + str(dados['id_musica']) + " para sigla= "+ str(dados['avaliacao']) },indent=4)
				status = 200
			r = make_response((resposta, status, {'Content-Type': 'application/json'}))
			return r


			

	if request.method == "DELETE":
		if request.url == 'http://localhost:5000/utilizadores/' + str(id): #DELETE UTILIZADOR <id_user> 
			try:
				g.db[1].execute("DELETE FROM utilizadores WHERE id=?", (int(id),))
				g.db[0].commit()
			except sqlite3.OperationalError:
				resposta = json.dumps({'describedBy' : 'http://localhost:5000/','httpStatus': 500, 'title' : 'Ocorreu um erro na execucao da query'},indent=4)
				status = 500
			else:
				resposta = json.dumps({'status': 'Utilizador removido com sucesso'},indent=4)
				status = 200
			r = make_response(resposta, status, {'Content-Type': 'application/json'})
			return r
		if request.url == 'http://localhost:5000/utilizadores/all/':#DELETE ALL UTILIZADORES 
			try:
				g.db[1].execute("DELETE FROM utilizadores")
				g.db[0].commit()
			except sqlite3.OperationalError:
				resposta = json.dumps({'describedBy' : 'http://localhost:5000/','httpStatus': 500, 'title' : 'Ocorreu um erro na execucao da query'},indent=4)
				status = 500
			else:
				resposta = json.dumps({'status': 'Todos os utilizadores foram removidos'},indent=4)
				status = 200

			r = make_response((resposta, status, {'Content-Type': 'application/json'}))
			return r
	

			

#------------------------------------------------------------------------------------
@app.route('/musicas', methods = ['PUT', 'GET', 'DELETE'])
@app.route('/musicas/<int:id>', methods = ['GET', 'DELETE'])
@app.route('/musicas/all/artista/<int:id>', methods = ['GET', 'DELETE'])
@app.route('/musicas/all/utilizador/<int:id>', methods = ['GET', 'DELETE'])
@app.route('/musicas/all/avaliacao', methods = ['GET', 'DELETE'])
@app.route('/musicas/all/', methods = ['GET', 'DELETE'])
@app.route('/musicas/playlists', methods = ['PUT', 'GET', 'DELETE'])


def musicas(id = None):
	if request.method == "GET": 
		if request.url == 'http://localhost:5000/musicas/' + str(id): #READ MUSICA <id_musica> ------ usa SPOTIFY API
			dados=json.loads(request.data)
			informacao = (int(dados['id_musica']),)
			try:
				
				cur_id_spotify = g.db[1].execute('SELECT id_spotify FROM musicas WHERE id = ?', informacao) 
				
				cur_id_spotify_fetch=cur_id_spotify.fetchone()
				if cur_id_spotify_fetch is None:
					resposta = json.dumps({'status': 'Musica inexistente na base de dados'},indent=4)
					status = 404
				else:
					id_spotify = cur_id_spotify_fetch[0]
					json_spotify = spotify_requests.requestMusica(token,str(id_spotify))
					lista_resp = ["Id da musica na base de dados: " + str(dados['id_musica']),"Informacao vinda da spotify API: "]
					if json_spotify is not None:
						lista_resp.append(json_spotify)
						resposta = json.dumps(lista_resp,indent=4)
						status = 200
			except sqlite3.OperationalError:
				resposta = json.dumps({'describedBy' : 'http://localhost:5000/musicas/'+str(id),'httpStatus': 500, 'title' : 'Ocorreu um erro na execucao da query'},indent=4)
				status = 500
			r = make_response((resposta, status, {'Content-Type': 'application/json'}))
			return r

		if request.url == 'http://localhost:5000/musicas/all/': #READ ALL MUSICAS
			try:
				cur = g.db[1].execute("SELECT * FROM musicas")
			except sqlite3.OperationalError:
				resposta = json.dumps({'describedBy' : 'http://localhost:5000/musicas/all/','httpStatus': 500, 'title' : 'Ocorreu um erro na execucao da query'},indent=4)
				status = 500
			else:
				linha = cur.fetchall() 
				if linha is not None and len(linha) != 0:
					lista_musicas=["Informacoes relativas a todas as musicas existentes na bases de dados:"]
					lista_musicas.append("#")
					lista_musicas.append("#")
					lista_musicas.append("#")
					for info in linha:
						id_musica = info[0]
						id_spotify = info[1]
						nome = info[2]
						id_artista= info[3]
						resposta_musica  = spotify_requests.requestMusica(token, str(id_spotify))
						lista_musicas.append("-----------MUSICA: " + str(nome) + ": -----------")
						lista_musicas.append("-----------INFORMACOES ENCONTRADAS NA BASE DE DADOS:-----------")
						lista_musicas.append({'ID':str(id_musica),'ID do Spotify': str(id_spotify),'Nome': str(nome), 'ID do artista': str(id_artista)})
						lista_musicas.append("-----------INFORMACOES ENCONTRADAS NA API DO SPOTIFY:-----------")
						lista_musicas.append(resposta_musica)
						lista_musicas.append("-----------------------------------------------------------------------")

					resposta = json.dumps(lista_musicas,indent=4)
					status = 200
				else:
					resposta = json.dumps({'describedBy' : 'http://localhost:5000/musicas/all/','httpStatus': 404, 'title' :'Nao existem musicas atualmente!'},indent=4)
					status = 404
			r = make_response((resposta, status, {'Content-Type': 'application/json'}))
			return r

		if request.url == 'http://localhost:5000/musicas/all/artista/' + str(id): #READ ALL MUSICAS_A <id_artista> 
			dados=json.loads(request.data)
			informacao = (int(dados['id_artista']),)
			try:
				cur = g.db[1].execute("SELECT * FROM musicas WHERE id IN(SELECT id_musica FROM playlists WHERE id_musica IN (SELECT id FROM musicas WHERE id_artista = ?))", informacao)
				linha = cur.fetchall()
				cur_playlist = g.db[1].execute('SELECT * FROM playlists WHERE id_musica IN (SELECT id FROM musicas WHERE id_artista = ?)',informacao) 
				linha_playlist = cur_playlist.fetchall()
			except sqlite3.OperationalError:
				resposta = json.dumps({'describedBy' : 'http://localhost:5000/musicas/all/artista/'+str(id),'httpStatus': 500, 'title' : 'Ocorreu um erro na execucao da query'},indent=4)
				status = 500
			else:
				
				
				
				if linha is not None and len(linha) != 0:
					corresp_avaliacao={1:'M', 2:'m', 3:'S',4:'B', 5:'MB'}
					lista_musicas=["Informacoes relativas a todas as musicas AVALIADAS do artista de id "+str(dados['id_artista'])+" existentes na bases de dados:"]
					lista_musicas.append("#")
					lista_musicas.append("#")
					lista_musicas.append("#")
					for info in linha:
						id_musica = info[0]
						id_spotify = info[1]
						nome = info[2]
						id_artista = info[3]
						resposta_musica  = spotify_requests.requestMusica(token, str(id_spotify))
						lista_musicas.append("-----------MUSICA: " + str(nome) + ": -----------")
						lista_musicas.append("-----------INFORMACOES ENCONTRADAS NA BASE DE DADOS:-----------")
						lista_musicas.append("TABELA MUSICAS")
						lista_musicas.append({'ID':str(id_musica),'ID do Spotify': str(id_spotify),'Nome': str(nome), 'ID do artista': str(id_artista)})
						lista_musicas.append("TABELA PLAYLIST")
						for info2 in linha_playlist:
							
							if info2[1] == id_musica:
								id_aval=int(info2[2])
								lista_musicas.append({'ID_UTILIZADOR': str(info2[0]), 'ID_MUSICA': str(info2[1]), 'AVALIACAO': str(corresp_avaliacao.get(id_aval))})
	
						lista_musicas.append("-----------INFORMACOES ENCONTRADAS NA API DO SPOTIFY:-----------")
						lista_musicas.append(resposta_musica)
						lista_musicas.append("-----------------------------------------------------------------------")		
					resposta = json.dumps(lista_musicas,indent=4)
					status = 200
				else:
					resposta = json.dumps({'describedBy' : 'http://localhost:5000/musicas/all/artista/'+str(id),'httpStatus': 404, 'title' :'Nao existem musicas avaliadas do artista de id= '+ str(id)},indent=4)
					status = 404
			r = make_response((resposta, status, {'Content-Type': 'application/json'}))
			return r

		if request.url == 'http://localhost:5000/musicas/all/utilizador/' + str(id): #READ ALL MUSICAS_U <id_user> 
			dados=json.loads(request.data)
			informacao = (int(dados['id_user']),)
			try:
				cur = g.db[1].execute("SELECT * FROM musicas WHERE id IN(SELECT id_musica FROM playlists WHERE id_user = ?)", informacao)
				linha = cur.fetchall()
				cur_playlist = g.db[1].execute("SELECT * FROM playlists WHERE id_user = ?", informacao)
				linha_playlist = cur.fetchall()
			except sqlite3.OperationalError:
				resposta = json.dumps({'describedBy' : 'http://localhost:5000/musicas/all/utilizador/'+str(id),'httpStatus': 500, 'title' : 'Ocorreu um erro na execucao da query'},indent=4)
				status = 500
			else:
				if linha is not None and len(linha) != 0:
					corresp_avaliacao={1:'M', 2:'m', 3:'S',4:'B', 5:'MB'}
					lista_musicas=["Informacoes relativas a todas as musicas AVALIADAS pelo utilizador de id "+str(dados['id_user'])+" existentes na bases de dados:"]
					lista_musicas.append("#")
					lista_musicas.append("#")
					lista_musicas.append("#")
					for info in linha:
						id_musica = info[0]
						id_spotify = info[1]
						nome = info[2]
						id_artista = info[3]
						resposta_musica  = spotify_requests.requestMusica(token, str(id_spotify))
						lista_musicas.append("-----------MUSICA: " + str(nome) + ": -----------")
						lista_musicas.append("-----------INFORMACOES ENCONTRADAS NA BASE DE DADOS:-----------")
						lista_musicas.append("TABELA MUSICAS")
						lista_musicas.append({'ID':str(id_musica),'ID do Spotify': str(id_spotify),'Nome': str(nome), 'ID do artista': str(id_artista)})
						lista_musicas.append("TABELA PLAYLIST")
						for info2 in linha_playlist:
							if info2[1] == id_musica:
								id_aval=int(info2[2])
								lista_musicas.append({'ID_UTILIZADOR': str(info2[0]), 'ID_MUSICA': str(info2[1]), 'AVALIACAO':  str(corresp_avaliacao.get(id_aval))})
						
						lista_musicas.append("-----------INFORMACOES ENCONTRADAS NA API DO SPOTIFY:-----------")
						lista_musicas.append(resposta_musica)
						lista_musicas.append("-----------------------------------------------------------------------")		
					resposta = json.dumps(lista_musicas,indent=4)
					status = 200
						
				else:
					resposta = json.dumps({'describedBy' : 'http://localhost:5000/musicas/all/utilizador/'+str(id),'httpStatus': 404, 'title' :'Nao existem musicas avaliadas do utilizador de id= '+ str(id)},indent=4)
					status = 404

			r = make_response((resposta, status, {'Content-Type': 'application/json'}))
			return r

		if request.url == 'http://localhost:5000/musicas/all/avaliacao': #READ ALL MUSICAS <avaliacao> 
			dados = json.loads(request.data)
			informacao = (dados['avaliacao'],)
			try:
				cur = g.db[1].execute('SELECT * FROM musicas WHERE id IN(SELECT id_musica FROM playlists WHERE id_avaliacao IN (SELECT id FROM avaliacoes WHERE sigla = ?))', informacao)
				linha = cur.fetchall()
				cur_playlist = g.db[1].execute('SELECT * FROM playlists WHERE id_avaliacao IN (SELECT id FROM avaliacoes WHERE sigla = ?)', informacao)
				linha_playlist = cur_playlist.fetchall()

			except sqlite3.OperationalError:
				resposta = json.dumps({'describedBy' : 'http://localhost:5000/musicas/all/avaliacao','httpStatus': 500, 'title' : 'Ocorreu um erro na execucao da query'},indent=4)
				status = 500
			else:
				if linha is not None and len(linha) != 0:
					corresp_avaliacao={1:'M', 2:'m', 3:'S',4:'B', 5:'MB'}
					lista_musicas=["Informacoes relativas a todas as musicas de avaliacao =  "+str(dados['avaliacao'])+" existentes na bases de dados:"]
					lista_musicas.append("#")
					lista_musicas.append("#")
					lista_musicas.append("#")
					for info in linha:
						id_musica = info[0]
						id_spotify = info[1]
						nome = info[2]
						id_artista = info[3]
						resposta_musica  = spotify_requests.requestMusica(token, str(id_spotify))
						lista_musicas.append("-----------MUSICA: " + str(nome) + ": -----------")
						lista_musicas.append("-----------INFORMACOES ENCONTRADAS NA BASE DE DADOS:-----------")
						lista_musicas.append("TABELA MUSICAS")
						lista_musicas.append({'ID':str(id_musica),'ID do Spotify': str(id_spotify),'Nome': str(nome), 'ID do artista': str(id_artista)})
						lista_musicas.append("TABELA PLAYLIST")
						for info2 in linha_playlist:
							if info2[1] == id_musica:
								id_aval=int(info2[2])
								lista_musicas.append({'ID_UTILIZADOR': str(info2[0]), 'ID_MUSICA': str(info2[1]), 'AVALIACAO':  str(corresp_avaliacao.get(id_aval))})
						lista_musicas.append("-----------INFORMACOES ENCONTRADAS NA API DO SPOTIFY:-----------")
						lista_musicas.append(resposta_musica)
						lista_musicas.append("-----------------------------------------------------------------------")		
					resposta = json.dumps(lista_musicas,indent=4)
					status = 200	
				else:
					resposta = json.dumps({'describedBy' : 'http://localhost:5000/musicas/all/avaliacao','httpStatus': 404, 'title' : 'Nao existem musicas com a avaliacao ='+ str(dados['avaliacao'])},indent=4)
					status = 404
			r = make_response((resposta, status, {'Content-Type': 'application/json'}))
			return r
		

	if request.method == "PUT":
		if request.url == 'http://localhost:5000/musicas': #CREATE MUSICA <id_spotify>  
			dados = json.loads(request.data)
			resposta_musica  = spotify_requests.requestMusica(token, str(dados['id_spotify']))
			if resposta_musica is None:
				resposta = json.dumps({'describedBy' : 'http://localhost:5000/musicas','httpStatus': 404, 'title' : 'O id do spotify eh invalido'},indent=4)
				status = 404
				r = make_response((resposta, status, {'Content-Type': 'application/json'}))
				return r

			nome_musica =spotify_requests.getNomeFromMusica(resposta_musica)
			id_artista = spotify_requests.getIdArtistaFromMusica(resposta_musica)
			informacao = (dados['id_spotify'],nome_musica, id_artista,)
			
			
			var = g.db[1].execute('SELECT id FROM artistas WHERE id_spotify = ?', (str(id_artista),))
			id_artista_bd=var.fetchone()

			cur_existe_musica = g.db[1].execute('SELECT id FROM musicas WHERE id_spotify = ?', (str(dados['id_spotify']),))
			existe_musica = cur_existe_musica.fetchone()
			
			if existe_musica is None:
				if id_artista_bd is None:
					resposta_artista = spotify_requests.requestArtista(token, id_artista)
					nome_artista = spotify_requests.getNomeFromArtista(resposta_artista)
					informacao2 = (id_artista, nome_artista,)
					g.db[1].execute('INSERT INTO artistas VALUES(NULL,?,?)', informacao2)
					g.db[0].commit()
					var2= g.db[1].execute('SELECT id FROM artistas WHERE id_spotify = ?', (str(id_artista),))
					id_artista_bd = var2.fetchone()

			
				informacao3 = (dados['id_spotify'],nome_musica, id_artista_bd[0],)
				g.db[1].execute('INSERT INTO musicas VALUES(NULL,?,?,?)', informacao3) 
				g.db[0].commit()
				resposta = json.dumps({'status': "Nova musica com nome= " + str(nome_musica) +  " e id= " + str(dados['id_spotify']) + " inserida na base de dados"},indent=4)
				status = 200
			else:
				resposta = json.dumps({'describedBy' : 'http://localhost:5000/musicas','httpStatus': 409, 'title' : "Ja existe uma musica com nome= " + str(nome_musica) +  " e id= " + str(dados['id_spotify']) + " inserida na base de dados"},indent=4)
				status = 409

			r = make_response((resposta, status, {'Content-Type': 'application/json'}))
			return r


		
	if request.method == "DELETE":
		if request.url == 'http://localhost:5000/musicas/' + str(id): #DELETE MUSICA <id_musica> 
			try:
				cur = g.db[1].execute("SELECT * FROM musicas WHERE id=?", (int(id),))
				cur_existe = cur.fetchone()

				g.db[1].execute("DELETE FROM musicas WHERE id=?", (int(id),))
				g.db[0].commit()

				cur = g.db[1].execute("DELETE FROM musicas WHERE id=?", (int(id),))
			except sqlite3.OperationalError:
				resposta = json.dumps({'describedBy' : 'http://localhost:5000/musicas/'+ str(id),'httpStatus': 500, 'title' : "Ocorreu um erro na execucao da query"},indent=4)
				status = 500
			if cur_existe is not None:
				resposta = json.dumps({'status':"Musica ID= " + str(id)+" eliminada"},indent=4)
				status = 200
			else:
				resposta = json.dumps({'describedBy' : 'http://localhost:5000/musicas','httpStatus': 404, 'title' : 'Nao existe nenhuma musica de ID= ' + str(id)+' na base de dados'},indent=4)
				status = 404
			r = make_response((resposta, status, {'Content-Type': 'application/json'}))
			return r
			
		if request.url == 'http://localhost:5000/musicas/all/':#DELETE ALL MUSICAS 
			try:
				g.db[1].execute("DELETE FROM musicas")
				g.db[0].commit()
			except sqlite3.OperationalError:
				resposta = json.dumps({'describedBy' : 'http://localhost:5000/musicas/all/','httpStatus': 500, 'title' : "Ocorreu um erro na execucao da query"},indent=4)
				status = 500
			else:
				resposta = json.dumps({'status':"Todas as musicas foram removidas"},indent=4)
				status = 200
			r = make_response((resposta, status, {'Content-Type': 'application/json'}))
			return r

		if request.url == 'http://localhost:5000/musicas/all/artista/' + str(id): #DELETE ALL MUSICAS_A <id_artista> 
			dados=json.loads(request.data)
			informacao = (int(dados['id_artista']),)
			try:
				g.db[1].execute("DELETE FROM musicas WHERE id IN (SELECT id_musica FROM playlists WHERE id_musica IN (SELECT id FROM musicas WHERE id_artista = ?))", informacao)
				g.db[0].commit()
			except sqlite3.OperationalError:
				resposta = json.dumps({'describedBy' : 'http://localhost:5000/musicas/all/artista/' + str(id),'httpStatus': 500, 'title' : "Ocorreu um erro na execucao da query"},indent=4)
				status = 500
			else:
				resposta = json.dumps({'status':'Todas as musicas avaliadas do artista de id= '+ str(id) + ' foram removidas'},indent=4)
				status = 200
			r = make_response((resposta, status, {'Content-Type': 'application/json'}))
			return r
			
		if request.url == 'http://localhost:5000/musicas/all/utilizador/' + str(id): #DELETE ALL MUSICAS_U <id_user> 
			dados=json.loads(request.data)
			informacao = (int(dados['id_user']),)
			try:
				g.db[1].execute("DELETE FROM musicas WHERE id IN(SELECT id_musica FROM playlists WHERE id_user = ?)", informacao)
				g.db[0].commit()
			except sqlite3.OperationalError:
				resposta = json.dumps({'describedBy' : 'http://localhost:5000/musicas/all/utilizador/'+ str(id),'httpStatus': 500, 'title' : "Ocorreu um erro na execucao da query"},indent=4)
				status = 500
			else:
				# r = make_response('Todas as musicas avaliadas do utilizador de id= '+ str(id) + ' foram removidas')
				resposta = json.dumps({'status':'Todas as musicas avaliadas do utilizador de id= '+ str(id) + ' foram removidas'},indent=4)
				status = 200
			r = make_response((resposta, status, {'Content-Type': 'application/json'}))
			return r
		
		if request.url == 'http://localhost:5000/musicas/all/avaliacao': #DELETE ALL MUSICAS <avaliacao> 
			dados = json.loads(request.data)
			informacao = (dados['avaliacao'],)
			try:
				g.db[1].execute('DELETE FROM musicas WHERE id IN(SELECT id_musica FROM playlists WHERE id_avaliacao IN (SELECT id FROM avaliacoes WHERE sigla = ?))', informacao)
				g.db[0].commit()
			except sqlite3.OperationalError:
				resposta = json.dumps({'describedBy' : 'http://localhost:5000/musicas/all/avaliacao','httpStatus': 500, 'title' : "Ocorreu um erro na execucao da query"},indent=4)
				status = 500
			else:
				resposta = json.dumps({'status':'Todas as musicas com a avaliacao= '+ str(dados['avaliacao']) + ' foram removidas'},indent=4)
				status = 200
			r = make_response((resposta, status, {'Content-Type': 'application/json'}))
			return r

#------------------------------------------------------------------------------------
@app.route('/artistas', methods = ['PUT', 'GET', 'DELETE'])
@app.route('/artistas/<int:id>', methods = ['GET', 'DELETE'])
@app.route('/artistas/all/', methods = ['GET', 'DELETE'])
@app.route('/artistas/avaliadas/<int:id>', methods = ['GET', 'DELETE'])

def artistas(id = None):
	if request.method == "GET":
		if request.url == 'http://localhost:5000/artistas/' + str(id): #READ ARTISTA <id_artista> 
			dados=json.loads(request.data)
			informacao = (dados['id_artista'],)
			try:
				cur_id_spotify = g.db[1].execute('SELECT id_spotify FROM artistas WHERE id = ?', informacao) 
				id_spotify = cur_id_spotify.fetchone()[0]

				json_spotify = spotify_requests.requestArtista(token,id_spotify)
				lista_resp = ["Id do artista na base de dados: " + str(dados['id_artista'])]
				if json_spotify is not None:
					lista_resp.append("-----------INFORMACOES ENCONTRADAS NA API DO SPOTIFY:-----------")
					lista_resp.append(json_spotify)
					lista_resp.append("-----------------------------------------------------------------------")		
					resposta = json.dumps(lista_resp,indent=4)
					status = 200
				else:
					resposta = json.dumps({'describedBy' : 'http://localhost:5000/artistas/'+str(id),'httpStatus': 404, 'title' : "Nao foram encontradas informacoes. Id do artista invalido!'"},indent=4)
					status = 404
			except sqlite3.OperationalError:
				resposta = json.dumps({'describedBy' : 'http://localhost:5000/artistas/'+str(id),'httpStatus': 500, 'title' : "Ocorreu um erro na execucao da query"},indent=4)
				status = 500
			r = make_response((resposta, status, {'Content-Type': 'application/json'}))
			return r
		if request.url == 'http://localhost:5000/artistas/all/': #READ ALL ARTISTAS  
			try:
				cur = g.db[1].execute("SELECT * FROM artistas")
			except sqlite3.OperationalError:
				resposta = json.dumps({'describedBy' : 'http://localhost:5000/artistas/all/','httpStatus': 500, 'title' : 'Ocorreu um erro na execucao da query'},indent=4)
				status = 500
			else:
				linha = cur.fetchall()
				if linha is not None and len(linha) != 0:
					lista_musicas=["Informacoes relativas a todos os artistas existentes na bases de dados:"]
					lista_musicas.append("#")
					lista_musicas.append("#")
					lista_musicas.append("#")
					for info in linha:
						id_artista = info[0]
						id_spotify = info[1]
						nome = info[2]
						resposta_artista  = spotify_requests.requestArtista(token, str(id_spotify))
						lista_musicas.append("-----------ARTISTA: " + str(nome) + ": -----------")
						lista_musicas.append("-----------INFORMACOES ENCONTRADAS NA BASE DE DADOS:-----------")
						lista_musicas.append({'ID':str(id_artista),'ID do Spotify': str(id_spotify),'Nome': str(nome)})
						lista_musicas.append("-----------INFORMACOES ENCONTRADAS NA API DO SPOTIFY:-----------")
						lista_musicas.append(resposta_artista)
						lista_musicas.append("-----------------------------------------------------------------------")

					resposta = json.dumps(lista_musicas,indent=4)
					status = 200
		
				else:
					resposta = json.dumps({'describedBy' : 'http://localhost:5000/artistas/all/','httpStatus': 404, 'title' : 'Nao existem artistas na base de dados atualmente'},indent=4)
					status = 404
			r = make_response((resposta, status, {'Content-Type': 'application/json'}))
			return r
			
	if request.method == "PUT":
		if request.url == 'http://localhost:5000/artistas': #CREATE ARTISTA <id_spotify> 
			dados = json.loads(request.data)
			resposta_artista = spotify_requests.requestArtista(token, dados['id_spotify'])
			if resposta_artista is None:
				resposta = json.dumps({'describedBy' : 'http://localhost:5000/artistas','httpStatus': 404, 'title' : 'O id do spotify eh invalido'},indent=4)
				status = 404
				r = make_response((resposta, status, {'Content-Type': 'application/json'}))
				return r

			nome_artista = spotify_requests.getNomeFromArtista(resposta_artista)
			informacao = (dados['id_spotify'], nome_artista)
				
			cur_existe_artista = g.db[1].execute('SELECT id FROM artistas WHERE id_spotify = ?', (str(dados['id_spotify']),))
			existe_artista = cur_existe_artista.fetchone()
			if existe_artista is None:
				try:
					g.db[1].execute('INSERT INTO artistas VALUES (NULL, ?, ?)', informacao) 
					g.db[0].commit()
				except sqlite3.OperationalError:
					resposta = json.dumps({'describedBy' : 'http://localhost:5000/artistas','httpStatus': 500, 'title' : 'Ocorreu um erro na execucao da query'},indent=4)
					status = 500
				else:
					resposta = json.dumps({'status':'Novo artista com nome= ' + str(nome_artista) +  ' e id= ' + str(dados['id_spotify']) + ' inserido na base de dados'},indent=4)
					status = 200
				
			else:
				resposta = json.dumps({'describedBy' : 'http://localhost:5000/artistas','httpStatus': 409, 'title' : "Ja existe um artista com nome= " + str(nome_artista) +  " e id= " + str(dados['id_spotify']) + " inserido na base de dados"},indent=4)
				status = 409
			r = make_response((resposta, status, {'Content-Type': 'application/json'}))
			return r

	
	if request.method == "DELETE":
		if request.url == 'http://localhost:5000/artistas/' + str(id): #DELETE ARTISTA <id_artista> 
			try:
				g.db[1].execute("DELETE FROM artistas WHERE id=?", (int(id),))
				g.db[0].commit()
			except sqlite3.OperationalError:
				resposta = json.dumps({'describedBy' : 'http://localhost:5000/artistas/'+str(id),'httpStatus': 500, 'title' : 'Ocorreu um erro na execucao da query'},indent=4)
				status = 500
			else:
				resposta =json.dumps({'status': "Artista ID= " + str(id)+" eliminado"},indent=4)
				status = 200
			r = make_response((resposta, status, {'Content-Type': 'application/json'}))
			return r
		if request.url == 'http://localhost:5000/artistas/all/':#DELETE ALL ARTISTAS 
			try:
				g.db[1].execute("DELETE FROM artistas")
				g.db[0].commit()
			except sqlite3.OperationalError:
				resposta = json.dumps({'describedBy' : 'http://localhost:5000/artistas/all/','httpStatus': 500, 'title' : 'Ocorreu um erro na execucao da query'},indent=4)
				status = 500
			else:
				resposta =json.dumps({'status': "Todos os artistas foram removidos"},indent=4)
				status = 200
			r = make_response((resposta, status, {'Content-Type': 'application/json'}))
			return r


if __name__ =='__main__':
    app.run(debug=True)
