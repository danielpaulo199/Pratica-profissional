from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os
from os import path
import re
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import date
import time
import smtplib


## Variaveis globais
produtos = ['Primeiro', 'Segundo', 'Terceiro', 'Quarto']
totalProd = 0
contProd = 0  # Conta quantos produtos ja foram desenhados no arquivo PDF
versao = 'V-3.3'
# Lançado dia 23/11/2019



# FUNÇÕES
def inicio():
    global totalProd
    hoje = date.today()
    data = str(hoje.strftime("%d-%m-%Y"))
    nomeArquivo = str('Boa do Dia '+data+'.pdf')


    pdfmetrics.registerFont(TTFont('Calibri', 'calibrib.ttf'))
    pdfmetrics.registerFont(TTFont('Algebrian Regular', 'ALGER.ttf'))

    mesano = time.strftime('%m-%Y')
    savepath = os.path.join('/PDFs/', mesano)
    
    path = './PDFs/'+mesano
    existentes = [os.path.splitext(filename)[0] for filename in os.listdir(path)]


    name = nomeArquivo.split('.')


    if name[0] in existentes:
        print('ARQUIVO EXISTE')
        copias = []
        for find in existentes:
            if data in find:
                copias.append(find)

        numero_copias = []
        for copy in copias:
            try:
                separa = int(copy.split('(')[1][:1])
                numero_copias.append(separa)
            except:
                pass

        index = int(len(numero_copias))
        copia = index + 1
        nomeArquivo = str('Boa do Dia '+data+' ('+str(copia)+')'+'.pdf')
        
    else:
        pass

    try:
        os.makedirs(savepath)
    except:
        pass

    pdf = canvas.Canvas('/PDFs/' + mesano + '/' + nomeArquivo)
    pdf.setTitle(nomeArquivo)

    totalProd = input_quant()

    pdf.drawInlineImage('/fundos/fundo'+str(totalProd)+'iten.jpg', 0, 0)


    return nomeArquivo, mesano, pdf
def input_quant():

    while True:
        total = input("Insira a quantidade de produtos: ").strip()
        if re.match(r'^[1-4]+$', total):
            if int(total) <= 4 and int(total) > 0:
                break
        print('Quantidade não pode conter: ', re.findall(r'[^1-4]', total))
        print('Tente novamente: ')
    return int(total)

def input_image():
    global contProd
    global totalProd

    while int(contProd) != int(totalProd):

        produto = str(input("Digite o {prod} produto: ".format(prod = produtos[contProd])))

        while path.exists('/imgs/'+produto+'.jpg') == False:
            produto = auto_complete(produto)
            if produto == None:
                produto = str(input("Digite o {prod} produto: ".format(prod = produtos[contProd])))

        draw_image(produto)
        draw_desc(produto)
        input_preco(produto)
        contProd += 1


        


def auto_complete(produto):
    
    #prods = os.listdir('./imgs')
    path = '/imgs' 
    prods = [os.path.splitext(filename)[0] for filename in os.listdir(path)]


    produtos_filtrados = []
    for find in prods:
        if produto in find:
            produtos_filtrados.append(find)


    if len(produtos_filtrados) >= 1:
        # Deal with more that one team.
        print('Selecione o Produto: "{0}"'.format(produto))
        for index, name in enumerate(produtos_filtrados):
            print("{0}: {1}".format(index, name))

        while True:
            try:
                opc = int(input("Digita a opção: "))
                if opc >= 0 and opc < len(produtos_filtrados):
                    break
                print("Opção invalida")
            except:
                print("Opção invalida")

        img = produtos_filtrados[opc]
        img = str(img)
        produtos_filtrados = []
        return img


def draw_image(produto):
    
    if totalProd == 1:
        x=[100]
        y=[300]
        pdf.drawImage('/imgs/'+produto+'.jpg', x[contProd], y[contProd], width=388, height=272)

    if totalProd == 2:
        x = [50, 300]
        y = [380, 125]
        pdf.drawImage('/imgs/'+produto+'.jpg', x[contProd], y[contProd])

    if totalProd == 3:
        x = [50, 35, 315]
        y = [380, 160, 160]
        pdf.drawImage('/imgs/'+produto+'.jpg', x[contProd], y[contProd])

    if totalProd == 4:
        x = [35, 315, 35, 315]
        y = [415, 415, 160, 160]
        pdf.drawImage('/imgs/'+produto+'.jpg', x[contProd], y[contProd])

def draw_desc(produto):

    ## DATA DE VALIDADE
    hoje = date.today()
    validade = str(hoje.strftime("%d/%m/%Y"))
    pdf.setFillColorRGB(1, 1, 1)
    pdf.setFont("Calibri", 24)
    pdf.drawString(120, 630, validade)
    pdf.setFontSize(15)
    ## VERSÃO
    pdf.drawString(0, 0, versao)
    ##
    pdf.setFillColorRGB(0, 0.4375, 0.75)    # Azul
    pdf.setFont("Algebrian Regular", 20)

    l1, l2, l3 = search(produto+'\n')
    if totalProd == 1:
        x = 65
        y = 240
        pdf.setFontSize(35)
        pdf.drawString(x, y, l1)
        pdf.drawString(x, y-35, l2)
        pdf.drawString(x, y-70, l3)
    
    if totalProd == 2:
        x = [300, 35]
        y = [530, 270]
        pdf.setFontSize(25)
        pdf.drawString(x[contProd], y[contProd], l1)
        pdf.drawString(x[contProd], y[contProd]-24, l2)
        pdf.drawString(x[contProd], y[contProd]-48, l3)

    if totalProd == 3:
        x = [300, 35, 300]
        y = [530, 140, 140]
        if contProd == 0:
            if len(l1) > 18:
                pdf.setFontSize(20)
            else:
                pdf.setFontSize(25)
        else:
            pdf.setFontSize(20)
        pdf.drawString(x[contProd], y[contProd], l1)
        pdf.drawString(x[contProd], y[contProd]-24, l2)
        pdf.drawString(x[contProd], y[contProd]-48, l3)
        
    if totalProd == 4:
        x = [35, 300, 35, 300]
        y = [395, 395, 140, 140]
        pdf.drawString(x[contProd], y[contProd], l1)
        pdf.drawString(x[contProd], y[contProd]-24, l2)
        pdf.drawString(x[contProd], y[contProd]-48, l3)

def search(produto):
    with open("descricoes.txt", "r") as f:
        for line in f:
            linha = str(line)
            if linha == produto:
                l1 = f.readline()
                l2 = f.readline()
                l3 = f.readline()
                
                # Retira a quebra de linha das strings
                l1 = l1[:-1]
                l2 = l2[:-1]
                l3 = l3[:-1]
                return l1, l2, l3
    f.close()

def input_preco(produto):
    print("Digite o Preço para: ", produto)
    preco, decimal = valida_preco()
    clear()
    cordenada_preco(preco, decimal)

def valida_preco():
    while True:
        preco = input().strip()
        if len(preco) < 7 and re.match(r'^[0-9,]+$', preco):
            break
        print('Preço não pode conter: ', re.findall(r'[^0-9,]', preco))
        print('Tente novamente: ')
    
    if len(preco) > 3 and preco.find(',') == -1:
        preco = preco[:3]
        decimal = '00'
    
    if len(preco) <= 3 and preco.find(',') == -1:
        decimal = '00'

    if preco.find(',') != -1:
        separa = preco.split(',')
        preco = separa[0][:3]
        
        if len(separa[1]) >= 2:
            decimal = separa[1][:2]
        if len(separa[1]) == 1:
            decimal = separa[1] + '0'
        if len(separa[1]) == 0:
            decimal = '00'

    return preco, decimal

def cordenada_preco(preco, decimal):
    total1p1 = [120, 480, 470, 415, 385]
    total1p2 = [120, 480, 470, 360, 325]
    total1p3 = [120, 480, 470, 305, 270]

    total2cimp1 = [360, 480, 470, 415, 385]
    total2cimp2 = [360, 480, 470, 360, 325]
    total2cimp3 = [360, 480, 470, 330, 295]

    total2baip1 = [100, 220, 210, 155, 125]
    total2baip2 = [100, 220, 210, 100, 65]
    total2baip3 = [100, 220, 210, 70, 35]

    total4esqP1 = [340, 260, 255, 225, 203]
    total4esqP2 = [340, 260, 255, 210, 190]
    total4esqP3 = [340, 260, 255, 190, 170]

    total4dirP1 = [340, 535, 530, 500, 478]
    total4dirP2 = [340, 540, 535, 489, 466]
    total4dirP3 = [340, 540, 535, 465, 445] #433

    pdf.setFont("Calibri", 30)
    pdf.setFillColorRGB(0.91796875, 0.421875, 0.08203125) #Laranja

# desenha preco para 1 iten
    if totalProd == 1:
        if len(preco) == 1:
            draw_precos(total1p1, preco, decimal, 114, 50, 28)
        if len(preco) == 2:
            draw_precos(total1p2, preco, decimal, 114, 50, 28)
        if len(preco) > 2:
            draw_precos(total1p3, preco, decimal, 114, 50, 28)

    if totalProd == 2:
        if contProd == 0:
            if len(preco) == 1:
                draw_precos(total2cimp1, preco, decimal, 114, 50, 28)
            if len(preco) == 2:
                draw_precos(total2cimp2, preco, decimal, 114, 50, 28)
            if len(preco) > 2:
                draw_precos(total2cimp3, preco, decimal, 90, 45, 28)
        else:
            if len(preco) == 1:
                draw_precos(total2baip1, preco, decimal, 114, 50, 28)
            if len(preco) == 2:
                draw_precos(total2baip2, preco, decimal, 114, 50, 28)
            if len(preco) > 2:
                draw_precos(total2baip3, preco, decimal, 90, 45, 28)
    
    if totalProd == 3:
        if contProd == 0:
            if len(preco) == 1:
                draw_precos(total2cimp1, preco, decimal, 114, 50, 28)
            if len(preco) == 2:
                draw_precos(total2cimp2, preco, decimal, 114, 50, 28)
            if len(preco) > 2:
                draw_precos(total2cimp3, preco, decimal, 90, 45, 28)
        if contProd == 1:
            total4esqP1[0] = 75
            total4esqP2[0] = 75
            total4esqP3[0] = 75

            if len(preco) == 1:
                draw_precos(total4esqP1, preco, decimal, 60, 30, 20)
            if len(preco) == 2:
                draw_precos(total4esqP2, preco, decimal, 45, 25, 20)
            if len(preco) > 2:
                draw_precos(total4esqP3, preco, decimal, 45, 25, 20)

        if contProd == 2:
            total4dirP1[0] = 75
            total4dirP2[0] = 75
            total4dirP3[0] = 75

            if len(preco) == 1:
                draw_precos(total4dirP1, preco, decimal, 60, 30, 20)
            if len(preco) == 2:
                draw_precos(total4dirP2, preco, decimal, 45, 25, 20)
            if len(preco) > 2:
                draw_precos(total4dirP3, preco, decimal, 45, 25, 20)

#desenha preco para 4 itens
    if totalProd == 4:
        if contProd == 0 or contProd == 2:
            if contProd == 2:
                total4esqP1[0] = 75
                total4esqP2[0] = 75
                total4esqP3[0] = 75

            if len(preco) == 1:
                draw_precos(total4esqP1, preco, decimal, 60, 30, 20)
            if len(preco) == 2:
                draw_precos(total4esqP2, preco, decimal, 45, 25, 20)
            if len(preco) > 2:
                draw_precos(total4esqP3, preco, decimal, 45, 25, 20)
        
        if contProd == 1 or contProd == 3:
            if contProd == 3:
                total4dirP1[0] = 75
                total4dirP2[0] = 75
                total4dirP3[0] = 75

            if len(preco) == 1:
                draw_precos(total4dirP1, preco, decimal, 60, 30, 20)
            if len(preco) == 2:
                draw_precos(total4dirP2, preco, decimal, 45, 25, 20)
            if len(preco) > 2:
                draw_precos(total4dirP3, preco, decimal, 45, 25, 20)

def draw_precos(cords, preco, decimal, fonteMaior, fonteMenor, fonteRs):
    pdf.setFontSize(fonteRs)
    pdf.drawString(cords[4], cords[0], 'R$')
    pdf.setFontSize(fonteMenor)
    pdf.drawString(cords[1], cords[0], decimal)
    pdf.drawString(cords[2], cords[0], ',')
    pdf.setFontSize(fonteMaior)
    pdf.drawString(cords[3], cords[0], preco)

clear = lambda: os.system('cls')
## CALL STACK (MAIN)
nomeArquivo, mesano, pdf = inicio()

input_image()

pdf.save()

print("Arquivo gerado com sucesso! ", nomeArquivo)
os.startfile('\\PDFs\\' + mesano + '\\' + nomeArquivo)