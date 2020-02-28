import os
import tarfile
import pandas as pd
'exec(%matplotlib inline)'
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg #Carregar .png
np.random.seed(42) #Gerar saidas iguais ao do livro
params = {'axes.titlesize':'30',
        'xtick.labelsize':'15',
        'ytick.labelsize':'15'}
        
from six.moves import urllib
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedShuffleSplit
from pandas.plotting import table #Colocar a tabela na figura stratified_versus_random.png
from pandas.plotting import scatter_matrix #Visualizar as relacoes entre os dados

# Computar a mediana dos atributos
try:
    from sklearn.impute import SimpleImputer #Scikit-Learn 0.20+
except ImportError:
    from sklearn.preprocessing import Imputer as SimpleImputer

#Usado para transformar as labels do atributo 'ocean_proximity' em valores discretos
try:
    from sklearn.preprocessing import OrdinalEncoder
    from sklearn.preprocessing import OneHotEncoder
except ImportError:
    from future_encoders import OneHotEncoder # Scikit-Learn <0.20



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
#   verify = Caso seja true e o arquivo ja existir entao nao eh sobreescrito o arquivo
#            Caso seja false o arquivo eh criado (Ou sobreescrito caso ja exista)
#   fig_id = Nome da imagem
def save_fig(verify, fig_id, tight_layout=True, fig_extension="png", resolution=300):
    path = os.path.join(IMAGES_PATH, fig_id + "." + fig_extension)

    #Se nao existir o diretorio entao sera criado para jogar a imagem la
    if not os.path.isdir(IMAGES_PATH):
        os.makedirs(IMAGES_PATH)

    if (os.path.isfile(path)) & (verify == True):
        print ("File " + fig_id + "." + fig_extension + " has already been created")
        return

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

save_fig( True, "attribute_histogram_plots")
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
save_fig( True, "stratified_versus_random")
plt.close()

#Removendo as proporcoes 
for set in (strat_train_set, strat_test_set):
    #axis=1->Remover o "income_cat" que se encontra na coluna da tabela
    set.drop(["income_cat"], axis=1, inplace=True)


csv = strat_train_set.copy()

#Carrega a imagem para incluir como tela de fundo na plotagem dos dados
california_img=mpimg.imread(PROJECT_ROOT_DIR + '/Images/end_to_end_project/california.png')

#Visualizacao das informacoes em area
#alpha=0.4-> auxilia na visualizacao da densidade das informacoes
#s->usado para determinar o tamanho do circulo a partir de csv["populaion"]
#c->usado para definir cores(preco) a partir das informacoes em "median_house_value" em csv que sera definido em cmap
ax = csv.plot(kind="scatter", x="longitude", y="latitude", alpha=0.4,
        s=csv["population"]/100, label="population", figsize=(10,7),
        c="median_house_value", cmap=plt.get_cmap("jet"), colorbar=False,
        sharex=False)#Colorbar da tabela foi desativado

#extent->onde a imagem vai ser incluida seguindo as coordenadas dos dados
#        (-124.55: coordenada x lateral esquerda, -113.90: coordenada x lateral direita)

plt.imshow(california_img, extent=[-124.55, -113.90, 32.45, 42.05], alpha=0.5, 
        cmap=plt.get_cmap("jet"))
plt.ylabel("Latitude", fontsize=14) #Mudando o tamanho das labels
plt.xlabel("Longitude", fontsize=14)

#Incluindo na barra de cores os preços, pra isso pegaremos os precos minimos e maximos
#e dividiremos os precos em 11 partes, em seguida jogaremos os valores nas legendas em y da barra
#Em seguida
prices = csv["median_house_value"]
tick_values = np.linspace(prices.min(), prices.max(), 11)
#Criando um colorbar com nossas labels
cbar = plt.colorbar()
#imprimi no formado "$%dk", o argumento eh (round(v/1000), aparentemente o % serve
#Como simbolo para definir os parametros
cbar.ax.set_yticklabels(["$%dk"%(round(v/1000)) for v in tick_values], fontsize=14)
cbar.set_label('Median House Value', fontsize=16)

plt.legend(fontsize=16)
save_fig( True, "california_housing_prices_scatterplot")
plt.close()




# Escolhendo quais atributos desejo relacionar para avaliar as relacoes entre os dados
attributes = ["median_house_value", "median_income", "total_rooms", "housing_median_age"]
scatter_matrix(csv[attributes], figsize=(12,8))
save_fig( True, "scatter_matrix_plot")
plt.close()
csv.plot(kind="scatter", x="median_income", y="median_house_value", alpha=0.1, figsize=(20,12))
mpl.rcParams.update(params)
plt.axis([0, 16, 0, 550000])#Definindo intervalo que sera plotado
plt.ylabel("median_house_value", fontsize=25)
plt.xlabel("median_income", fontsize=25)
save_fig( True, "income_vs_house_value_scatterplot")
plt.close()

#Divide cada valor de um atributo por outro atributo de mesmo index
csv["rooms_per_household"] = csv["total_rooms"]/csv["households"]
csv["bedrooms_per_room"] = csv["total_bedrooms"]/csv["total_rooms"]
csv["population_per_household"] = csv["population"]/csv["households"]

#Avaliando as relacoes com os dados
corr_matrix = csv.corr()
print("\n" + "Correlacao entre \"median_house_value\" e outros atributos".upper())
print( corr_matrix["median_house_value"].sort_values(ascending=False))
print()

print(csv["total_bedrooms"].value_counts())

#Vamos preparar os dados para aplicar algoritimos de treinamento
#A seguir vamos separar os rotulos dos preditores
csv = strat_train_set.drop("median_house_value", axis=1)#Retirando os rotulos dos conjuntos de treinamento
csv_labels = strat_train_set["median_house_value"].copy()#Obtendo as labels

#visualizar se existe dados nulos
#csv.isnull() -> Verifica os valores nulos e retorna um dataframe
#csv.isnull().any() -> Faz reducao na linha pra identificar quais colunas sao considerados nulos
#null_columns -> pega as colunas que sao tem algum index nulo
null_columns = csv.columns[csv.isnull().any()]
print('\n' + 'Informa quantos nulos tem no csv'.upper())
print(csv[null_columns].isnull().sum())#Conta os nulos das colunas que possuem nulos

#csv.isnull().any(axis=1)->Reducao considerando as colunas, retornando booleanos dos index que contem nulos
print(csv[csv.isnull().any(axis=1)][null_columns].head())



#Vamos obter as medianas dos atributos da tabela csv por meio do Imputer
#As medianas serao usadas para substituir os valores nulos do csv
#Tres formas de substituir valores nulos(pg 82):
#   -Retirar a coluna
#   -Retirar os index com nulos
#   -Substituir pela mediana
imputer = SimpleImputer(strategy="median")

#ATENCAO: Soh pode ser obtido a mediana para valores numericos, a nossa tabela csv
#         Contem em "ocean_proximity" string, entao retiraremos ela pra jogar em uma copia
csv_num = csv.drop("ocean_proximity", axis=1)
imputer.fit(csv_num)#Obtem as medianas, que se encontram em imputer.statistics_
X = imputer.transform(csv_num)#X eh uma matriz simples contem a tabela csv_num com as medianas no lugar dos nulos

#Repassando a matriz X como um DataFrame contendo as labels de antes
#O csv_tr tera como indice os mesmo do csv(que serao obtidos seguindo a sequencia do csv em um array)
csv_tr = pd.DataFrame(X, columns=csv_num.columns, index=csv.index)

#Pegando DataFrame que contem apenas os valores nulos
sample_incomplete_rows = csv[csv.isnull().any(axis=1)]
#Agora verifico como esses valores estao apos inclusao da mediana
#O Dataframe.loc me permite acessar um conjunto de linhas ou colunas

print('Visualizando os valores nulos contidos em \"total_bethroon\" e a inclusao da mediana neles')
print(csv.loc[sample_incomplete_rows.index.values].head())
print()
print(csv_tr.loc[sample_incomplete_rows.index.values].head())

#Transformando os atributos de 'ocean_proximity', que esta representado por texto, em valores discretos
csv_cat = csv[['ocean_proximity']] #Pegando os textos contidos em 'ocean_proximity'
ordinal_encoder = OrdinalEncoder()
csv_cat_encoded = ordinal_encoder.fit_transform(csv_cat)

print('\n', "Transformando a distancia dos distrituos ao oceano em valores discretos")
print(ordinal_encoder.categories_)

print('\n', "Visualizacao dos primeiros distritos categorizado por distancia de oceano")
print(csv_cat_encoded[:10])

cat_encoder = OneHotEncoder()
#Com os textos contidos em 'ocean_proximity' eh montado o oneHotEncode
csv_cat_1hot = cat_encoder.fit_transform(csv_cat)

print("\n", "colunas:", ordinal_encoder.categories_)#TERMINAR AQUI DE INCLUIR OS NOMES DAS COLUNAS
print("\n", "montado o oneHotEncode, nas linhas temos instancias e nas colunas as labels dos oceanos")
print(csv_cat_1hot.toarray())



