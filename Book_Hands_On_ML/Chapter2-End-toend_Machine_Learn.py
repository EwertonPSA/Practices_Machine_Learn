import os
import tarfile
from six.moves import urllib

#IMPORTANTE: nao adianta copiar link da pagina web do github pra fazer o download
#Do arquivo .tgz, para fazer o download eh necessario pegar o link raw do github
#Inclui as variaveis necessarias para direcionar pro caminho correto para um arquivo
#Qualquer do github, a estrutura para direcionar para um arquivo qualquer do github seria
#LINK = os.path.join( HTTP_RAW, USER, REPOSITORY, "master/", PATH, FILE)
USER="ageron" #"EwertonPSA"
REPOSITORY="handson-ml" #"Practices_Machine_Learn"
HTTP_RAW="https://raw.githubusercontent.com"
PATH="datasets/housing" #"Book_Hands_On_ML/datasets/housing"
FILE="/housing.tgz"
DOWNLOAD_ROOT = os.path.join( HTTP_RAW, USER, REPOSITORY, "master/")
#Diretorio completo do arquivo compactado
HOUSING_URL = DOWNLOAD_ROOT + PATH + "/housing.tgz"

#Funcao que realiza o download dos dados que se encontra compacto.
#Em seguida sera realizado a extracao dos dados
#Isso permite que diferentes machinas realizem baixem e atualizem os dados

def fetch_housing_data(housing_url=HOUSING_URL, housing_path=PATH):
    #Checa se o diretorio na minha maquina se encontra criado
    if not os.path.isdir(housing_path):
        os.makedirs(housing_path)
    #Pegando o diretorio local "datasets/housing/housing.tgz"
    tgz_path = os.path.join( housing_path, "housing.tgz")
    print (HOUSING_URL)

    #Copia o arquivo do github pro diretorio local
    #Se o arquivo ja existir, ele atualiza pro novo e substitui? verificar..
    urllib.request.urlretrieve( housing_url, tgz_path)

    #Extrair arquivo compactado
    housing_tgz = tarfile.open(tgz_path)
    housing_tgz.extractall(path=housing_path)
    housing_tgz.close()

fetch_housing_data()
