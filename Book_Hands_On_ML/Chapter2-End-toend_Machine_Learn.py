import os
import tarfile
from six.moves import urllib

#IMPORTANTE: nao adianta copiar link da pagina web do github pra fazer o download
#Do arquivo .tgz, para fazer o download eh necessario pegar o arquivo
#Pela pagina raw...A variavel DOWNLOAD_ROOT serve como referencia para obter o caminho html
#Na frente inclua o diretorio do seu github ateh o arquivo e o nome do arquivo
#Se isso nao for feito da erro em urlib.request.urlretrieve()
DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml/master/"

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
    print (housing_url)

    #Copia o arquivo do github pro diretorio local
    #Se o arquivo ja existir, ele atualiza pro novo e substitui? verificar..
    urllib.request.urlretrieve( housing_url, tgz_path)

    #Extrair arquivo compactado
    housing_tgz = tarfile.open(tgz_path)
    housing_tgz.extractall(path=housing_path)
    housing_tgz.close()

fetch_housing_data()
