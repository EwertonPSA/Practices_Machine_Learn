import os
import tarfile
import pandas as pd
'exec(%matplotlib inline)'
import matplotlib as mpl
mpl.rc('axes', labelsize=14)
mpl.rc('xtick', labelsize=12)
mpl.rc('ytick', labelsize=12)
import matplotlib.pyplot as plt
from six.moves import urllib


#################################################################################
#Variaveis utilizadas na funcao fetch_housing_data()

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
################################################################################


#Funcao que realiza o download dos dados que se encontra compactado.
#Em seguida sera realizado a extracao dos dados
#Isso permite que diferentes maquinas realizem baixem e atualizem os dados

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

def load_housing_data(housing_path=PATH):
    csv_path = os.path.join( housing_path, "housing.csv")
    return pd.read_csv(csv_path)

##############################################################################
#Variaveis utilizadas na funcao save_fig
PROJECT_ROOT_DIR = "."
CHAPTER_ID = "end_to_end_project"
IMAGES_PATH = os.path.join( PROJECT_ROOT_DIR, "Images", CHAPTER_ID)
##############################################################################

#Funcao para salvar imagem
#Parametros: 
#   fig_id = Nome da imagem
def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=200):
    path = os.path.join(IMAGES_PATH, fig_id + "." + fig_extension)

    #Se nao existir o diretorio entao sera criado para jogar a imagem la

    if not os.path.isdir(IMAGES_PATH):
        os.makedirs(IMAGES_PATH)
    
    print("Saving figure", fig_id)

    #Retirei esse ajuste pois a imagem estava ficando feia
    #if tight_layout:
       # plt.tight_layout()
    plt.savefig( path, format=fig_extension, dpi=resolution)

fetch_housing_data()
csv = load_housing_data()
#OBS: para mostrar os dados lidos com csv.head() no terminal deve incluir o print nele
print("\n" + "Observando as estruturas do .csv e as 5 primeiras linhas".upper())
print(csv.head())

#IMPORTANTE: csv.info() permite obter informacoes do arquivo .csv como os tipos de atributos
print("\n" + "Detalhando as estruturas que se encontram no .csv".upper())
print(csv.info())

print("\n" + "Observando os valoes que se encontra na coluna \"ocean proximity\" e quantas vezes aparece".upper())
print(csv["ocean_proximity"].value_counts())


print("\n" + "Observando informações de max, min, quartis e outros dados da tabela".upper())
print(csv.describe())

#Plotagem de um histograma por coluna nos dados lidos do arquivo .csv
#figsize=(30,15)-> 30 em x e 15 em y
#bins=50-> significa que na plotagem os dados serao dividos em 50 partes(Na coordenada x) e incluido as barras correspondente a cada informacao
#           Se incluir 5 por exemplo, havera 5 barras apenas com os dados preenchidos
csv.hist(bins=50, figsize=(30,15))
plt.suptitle("Histogram of csv file".upper())
save_fig("attribute_histogram_plots")
plt.show()

