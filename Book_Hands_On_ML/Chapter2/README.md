# Chapter 2 – End-to-end Machine Learning project
Realizamos a simulação de um possivel problema "real"

Pontos importantes do código: visualização dos dados .csv( .value_count(); .counts(); .head(); .info() e .describe(): IMPORTANTE, permite ver informações de valores não nulos), estrutura correta para incluir link de download de arquivo a partir do github, atualização de tamanho do titulo nos subplot, analise das proporções na validação cruzada.

### Parte 1
Visualização dos dados


<img src="https://raw.githubusercontent.com/EwertonPSA/Practices_Machine_Learn/master/Book_Hands_On_ML/Chapter2/Images/end_to_end_project/attribute_histogram_plots.png" width="1700" height="400" />

### Parte 2

Medimos as proporções da categoria de renda no conjunto de testes e no conjunto ddos dados para avaliar as proporções. Comparamos o conjunto de testes gerados por amostragem estratificada e vemos que ela tem proporções de categoria de renda quase idênticas às do conjunto de dados completo(conjunto de dados usado), enquanto o conjunto de testes gerado usando amostragem puramente aleatória é bastante distorcido.

<img src="https://raw.githubusercontent.com/EwertonPSA/Practices_Machine_Learn/master/Book_Hands_On_ML/Chapter2/Images/end_to_end_project/stratified_versus_random.png" width="600" height="400" />

### Parte 3
A partir dos dados geramos imagens com recursos visuais para facilitar a visualização dos dados. Por exemplo, os circulos possuem raios que estabelecem a densidde em cada localização e também possuem cores demonstrando os preços.

<img src="https://raw.githubusercontent.com/EwertonPSA/Practices_Machine_Learn/master/Book_Hands_On_ML/Chapter2/Images/end_to_end_project/california_housing_prices_scatterplot.png" width="600" height="400" />

### Parte 4
Analisando relações entre os dados.No segundo gráfico é possivel ver uma linha na parte superior, sendo um problema para o algoritimo de treinamento.

<img src="https://raw.githubusercontent.com/EwertonPSA/Practices_Machine_Learn/master/Book_Hands_On_ML/Chapter2/Images/end_to_end_project/scatter_matrix_plot.png" width="600" height="400" />

<img src="https://raw.githubusercontent.com/EwertonPSA/Practices_Machine_Learn/master/Book_Hands_On_ML/Chapter2/Images/end_to_end_project/income_vs_house_value_scatterplot.png" width="600" height="400" /> 
