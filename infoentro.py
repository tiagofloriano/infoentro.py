#!/usr/bin/python3
# -*- coding: latin-1 -*-

'''Calculates information entropy of dataset from MRT files
Usage:
    Run the file in the root of the directory where the directories containing the MRT files are located.
Author:
    Tiago Floriano - 2023-12-15
License:
    GNU GPL v3 License
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import numpy as np
import pandas as pd
import collections,os
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from scipy.interpolate import make_interp_spline
import scipy

# calculo da entropia
def calcular_entropia(conteudo):
    n = len(conteudo)
    contador = collections.Counter(conteudo)
    probabilities = [count / n for count in contador.values()]
    entropia = -sum(p * np.log2(p) for p in probabilities)
    return entropia

# defini��es
infodir = input("Informe o diret�rio onde est�o os arquivos MRT: ")
arquivo = input("Informe o nome do arquivo: ")
resultados =[] # lista de resultados

caminho_arquivo = "{}/{}".format(infodir,arquivo)

# Abra o arquivo em modo de leitura ('r')
with open(caminho_arquivo, 'r') as arquivo:
    # Leia o conte�do do arquivo
    conteudo = arquivo.read()

    # TRATAMENTO DO CONTE�DO DO ARQUIVO
    # filtrar conteudo do arquivo para usar apenas os resultados
    conteudo = conteudo.split('IDEOS-PIPELINE-LOG-FILE-END')

    # remover caracteres desnecess�rios da filtragem anterior 
    remover = "#-" 
    conteudo = ''.join(char for char in conteudo[1] if char not in remover)

    # filtrar apenas a segunda coluna
    linhas = conteudo.strip().split('\n')
    conteudo_col1 = [linha.split()[0] for linha in linhas]
    conteudo_col2 = [linha.split()[1] for linha in linhas]
    for calc_entro in conteudo_col2:
        # inserir resultados na lista
        resultados.append(round(calcular_entropia(calc_entro),3))

    
# MONTAR GR�FICO
tipograf = input("Tipo de gr�fico: [1] barras [2] linhas")

if tipograf == "1":
    # Criar o gr�fico de barras
    plt.bar(conteudo_col1, resultados, align='center', alpha=0.7, color='blue')
    plt.xticks(conteudo_col1, resultados)  # Define os n�meros no eixo x
elif tipograf == "2":
    # Criar a curva spline
    x = np.linspace(float(conteudo_col1[0]), float(conteudo_col1[-1]), 2000)
    #x = np.linspace(conteudo_col1.index(conteudo_col1[0]), conteudo_col1.index(conteudo_col1[-1]), 50)
    y = scipy.interpolate.make_interp_spline(conteudo_col1, resultados, k=2)(x)

    # Criar o gr�fico de linhas suaves
    plt.plot(x, y, color='blue')

conteudo_col1_numerico = [float(x) for x in conteudo_col1]
plt.xticks(conteudo_col1_numerico, resultados)  # Define os n�meros no eixo x
plt.xlabel('Col1')
plt.ylabel('Col2')
plt.title('Entropia da informa��o')

# Mostrar o gr�fico
plt.show()