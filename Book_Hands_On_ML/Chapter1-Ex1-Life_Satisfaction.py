

#Importar biblioteca python 2 e 3
#FROM __FUTURE__ -> Serve para utilizar funcionalidades do python mesmo que seja implementado em versoes futuras
from __future__ import division, print_function, unicode_literals

import numpy as np
import pandas as pd
import sklearn.linear_model
import os

#Definir uma semente pro rand
np.random.seed(42)

#PRA PLOTAGEM
#%matplotlib inline -> PROBLEMA, SO FUNCIONA PRA IPython, nao pra Python cl
#pra resolver isso substitua por 'exec(%matplotlib inline)'
'exec(%matplotlib inline)'
import matplotlib as mpl
import matplotlib.pyplot as plt

#ignorar warnings
import warnings
warnings.filterwarnings(action="ignore", message="^internal gelsd")

#Customizando as plotagens
mpl.rc('axes', labelsize=14)#Titulo dos eixos
mpl.rc('xtick', labelsize=12)#tamanho dos valores q vao na legenda da coordenada x
mpl.rc('ytick', labelsize=12)#tamanho dos valores q vao na legenda da coordenada y

#Local em que sera salvo as figuras
PROJECT_ROOT_DIR = "."

def save_fig(fig_id, tight_layout = True):
    #os.path.join->Definindo diretorio, em cada ',' 
    #nos parametros sera incluido '/' para definir o diretorio
    #Onde sera salvo as imagens
    path = os.path.join(PROJECT_ROOT_DIR, "Images", fig_id + ".png")
    print("Saving figure", fig_id)
    if(tight_layout):
        #Utilizado para redimensionar os objetos de um subplot 
        #de forma que fique visivel, eh feito automaticamente isto chamando plt.tight_layout()
        plt.tight_layout()
    plt.savefig(path, format='png', dpi=300)


#Tratando as entradas
def prepare_country_stats(oecd_bli, gdp_per_capita):
    oecd_bli = oecd_bli[oecd_bli["INEQUALITY"]=="TOT"]

    #Aqui eh remodelado a tabela lida no .csv
    #A tabela remodelada tera como conteudo de index as informacoes que estao contidas no campo(coluna) "Country" da tabela antiga
    #A tabela remodelada criarah colunas com informacoes que estao contidas no campo(coluna) "Indicator" da tabela antiga
    #Os valores incluidos na tabela remodelada virah a partir das informacoes contidas no campo(coluna) "Value" da tabela antiga
    oecd_bli = oecd_bli.pivot(index="Country", columns="Indicator", values="Value")
   
    #Renomeia a coluna e inplace=True faz com que a copia da tabela remodelada seja ignorada, pois quero que a mudança ocorra na tabela
    gdp_per_capita.rename(columns={"2015":"GDP per capita"}, inplace=True)
    gdp_per_capita.set_index("Country", inplace = True)
    
    #Juncao das duas tabelas, tipo do SQL
    #left_index e right_index = True significa que usaram a chave das duas tabelas como index para realizar a juncao
    full_country_stats=pd.merge( left=oecd_bli, right=gdp_per_capita, 
                                left_index=True, right_index=True)

    #Ordenacao baseado na coluna "GDP per capita"
    #inplace=True faz com que a ordenacao seja realizada na propria tabela
    full_country_stats.sort_values(by="GDP per capita", inplace=True)
    remove_indices = [0,1,6,8,33,34,35]
    keep_indices = list(set(range(36)) - set(remove_indices))

    #Retorna parte da tabela baseado nos indices que selecionei
    return full_country_stats[["GDP per capita", 'Life satisfaction']].iloc[keep_indices]

datapath = os.path.join( "dataset", "lifesat", "") #Caminho dos dados

oecd_bli = pd.read_csv(datapath + "oecd_bli_2015.csv", thousands=',')
gdp_per_capita = pd.read_csv(datapath + "gdp_per_capita.csv", thousands=',', 
                            delimiter='\t', encoding='latin1', na_values="n/a")

country_stats = prepare_country_stats(oecd_bli, gdp_per_capita)

#Numpy.c_-> transpoem um array e concatena(caso seja incluido mais nos seus parametros)
#Nesse caso ele ta pegando o array do conteudo "GDP per capita" de country
#Obtendo como coluna e repassando pra X

X = np.c_[country_stats["GDP per capita"]]
y = np.c_[country_stats["Life satisfaction"]]

#Definindo informacoes da plotagem
#o kind define o tipo formatacao das informacoes na plotagem
#kind pode ser igual a line e os pontos serao interligados por exemplo
#mais exemplos em http://queirozf.com/entries/pandas-dataframe-plot-examples-with-matplotlib-pyplot
#country_stats.plot(kind='scatter', x="GDP per capita", y='Life satisfaction')
#plt.show()

#Cria um modelo utilizando regressao linear
model = sklearn.linear_model.LinearRegression()

#Treina o modelo a partir do conjunto de dados
model.fit(X,y)

#X_New representa um valor que sera usado para tentar predizer utilizando o modelo
#X_new = [[22587]]
#print(model.predict(X_new))

#IMPORTANTE PARA APLICAR OS MODELOS
from sklearn.neighbors import KNeighborsRegressor


modelKNN3= sklearn.neighbors.KNeighborsRegressor(n_neighbors=3)
modelKNN3.fit(X,y)

modelKNN1= sklearn.neighbors.KNeighborsRegressor(n_neighbors=1)
modelKNN1.fit(X,y)

plt.scatter(X, y, label='Dataset' ,color='blue')
plt.plot(X, model.predict(X), linestyle='-', label='Model Linear Regression', color='red')
plt.plot(X, modelKNN3.predict(X), linestyle='--', label='Model KNN(k=3)', color='green', linewidth=4)
plt.plot(X, modelKNN1.predict(X), linestyle='-.', label='Model KNN(k=1)', color='black')
plt.legend()#ativa a legenda
plt.grid(True)
plt.title('Dataset and Models training of life satisfaction vs GDP')
save_fig("life satisfaction vs GDP")
plt.show()

