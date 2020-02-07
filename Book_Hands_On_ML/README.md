# Práticas em Machine Learn 
Os códigos elaborados foram baseado no livro Hands On Machine Learning with Scikit Learn and TensorFlow, nos meus códigos serão incluidos comentários para auxiliar o estudo e a compreensão do material.
Além disso, alguns códigos serão alterados para compreensão e prática da linguagem python, os gráficos plotados estarão no repositório ./Images/ mas serão incluidos no README.md também com uma breve explicação

[](https://raw.githubusercontent.com/EwertonPSA/Practices_Machine_Learn/master/Book_Hands_On_ML/Images/life%20satisfaction%20vs%20GDP.png=)

### Chapter 1 - Ex1 (PLOT E CODIGO ALTERADO)
Esse é um problema de regressão univariada pois explora apenas um recurso, dado a renda per capita de um pais(GDP) estimamos a 'Life satisfaction'. <br/>
O código do livro não contem esse gráfico, sendo gerado por mim para fins de estudo.<br/>
Fiz esse gráfico para ver o impacto do valor K no algorítimo de treinamento KNN. Além disso, inclui o modelo com regressão linear para comparar os diferentes modelos. Esse gráfico foi gerado pelo codigo Chapter1-Ex1-Life_Satisfaction.py e as partes importantes que devem ser observada no codigo: salvar imagem, leitura dos dados .csv e como foi plotado a imagem. 

<img src="https://raw.githubusercontent.com/EwertonPSA/Practices_Machine_Learn/master/Book_Hands_On_ML/Images/Chapter1_Fundamentals/life%20satisfaction%20vs%20GDP.png" width="500" height="300" />

### Chapter 2 – End-to-end Machine Learning project
Realizamos a simulação de um possivel problema "real".<br/>
Pontos importantes do código: visualização dos dados .csv( .value_count(); .counts(); .head(); .info() e .describe(): IMPORTANTE, permite ver informações de valores não nulos), estrutura correta para incluir link de download de arquivo a partir do github, atualização de tamanho do titulo nos subplot, agrupar informacoes ou passar informacoes continuas para discretas (pandas.cut()), .

<img src="https://raw.githubusercontent.com/EwertonPSA/Practices_Machine_Learn/master/Book_Hands_On_ML/Images/end_to_end_project/attribute_histogram_plots.png" width="1700" height="400" />

