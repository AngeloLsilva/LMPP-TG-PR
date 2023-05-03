import cv2
import os
import numpy as np

# Definir o caminho para o diretório das imagens
caminho_diretorio = 'imagens/Lmpp'

# Definir a área da circunferência utilizada para calcular o volume das boias
Area_da_circunferencia = 1.0

# Definir a cor laranja em RGB
laranja = (0, 165, 255)

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
        roi = imagem[y:y+h, x:x+w]
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, thresh_roi = cv2.threshold(gray_roi, 100, 255, cv2.THRESH_BINARY)
        medida_area = cv2.countNonZero(thresh_roi)

        # Calcular o volume da boia com base na área medida
        # (supondo que as boias são esféricas)
        raio = np.sqrt(medida_area/Area_da_circunferencia)
        volume = (4/3)*np.pi*raio**3

        # Exibir o resultado
        print('O volume da boia é: ', volume)
        
                # Salvar o resultado em um arquivo de texto
        with open('resultados.txt', 'a') as f:
            f.write(f'{nome_arquivo}: {volume}\n')
