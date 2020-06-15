import pandas as pd
import re 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Definindo as funções
def ResumeDados(data):
    """
    Resume as porcentagens de valores missings e os tipos das colunas em um dataframe.
    
    param data: Dataframe para sumarizar os dados
    
    returns: dataFrame com valores missings.
    """
    
    tipos = data.dtypes
    missingValues = data.isna().sum().sort_values(ascending=False)
    dfMissingValues = pd.DataFrame({"Tipo": tipos,
                                    "NumValorMissing": missingValues,
                                    "PorcentagemValorMissing(%)": (round((missingValues/data.shape[0])*100, 2))})

    dfMissingValues = dfMissingValues[dfMissingValues["PorcentagemValorMissing(%)"] > 0]
    
    return dfMissingValues

def converteBoolParaInt(x):
    
    """
    Converte strings ou booleans para inteiro.
    
    param x: Valor de cada registro.
    
    returns: inteiro.
    """
    
    padraoTrue = "True|1|SIM"
    padraoFalse = "False|0|NAO"
    
    if isinstance(x, bool):
        return int(x)
    elif isinstance(x, str):
        if re.search(padraoTrue, x):
            return int(1)
        elif re.search(padraoFalse, x):
            return int(0)

def agrupaColunaJuridicaMacro(x):
    if x == "ENTIDADES EMPRESARIAIS":
        return(0)
    elif x == "ENTIDADES SEM FINS LUCRATIVOS":
        return(1)
    else:
        return(2)

def agrupaColunaIdadeEmp(x):
    if x == "1 a 5" or x == '<= 1':
        return(0)
    elif x == "5 a 10":
        return(1)  
    elif x == "10 a 15":
        return(2)
    elif x == "15 a 20":
        return(3)
    else:
        return(4)
    
def agrupaColunaUF(x):
    """
    Agrupa a coluna UF para diminuir a cardinalidade da coluna.
    
    param x: Valor de cada registro.
    
    returns: \Valor categórico como inteiro.
    """
    if x == "MA":
        return(0)
    elif x == "RN":
        return(1)
    elif x == "AM":
        return(2)
    elif x == "PI":
        return(3)
    # Outros
    else:
        return(4)
    
def heatMap(data):
    """
    Imprime o heatmap de correlação.
    
    param data: Dataframe para plotar o heatmap.
    """
    
    corr = data.corr()

    mask = np.triu(np.ones_like(corr, dtype=np.bool))

    f, ax = plt.subplots(figsize=(18, 15))

    sns.heatmap(corr, mask=mask, cmap='RdBu', vmax=.3, fmt='.1f', annot=True, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})
    

def geraRecomendacao(portifolio, mercado, modelo):
    distancias, indices = modelo.kneighbors(portifolio)
    
    recomendacaoDF = pd.DataFrame({'indice': indices.flatten(),
                                   'distancia': distancias.flatten()})
    
    ids_pred = mercado.reset_index().iloc[recomendacaoDF.indice].id.values
    
    return ids_pred

def metrica_acc(acerto, Total):
    return round((acerto/Total)*100, 2)