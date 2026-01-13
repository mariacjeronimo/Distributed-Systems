#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 4 - servidor.py
Grupo: 23
Números de aluno: Maria Jerónimo 56887, Lara Ângelo 56945
"""
# Zona para fazer imports
import json
import requests
from requests_oauthlib import OAuth2Session
from flask import Flask, request, make_response, redirect, url_for, jsonify
import servidor 

def requestArtista(id_artista): #READ ARTISTA

    url = 'https://api.spotify.com/v1/artists/' + id_artista
    resp = servidor.spotify.get(url).json()

    
    return(resp)
    

def requestMusica(id_musica): #READ MUSICA

    url = 'https://api.spotify.com/v1/tracks/' + id_musica
    resp = servidor.spotify.get(url).json()

    return(resp)



# resposta_artista = requestArtista(token, id_artista)
# resposta_musica  = requestMusica(token, id_musica)


#-------------------------------------------COMPLETAR TABELAS----------------------------------------------
def getNomeFromArtista(resposta): #TABELA ARTISTA (descobrir nome do artista através do id_artista)
        return( resposta["name"] )



def getNomeFromMusica(resposta): #TABELA MUSICA
        return( resposta['name'] )
  

def getIdArtistaFromMusica(resposta):#TABELA MUSICA
        return( resposta['album']['artists'][0]['id'] )
    



# print(getNomeFromArtista(resposta_artista))
# print( getNomeFromMusica(resposta_musica) )
# print( getIdArtistaFromMusica(resposta_musica) )