import os
import tarfile
from six.moves import urllib

#Diretorio pra baixar os dados
DOWNLOAD_ROOT = "https://github.com/ageron/handson-ml/tree/master/"
#Diretorio em que sera salvo os dados na minha maquina
HOUSING_PATH = "datasets/housing"
#Diretorio completo do arquivo compactado
HOUSING_URL = DOWNLOAD_ROOT + HOUSING_PATH + "/housing.tgz"

#Funcao que realiza o download dos dados que se encontra compacto.
#Em seguida sera realizado a extracao dos dados
#Isso permite que diferentes machinas realizem baixem e atualizem os dados

def fetch_housing_data(housing_url=HOUSING_URL, housing_path=HOUSING_PATH):
    #Checa se o diretorio na minha maquina se encontra criado
    if not os.path.isdir(housing_path):
        os.makedirs(housing_path)
    #Pegando o caminho "datasets/housing/housing.tgz"
    tgz_path = os.path.join( housing_path, "housing.tgz")

    #Copia o arquivo do github pro diretorio local
    #Se o arquivo ja existir, ele atualiza pro novo e substitui? verificar..
    urllib.request.urlretrieve( housing_url, tgz_path)

    #Extrair arquivo compactado
    housing_tgz = tarfile.open(tgz_path)
    housing_tgz.extractall(path=housing_path)
    housing_tgz.close()

fetch_housing_data()
