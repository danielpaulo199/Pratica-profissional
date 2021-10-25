import os
from datetime import datetime
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib import colors


class createPDF:
    def __init__(self, newOffer):
        self.date = datetime.today().strftime('%d-%m-%Y')
        self.savepath = os.path.join(
            newOffer['PDFsavepath'], datetime.today().strftime('%m-%Y'))
        self.products = newOffer['products']
        self.prices = newOffer['prices']
        self.background = newOffer['background']
        self.validity = newOffer.get(
            'validity', datetime.today().strftime('%d/%m/%Y'))

    def initPDFfile(self):
        # Cria o diretorio para salvar o PDF e cria o nome do arquivo
        self.checkAndCreatesavepath()

        # Atribui nome e titulo ao arquivo PDF
        PDFname = self.setPDFname()
        pdf = canvas.Canvas(self.savepath + '/' + PDFname)
        pdf.setTitle(PDFname)

        # Desenhas os objetos no PDF
        self.drawProductsImages(pdf)
       # AINDA EM DEV --  self.drawCenterLines(pdf)
        self.drawDescriptions(pdf)
        self.drawPrices(pdf)
        pdf.save()

        pdfmetrics.registerFont(TTFont('Calibri', 'calibrib.ttf'))

    def checkAndCreatesavepath(self):
        if not os.path.isdir(self.savepath):
            os.makedirs(self.savepath)

    def setPDFname(self):

        # Chega se existe copias para renomear
        copies = []
        existentes = os.listdir(self.savepath)
        for file in existentes:
            if self.date in file:
                copies.append(file)

        if len(copies) == 0:
            return str('Boa do Dia '+self.date+'.pdf')
        else:
            return str('Boa do Dia '+self.date+' ('+str(len(copies))+')'+'.pdf')

    def drawProductsImages(self, pdf):
        # variavel para controlar o array
        productAmmount = str(len(self.products))

        # desenha o background
        pdf.drawInlineImage(self.background, 0, 0)

        imgCoordinates = {
            "1": {
                "x": [100],
                "y": [300],
                "width": 388,
                "height": 272
            },
            "2": {
                "x": [50, 300],
                "y": [380, 125]
            },
            "3": {
                "x": [50, 35, 315],
                "y": [380, 160, 160]
            },
            "4": {
                "x": [35, 315, 35, 315],
                "y": [415, 415, 160, 160]
            }
        }

        for index in range(0, len(self.products)):
            pdf.drawImage(self.products[index]['img_path'],
                          imgCoordinates[productAmmount]['x'][index],
                          imgCoordinates[productAmmount]['y'][index],
                          width=imgCoordinates.get(
                              productAmmount, {}).get('width', 238),
                          height=imgCoordinates.get(productAmmount, {}).get('height', 167))

    def drawCenterLines(self, pdf):
        pass
        # SERA DESENVOLVIDO DEPOIS DAS DESCRIÇÕES E PREÇOS att.
        # canvas.line(x1,y1,x2,y2)
        # pdf.line(0,510,500,510)
        pdf.setStrokeColorRGB(0.91796875, 0.421875, 0.08203125)  # laranja
        pdf.line(24, 350, 571, 350)

    def drawDescriptions(self, pdf):
        pdfmetrics.registerFont(TTFont('Algebrian Regular', 'ALGER.ttf'))
        pdf.setFont("Algebrian Regular", 25)
        pdf.setFillColorRGB(0, 0.4375, 0.75)  # Azul claro

        productAmmount = (str(len(self.products)))

        descCoordinates = {  # Coordenadas das descrições
            "1": {
                "x": [65],
                "y": [240],
                "lineHeight": [0, 35, 70]
            },
            "2": {
                "x": [300, 35],
                "y": [530, 270],
                "lineHeight": [0, 24, 48]
            },
            "3": {
                "x": [300, 35, 300],
                "y": [530, 140, 140],
                "lineHeight": [0, 24, 48]
            },
            "4": {
                "x": [35, 300, 35, 300],
                "y": [395, 395, 140, 140],
                "lineHeight": [0, 24, 48]
            }
        }

        if len(self.products) == 1:
            pdf.setFontSize(35)

        # Loop para descrição de cada produto
        for index in range(0, len(self.products)):
            # Desenha as 3 linhas de descrição
            for line in range(0, 3):
                # Caso a linha da descrição seja maior de 18 caracteres diminui a fonte
                if len(self.products[index]['disc'+str(line+1)]) > 18:
                    pdf.setFontSize(20)

                # Draw Strings de descrição
                pdf.drawString(descCoordinates[productAmmount]['x'][index],
                               descCoordinates[productAmmount]['y'][index] -
                               descCoordinates[productAmmount]['lineHeight'][line],
                               self.products[index]['disc'+str(line+1)])

    def drawPrices(self, pdf):
        pdfmetrics.registerFont(TTFont('Calibri', 'calibrib.ttf'))
        pdf.setFont("Calibri", 30)
        pdf.setFillColorRGB(0.91796875, 0.421875, 0.08203125)  # Laranja

        pdf.drawString(300, 300, 'Hello world 3,99')

    def printar(self):
        print(self.savepath)
        print(self.products)
        print(self.prices)
