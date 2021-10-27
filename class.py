from os import system, path, listdir
import re
import pickle
from createPDF import createPDF
import tkinter as tk
from tkinter import filedialog
from shutil import copyfile

# adicionar fundos
# Bug = na hora de selecionar produtos no autocomplete se colocar letra crasha


class NiceDoDia:
    def __init__(self):
        self.itensFile = "data.pkl"
        self.productAmmount = 0
        self.PDFsavepath = path.join('./PDFs/')
        self.BGsavepath = './fundos'
        self.background = self.BGsavepath+'/Default.jpg'
        # Dict que vai conter as variaveis para gerar o pdf
        self.newOfferDict = {
            "products": [],
            "prices": [],
            "PDFsavepath": self.PDFsavepath,
            "background": self.background
        }

    def mainMenu(self):
        ans = True
        while ans:
            system("cls")
            print("""
            ------ NICE DO DIA ------

            1.Gerar Oferta
            2.Alterar imagem de fundo
            3.Adicionar novas imagens de fundo
            4.Adicionar produtos
            5.Editar produto
            6.Sair
            """)
            ans = input("Escolha uma opção: ")
            if ans == "1":
                system('cls')
                self.createOffer()
            elif ans == "2":
                system('cls')
                self.setBgImage()
            elif ans == "3":
                system('cls')
                self.addBackgrouds()
            elif ans == "4":
                system('cls')
                self.payloadPDF()
            elif ans == "6":
                exit()
            elif ans != "":
                wait = input('\n Opção Invalida, tente novamente')
                system('cls')

    def getProductAmmountInput(self):
        while 1:
            self.productAmmount = input(
                "Digite a quantidade de itens (Máximo 4): ").strip()
            if re.match(r'^[1-4]+$', self.productAmmount):
                if int(self.productAmmount) <= 4 and int(self.productAmmount) > 0:
                    break
            print('Quantidade não pode conter: ',
                  re.findall(r'[^1-4]', self.productAmmount))
            print('Tente novamente: ')

    def getProductsInput(self):
        inputOrder = ['primeiro', 'segundo', 'terceiro', 'quarto']

        while len(self.newOfferDict['products']) < int(self.productAmmount):
            system("cls")
            product = str(input("Digite o {order} produto: ".format(
                order=inputOrder[len(self.newOfferDict['products'])])))

            validated_product = self.handleProductsInput(product)

            if validated_product != None:
                self.newOfferDict['products'].append(validated_product)
                self.getAndHandlePrices()

    def getAndHandlePrices(self):
        array_possition = int(len(self.newOfferDict['products']) - 1)
        while 1:
            print("Digite o preço para: ",
                  self.newOfferDict['products'][array_possition]["name"])
            price = input().strip()
            if len(price) < 7 and re.match(r'^[0-9,]+$', price):
                break
            print('Preço não pode conter: ', re.findall(r'[^0-9,]', price))
            print('Tente novamente: ')

        if len(price) > 3 and price.find(',') == -1:
            price = price[:3]
            decimal = '00'

        if len(price) <= 3 and price.find(',') == -1:
            decimal = '00'

        if price.find(',') != -1:
            separa = price.split(',')
            price = separa[0][:3]

            if len(separa[1]) >= 2:
                decimal = separa[1][:2]
            if len(separa[1]) == 1:
                decimal = separa[1] + '0'
            if len(separa[1]) == 0:
                decimal = '00'

        self.newOfferDict['prices'].append(str(price+","+decimal))

    def handleProductsInput(self, product):
        with open(self.itensFile, "rb") as f:
            data = pickle.load(f)
            f.close()

        matches = ["Cancelar"]
        for find in data:
            if product in find and find[0] != "#":
                matches.append(find)

        if len(matches) <= 1:
            print("\n   Produto não encontrado!")
            system("pause")
            return

        print('Selecione o Produto: "{0}"\n'.format(product))
        for index, name in enumerate(matches):
            print("{0}: {1}".format(index, name))
        print("\n0: Cancelar\n")

        while 1:
            option = int(input("Digite a opção: "))

            if option >= 1 and option < len(matches):
                return data[matches[option]]

            if option == 0:
                return

            print("Opção invalida")

    def setDefaultBGimage(self):

        if path.exists(self.newOfferDict['background']):
            return

        default = self.BGsavepath+'/Default.jpg'
        # Seta o background para padrão
        if path.exists(default):
            self.newOfferDict['background'] = default
        else:  # caso não encontre o default
            backgrounds = listdir(self.BGsavepath)
            # usa o primeiro que encontar no diretorio
            self.newOfferDict['background'] = self.BGsavepath + \
                '/'+backgrounds[0]

    def setBgImage(self):
        with open(self.itensFile, "rb") as f:
            data = pickle.load(f)
            f.close()

        # hashtag é o sufixo dos backgrounds , ja q o input de produto não aceita # ele so sera mostrado aqui
        backgrounds = "#"

        matches = [".Cancelar"]
        for find in data:
            if backgrounds in find:
                matches.append(find)

        if len(matches) <= 1:
            print("\n Não ha imagens de fundo cadastradas!")
            system("pause")
            return

        print("Selecione a imagem de fundo: \n")
        for index, name in enumerate(matches):
            print("{0}: {1}".format(index, name[1:]))
        print("\n0: Cancelar\n")

        while 1:
            option = int(input("Digite a opção: "))

            if option >= 1 and option < len(matches):
                selectedBg = matches[option]
                self.newOfferDict['background'] = data[selectedBg]['img_path']
                break

            if option == 0:
                return

            print("Opção invalida!")

        print("\n Imagem de fundo definida com sucesso! \n")
        system('pause')

    def createOffer(self):
        # Chama os métodos para receber os inputs
        self.getProductAmmountInput()
        self.getProductsInput()
        # Define o background
        self.setDefaultBGimage()
        # Método para instanciar e criar novo PDF
        self.createPDFfile()

    def payloadPDF(self):

        self.newOfferDict = {'products': [{'name': 'abacaxi tropical unidade', 'img_path': './imgs/abacaxi tropical und.jpg', 'disc1': 'abacaxi tropical',
                                           'disc2': 'gostozo d+', 'disc3': 'und'}], 'prices': ['222,00'], 'PDFsavepath': './PDFs/', 'background': './fundos/Default.jpg'}

        PDFfile = createPDF(self.newOfferDict)
        PDFfile.initPDFfile()

    def createPDFfile(self):

        PDFfile = createPDF(self.newOfferDict)
        PDFfile.initPDFfile()

        # Deleta a instacia da classe de geração de PDF
        del PDFfile
        # Zera os valores da oferta
        self.newOfferDict = {
            "products": [],
            "prices": [],
            "PDFsavepath": self.PDFsavepath}

        system("pause")

    def addBackgrouds(self):
        root = tk.Tk()
        root.withdraw()

        print("Selecione uma imagem...")
        selectedFile = filedialog.askopenfilename(
            initialdir="/", title="Selecione uma imagem", filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png")))

        if selectedFile == "":
            print("\nNenhuma imagem selecionada!")
            system("pause")
            return

        # Pega a extensão do arquivo para salvar dnv
        extension = selectedFile[-4:]

        # input que define o novo nome do fundo
        while 1:
            name = input("Digite o nome da imagem de fundo: ").strip()
            if len(name) >= 1 and re.match(r'^[A-Za-z0-9_-]*$', name):
                break
            print('Nome do arquivo não pode conter: ',
                  re.findall(r'[^A-Za-z0-9_-]', name))
            print('\nTente novamente: ')

        # Copia a imagem selecionada para a pasta de fundos
        savepath = self.BGsavepath+'/'+name+extension
        copyfile(selectedFile, savepath)

        # ADD= colocar o novo bg no arquivo local com # no prefixo

        # para a liste
        # newBackground = "#"+name


if __name__ == "__main__":
    app = NiceDoDia()
    app.mainMenu()
