import cv2
import os
import numpy as np
import pandas as pd

# Definir o caminho para o diretório das imagens
caminho_diretorio = 'imagens/Lmpp_tratada'

# Definir a área da circunferência utilizada para calcular o volume das boias
Area_da_circunferencia = 1.0

# Definir a cor laranja em RGB
laranja = (0, 165, 255)

# Inicializar as listas de volumes, quantidades de água e coeficientes de variação
volumes = []
quantidades_de_agua = []
coeficientes_variacao = []

# Loop através de todas as imagens no diretório
for nome_arquivo in os.listdir(caminho_diretorio):
    # Verificar se o arquivo é uma imagem
    if nome_arquivo.endswith('.jpg') or nome_arquivo.endswith('.png'):

        # Carregar a imagem
        img = cv2.imread(os.path.join(caminho_diretorio, nome_arquivo))

        # Converter para escala de cinza
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Filtrar apenas as cores laranja
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_orange = np.array([0, 100, 100])
        upper_orange = np.array([20, 255, 255])
        mask = cv2.inRange(hsv, lower_orange, upper_orange)

        # Aplicar limiarização para separar o fundo das boias
        _, thresh = cv2.threshold(mask, 100, 255, cv2.THRESH_BINARY)

        # Aplicar um filtro gaussiano para suavizar a imagem
        blur = cv2.GaussianBlur(thresh, (5,5), 0)

        # Encontrar contornos na imagem filtrada
        contours, _ = cv2.findContours(blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Desenhar os contornos encontrados na imagem original
        for cnt in contours:
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(img, (x,y), (x+w,y+h), laranja, 2)

            # Calcular o volume da boia
            volume = (w/2)**2 * np.pi * Area_da_circunferencia
            volumes.append(volume)

            # Calcular a quantidade de água no tubo
            quantidade_de_agua = 250 - (250*w/img.shape[1])
            quantidades_de_agua.append(quantidade_de_agua)
        
        # Calcular o coeficiente de variação
        coef_variacao = np.std(volumes) / np.mean(volumes)
        coeficientes_variacao.append(coef_variacao)
        
# Salvar os coeficientes de variação em um único arquivo CSV
df = pd.DataFrame({'nome_arquivo': os.listdir(caminho_diretorio),
                   'coeficiente_variacao': coeficientes_variacao})
df.to_csv('coeficientes_variacao.csv', index=False)

