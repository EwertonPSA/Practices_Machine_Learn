import os
import tarfile
import pandas as pd
'exec(%matplotlib inline)'
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
np.random.seed(42) #Gerar saidas iguais ao do livro
params = {'axes.titlesize':'30',
        'xtick.labelsize':'15',
        'ytick.labelsize':'15'}
        
from six.moves import urllib
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedShuffleSplit
from pandas.plotting import table


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
def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
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

#IMPORTANTE
#Eh incluido os parametros de texto no DataFrame
mpl.rcParams.update(params)

#Plotagem de um histograma por coluna nos dados lidos do arquivo .csv
#figsize=(30,15)-> 30 em x e 15 em y
#bins=50-> significa que na plotagem os dados serao dividos em 50 partes(Na coordenada x) e incluido as barras correspondente a cada informacao
#           Se incluir 5 por exemplo, havera 5 barras apenas com os dados preenchidos
csv.hist(bins=50, figsize=(30, 15))
plt.suptitle("Histogram of csv file".upper(), fontsize=34)

save_fig("attribute_histogram_plots")
plt.close()

#############################################################################
#A seguir compararemos duas formas de selecionar os dados de treino e teste
#Um nao considera a proporcao existente nos dados(train_test_split)
#O outro considera a proporcao da renda media nos dados e depois 
#Realiza o serteio seguindo esse criterio(StratifeShuffleSplit)
#############################################################################

#Sera reunido as informacoes de "median_income"(renda media)
#Em um conjunto de labels, faremos isso para depois considerar as proporcoes
#Existente nos dados e fazer o sortei adequado para teste e treinamento
#Os dados serao reunidos em uma nova coluna da tabela .csv
#Que chama "income_cat". Os valores que estao entre as sessoes 0 e 1.5
#Entraram na sessao de label 1, os valores que estao entre as sessoes 1.5 e 3.0
#Entram na sessao de label 2 e assim por diante
intervalos = [0., 1.5, 3.0, 4.5, 6., np.inf]
labels_Intervalos = [1, 2, 3, 4, 5]
#FUNCAO PD.CUT IMPORTANTE PRA PASSAR VALORES CONTINUOS PARA DISCRETOS 
csv["income_cat"] = pd.cut(csv["median_income"], bins=intervalos, labels=labels_Intervalos)

#Particionar os dados em treinamento e teste, com 20% para teste 
#IMPORTANTE: train_test_split() separa os dados nao considerando
#            A proporcao existente nos dados, podendo causar um vies
train_set, test_set = train_test_split(csv, test_size=0.2, random_state=42)

#Validacao cruzada com embaralhamento
split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

#split.split gera indices para treinamento e teste
#csv=Conjunto de dados a serem estratificados
#csv["income_cat"]=Usado para analisar a proporcao dos dados e realizar a estratificacao adequada com a proporcao
#O 'for' serve para retirar os n sorteios(que nesse caso seria apenas 1)
#Em strat_train_set e strat_test_set tera (DataFrames) um grupo de informacoes obtidos pelos index
#Para realizar o treinamento e teste. 
for train_index, test_index in split.split( csv, csv["income_cat"]):
    strat_train_set = csv.loc[train_index]
    strat_test_set = csv.loc[test_index]

#Obtendo as proporcoes de "income_cat" a partir dos data( DataFrame )
def income_cat_proportions(data):
    return data["income_cat"].value_counts() / len(data)

#Criando um DataFrame
compare_props = pd.DataFrame({
    "Overall": income_cat_proportions(csv),
    "Stratified": income_cat_proportions(strat_test_set),
    "Random": income_cat_proportions(test_set), }).sort_index()
compare_props["Rand. %error"] = 100*compare_props["Random"] / compare_props["Overall"] - 100
compare_props["Strat. %error"] = 100*compare_props["Stratified"] / compare_props["Overall"] - 100
fig, ax = plt.subplots(1,1)
table(ax, np.round(compare_props, 5), loc='upper center', colWidths=[0.15, 0.15, 0.15, 0.15, 0.15])
compare_props.plot(ax=ax, ylim=(-10, 10))
ax.legend(loc='lower left')
plt.suptitle("Error stratified versus purely random sampling".upper(), fontsize=14)
save_fig("stratified_versus_random")
plt.close()

#Removendo as proporcoes 
for set in (strat_train_set, strat_test_set):
    #axis=1->Remover o "income_cat" que se encontra na coluna da tabela
    set.drop(["income_cat"], axis=1, inplace=True)

