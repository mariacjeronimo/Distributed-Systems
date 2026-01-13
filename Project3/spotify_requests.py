"""
Aplicações Distribuídas - Projeto 3 - spotify_requests.py
Grupo: 23
Números de aluno: Maria Jerónimo 56887, Lara Ângelo 56945
"""
import json
import requests

#------------------------GERAR TOKEN AUTOMATICAMENTE----------------------------------------
def generateNewOAuthToken():
    url = 'https://accounts.spotify.com/api/token'

    CLIENT_ID = '4a28ffa21f4a44b5bb99aa21b0835611'
    CLIENT_SECRET = 'c09e52dea57e44798f4030ac40656104'

    auth_response = requests.post(url, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    })


    auth_response_data = auth_response.json()
    OAuthToken = auth_response_data['access_token']
    
    return( OAuthToken )

#print('Token: ' + generateNewOAuthToken() )
#
# #token = generateNewOAuthToken()
# #id_artista = '1lQnDEcvFAWaUjbyZiHKih'
# #id_musica = '4YK4SXrTvreEWvJNOdg3wW'

#--------------------REQUESTS INFORMAÇÃO------------------------------------
def requestArtista(OAuth_token, id_artista): #READ ARTISTA
    
    headers = {
    'Authorization': 'Bearer {token}'.format(token=OAuth_token)
    }

    url = 'https://api.spotify.com/v1/artists/' + id_artista

    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        return( resp.json() )
    else:
        return(None)

def requestMusica(OAuth_token, id_musica): #READ MUSICA
    headers = {
    'Authorization': 'Bearer {token}'.format(token=OAuth_token)
    }

    url = 'https://api.spotify.com/v1/tracks/' + id_musica
    
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return( resp.json() )
    else:
        return(None)


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