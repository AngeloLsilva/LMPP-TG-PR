import cv2
import os
import numpy as np

# Definir o caminho para o diretório das imagens
caminho_diretorio = 'imagens/Lmpp_tratada'

# Definir a área da circunferência utilizada para calcular o volume das boias
Area_da_circunferencia = 1.0

# Definir a cor laranja em RGB
laranja = (0, 165, 255)

# Inicializar a lista de volumes
volumes = []

# Abrir o arquivo resultados.txt em modo de escrita
arquivo_resultados = open("resultados.txt", "w")

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
            cv2.rectangle(img, (x,y), (x+w, y+h), laranja, 2)

        # Salvar a imagem com os contornos desenhados em um diretório
        cv2.imwrite('imagens_com_contornos/' + nome_arquivo, img)

        # Carregar a imagem com os contornos desenhados
        imagem = cv2.imread('imagens_com_contornos/' + nome_arquivo)

        # Realizar as análises desejadas na imagem
        # Por exemplo, medir a área da região de interesse
        roi = imagem

        # Escrever o resultado no arquivo de texto
        arquivo_resultados.write("Imagem: {}\n".format(nome_arquivo))
        arquivo_resultados.write("Número de boias: {}\n".format(len(contours)))
        arquivo_resultados.write("Volume total das boias: {} m³\n".format(sum(volumes)))
