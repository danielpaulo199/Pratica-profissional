import os
from datetime import date, datetime
from platform import system
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


class createPDF:
    def __init__(self, newOffer):
        self.date = datetime.today().strftime("%d-%m-%Y")
        self.savepath = newOffer["PDFsavepath"]
        self.products = newOffer["products"]
        self.prices = newOffer["prices"]
        self.background = newOffer["background"]

    def initPDFfile(self):

        # Atribui nome e titulo ao arquivo PDF
        PDFname = self.setPDFname()
        pdf = canvas.Canvas(self.savepath + "/" + PDFname)
        pdf.setTitle(PDFname)

        # Desenhas os objetos no PDF
        self.drawProductsImages(pdf)
        self.drawCenterLines(pdf)
        self.drawDescriptions(pdf)
        self.drawPrices(pdf)
        self.drawExpirationDate(pdf)
        pdf.save()

        # Abre o arquivo automaticamente após criado
        os.startfile(self.savepath + "\\" + PDFname)

    def setPDFname(self):

        # Chega se existe copias para renomear
        copies = []
        existentes = os.listdir(self.savepath)
        for file in existentes:
            if self.date in file:
                copies.append(file)

        if len(copies) == 0:
            return str("Boa do Dia " + self.date + ".pdf")
        else:
            return str(
                "Boa do Dia " + self.date + " (" + str(len(copies)) + ")" + ".pdf"
            )

    def drawProductsImages(self, pdf):
        # variavel para controlar o array
        productAmmount = str(len(self.products))

        # desenha o background
        try:
            pdf.drawInlineImage(self.background, 0, 0)
        except:
            print(
                "ATENÇÃO: Não existem imagens de fundo cadastradas, o fundo fica em branco.\n"
            )
            os.system("pause")
            os.system("cls")

        imgCoordinates = {
            "1": {"x": [100], "y": [300], "width": 388, "height": 272},
            "2": {"x": [50, 300], "y": [380, 125]},
            "3": {"x": [50, 35, 315], "y": [380, 160, 160]},
            "4": {"x": [35, 315, 35, 315], "y": [415, 415, 160, 160]},
        }

        for index in range(0, len(self.products)):
            pdf.drawImage(
                self.products[index]["img_path"],
                imgCoordinates[productAmmount]["x"][index],
                imgCoordinates[productAmmount]["y"][index],
                width=imgCoordinates.get(productAmmount, {}).get("width", 238),
                height=imgCoordinates.get(productAmmount, {}).get("height", 167),
            )

    def drawCenterLines(self, pdf):
        # Desenha as linhas para separar os produtos
        pdf.setStrokeColorRGB(0.91796875, 0.421875, 0.08203125)  # laranja

        if len(self.products) == 2:
            pdf.line(24, 325, 571, 325)

        if len(self.products) > 2:
            pdf.line(24, 333, 571, 333)
            pdf.line(290, 65, 290, 333)

            if len(self.products) == 4:
                pdf.line(290, 330, 290, 591)

    def drawDescriptions(self, pdf):
        try:
            pdfmetrics.registerFont(TTFont("Algebrian Regular", "ALGER.ttf"))
            pdf.setFont("Algebrian Regular", 20)
        except:
            pdfmetrics.registerFont(TTFont("Calibri", "calibrib.ttf"))
            pdf.setFont("Calibri", 20)

        pdf.setFillColorRGB(0, 0.4375, 0.75)  # Azul claro

        productAmmount = str(len(self.products))

        descCoordinates = {  # Coordenadas das descrições
            "1": {"x": [65], "y": [240], "lineHeight": [0, 35, 70]},
            "2": {"x": [300, 35], "y": [530, 270], "lineHeight": [0, 24, 48]},
            "3": {"x": [300, 35, 300], "y": [530, 140, 140], "lineHeight": [0, 24, 48]},
            "4": {
                "x": [35, 300, 35, 300],
                "y": [395, 395, 140, 140],
                "lineHeight": [0, 24, 48],
            },
        }

        if len(self.products) == 1:
            pdf.setFontSize(35)

        # Loop para descrição de cada produto
        for index in range(0, len(self.products)):
            # Desenha as 3 linhas de descrição
            for line in range(0, 3):

                # Draw Strings de descrição
                pdf.drawString(
                    descCoordinates[productAmmount]["x"][index],
                    descCoordinates[productAmmount]["y"][index]
                    - descCoordinates[productAmmount]["lineHeight"][line],
                    self.products[index]["disc" + str(line + 1)],
                )

    def drawPrices(self, pdf):
        pdf.setFillColorRGB(0.91796875, 0.421875, 0.08203125)  # Laranja
        pdf.setFont("Calibri", 20)

        # Total de produtos em string para chamar as chaves do dicionario
        productAmmount = str(len(self.products))

        # coordenadas base onde iniciara os decimais
        priceCoordinates = {
            "1": {"x": [470], "y": [120]},
            "2": {"x": [470, 210], "y": [360, 100]},
            "3": {"x": [470, 250, 530], "y": [360, 75, 75]},
            "4": {"x": [250, 530, 250, 530], "y": [340, 340, 75, 75]},
        }

        # String fixa para desenha o R$
        dolarSignString = "R$"
        dolarSignFont = 20

        for index in range(0, len(self.products)):

            # define as strings a serem desenhadas
            numeralString = self.prices[index].split(",")[0]
            decimalString = "," + self.prices[index].split(",")[1]

            # Define o tanho da fonte para as string
            numeralFont, decimalFont = self.getPriceFontSize(numeralString, index)

            # Define as coordenadas base
            x = priceCoordinates[productAmmount]["x"][index]
            y = priceCoordinates[productAmmount]["y"][index]

            # Desenha os decimais
            pdf.setFontSize(decimalFont)
            pdf.drawString(x, y, decimalString)

            # Calcula a proxima coordenada com base no tamanho da passada
            nextCoordinate = x - int(
                pdfmetrics.stringWidth(numeralString, "Calibri", numeralFont)
            )

            # Desenha o Numeral
            pdf.setFontSize(numeralFont)
            pdf.drawString(nextCoordinate, y, numeralString)

            # Calcula a proxima coordenada com base no tamanho da passada
            nextCoordinate -= pdfmetrics.stringWidth(
                dolarSignString, "Calibri", dolarSignFont
            )

            # Desenha o R$
            pdf.setFontSize(dolarSignFont)
            pdf.drawString(nextCoordinate, y, dolarSignString)

    def getPriceFontSize(self, numeralString, index):
        if len(self.products) == 1:
            numeralFont = 114
            decimalFont = 50

        if len(self.products) == 2:
            numeralFont = 114
            decimalFont = 50

            if len(numeralString) > 2:
                numeralFont = 90
                decimalFont = 45

        # Caso até 3 produtos
        if len(self.products) == 3:
            if index == 0:
                numeralFont = 114
                decimalFont = 50

                if len(numeralString) > 2:
                    numeralFont = 90
                    decimalFont = 45
            else:
                numeralFont = 60
                decimalFont = 30

                if len(numeralString) >= 2:
                    numeralFont = 45
                    decimalFont = 25

        # Caso 4 produtos
        if len(self.products) == 4:
            numeralFont = 60
            decimalFont = 30

            if len(numeralString) >= 2:
                numeralFont = 45
                decimalFont = 25

        return numeralFont, decimalFont

    def drawExpirationDate(self, pdf):
        expDate = str(date.today().strftime("%d/%m/%Y"))
        pdf.setFillColorRGB(1, 1, 1)
        pdf.setFontSize(24)
        pdf.drawString(120, 630, expDate)
