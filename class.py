from os import system, path, listdir, makedirs, chmod, stat, remove
import re
import pickle
from createPDF import createPDF
import tkinter as tk
from tkinter import filedialog
from shutil import copyfile
from datetime import date, datetime

# adicionar fundos
# Bug = na hora de selecionar produtos no autocomplete se colocar letra crasha


class NiceDoDia:
    def __init__(self):
        self.itensFile = "data.pkl"
        self.productAmmount = 0
        self.imgSavepath = './imgs'
        self.PDFsavepath = path.join(
            './PDFs/' + datetime.today().strftime('%m-%Y'))
        self.BGsavepath = './fundos'
        self.background = ''
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
            7.Paylod (testes)
            """)
            ans = input("Escolha uma opção: ")
            if ans == "1":
                system('cls')
                self.createOffer()
            elif ans == "2":
                system('cls')
                self.selectBackground()
            elif ans == "3":
                system('cls')
                self.addBackgrouds()
            elif ans == "4":
                system('cls')
                self.addProducts()
            elif ans == "5":
                system('cls')
                self.editProducts()
            elif ans == "6":
                exit()
            elif ans == "7":
                self.payloadPDF()
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
            try:
                data = pickle.load(f)
                f.close()
            except:
                print("Não existem produtos cadastrados!")
                system("pause")
                self.mainMenu()

        matches = ["Cancelar"]
        for find in data:
            if product in find:
                matches.append(find)

        if len(matches) <= 1:
            print("\n   Produto não encontrado!")
            system("pause")
            return

        print('Selecione o Produto: "{0}"\n'.format(product))
        for index, name in enumerate(matches):
            print("{0}: {1}".format(index, name))
        print("\n0: Cancelar\n")

        while True:
            option = int(input("Digite a opção: "))

            if option >= 1 and option < len(matches):
                return data[matches[option]]

            if option == 0:
                return

            print("Opção invalida")

    def checkBackgroundImage(self):

        # Caso a imagen de fundo selecionado exista retorna
        if path.exists(self.newOfferDict['background']):
            return

        # caso a imagem selecionada não existe coloca uma padrão
        default = self.BGsavepath+'/Default.jpg'
        # Seta o background para padrão
        if path.exists(default):
            self.newOfferDict['background'] = default
        else:  # caso não encontre o default
            backgrounds = listdir(self.BGsavepath)

            if len(backgrounds) == 0:
                return
            # usa o primeiro que encontar no diretorio
            self.newOfferDict['background'] = self.BGsavepath + \
                '/'+backgrounds[0]

    def createOffer(self):
        # Chama os métodos para receber os inputs
        self.getProductAmmountInput()
        self.getProductsInput()
        # Define o background
        self.checkBackgroundImage()
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
        # seleciona a imagem
        selectedFile, extension = self.selectFiles()

        # caso nada for selceionado cancela a operação
        if selectedFile == "":
            print("\nNenhuma imagem selecionada!")
            system("pause")
            return

        # Aplica o nome do arquivo com o padrão de nome do windowns
        name = self.handleFileName("Digite o nome para a imagem de fundo: ")

        # Chega se a pasta de destino existe
        self.checkAndCreateFolders()

        # Copia a imagem selecionada para a pasta de fundos
        savepath = self.BGsavepath+'/'+name+extension
        copyfile(selectedFile, savepath)
        print("\nImagem de fundo adicionada com sucesso!\n")
        system("pause")

    def selectBackground(self):

        print("Imagens de fundo:\n")
        # Recupera todas as imagens de fundo encontradas
        backgrounds = listdir(self.BGsavepath)
        backgrounds.insert(0, 'Cancelar....')

        # caso não existam imagens de fundo volta ao menu
        if len(backgrounds) <= 1:
            print("Não existem imagens de fundo cadastradas\n")
            system("pause")
            return

        # Lista para o usuario
        print("Selecione a imagem de fundo: \n")
        for index, name in enumerate(backgrounds):
            print("{0}: {1}".format(index, name[:-4]))
        print("\n0: Cancelar\n")

        while True:
            option = int(input("Digite a opção: "))

            if option >= 1 and option < len(backgrounds):
                selectedBg = backgrounds[option]
                self.newOfferDict['background'] = self.BGsavepath + \
                    '/'+backgrounds[option]
                break

            if option == 0:
                return

            print("Opção invalida!")

        print("\n Imagem de fundo definida com sucesso! \n")
        system('pause')

    def checkAndCreateFolders(self):
        # cria o arquivo local para salvar os itens caso nao exista
        if path.isfile(self.itensFile) == False:
            file = open(self.itensFile, "a+")
            file.close()

        # Cria e da permisão para os dirétorio locais caso não existam
        if not path.isdir(self.BGsavepath):
            makedirs(self.BGsavepath)
            chmod(self.BGsavepath, stat.S_IWRITE)

        if not path.isdir(self.imgSavepath):
            makedirs(self.imgSavepath)
            chmod(self.imgSavepath, stat.S_IWRITE)

        if not path.isdir(self.PDFsavepath):
            makedirs(self.PDFsavepath)
            chmod(self.PDFsavepath, stat.S_IWRITE)

    def addProducts(self):
        displatText = ['primeira', 'segunda', 'terceira']

        # seleciona a imagem
        selectedFile, extension = self.selectFiles()

        # caso nada for selceionado cancela a operação
        if selectedFile == "":
            print("\nNenhuma imagem selecionada!")
            system("pause")
            return

        # Aplica o nome do arquivo com o padrão de nome do windowns
        name = self.handleFileName("Digite o nome completo do novo produto: ")

        # caminho da nova imagem
        savepath = self.imgSavepath+'/'+name+extension

        # loop para inserir as linhas de descrição dos produtos
        system('cls')
        print("OS PRODUTOS DEVEM TER 3 LINHAS DE DESCRIÇÃO.\n")
        descriptions = []
        for index in range(3):
            description = input(
                "Digite a "+displatText[index]+" linha da descrição:")
            descriptions.append(description)

        # Salva os registros no arquivo local
        with open("data.pkl", "rb+") as f:
            try:
                data = pickle.load(f)
            except:
                data = {}

            data[name] = {
                "name": name,
                "img_path": savepath,
                "disc1": descriptions[0],
                "disc2": descriptions[1],
                "disc3": descriptions[2]
            }

        with open("data.pkl", "wb") as f:
            pickle.dump(data, f)
            f.close()

        # Copia nova imagem para a pasta local
        copyfile(selectedFile, savepath)

        system('cls')
        print('Produto "{0}" adicionado com sucesso!'.format(name))
        system("pause")

    def selectFiles(self):
        # Cria uma janela de interface para renderizar o explorer de arquivos
        root = tk.Tk()
        # Faz a janela fica quase invisivel ao usuario para apenas mostrar o explorer
        root.overrideredirect(True)
        root.geometry('0x0+0+0')

        print("Selecione uma imagem...")
        root.focus_force()

        selectedFile = filedialog.askopenfilename(
            initialdir="/", title="Selecione uma imagem", filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png")))

        # pega a extensão do arquivo selecionado
        extension = selectedFile[-4:]
        # Destroi a janela apos o uso
        root.withdraw()
        root.destroy()

        return selectedFile, extension

    def editProducts(self):

        product = self.getAndlistProducts(
            "Digite o produto que deseja editar: ")

        if product == None:
            return

        # nome antigo
        oldName = product['name']

        editName = self.yesNoquestion("Deseja editar o nome do produto? ")
        if editName == 'y':
            product = self.handleNameEdit(product)

        editImage = self.yesNoquestion("Deseja editar a imagem do produto? ")
        if editImage == 'y':
            product = self.handleImageEdit(product)

        editDescription = self.yesNoquestion(
            "Deseja editar a descrição do produto? ")
        if editDescription == 'y':
            product = self.handleDescriptionsEdit(product)

        # Ápos feita a edição deleta o objeto antigo e salva o novo
        with open("data.pkl", "rb") as f:
            data = pickle.load(f)

        del data[oldName]

        data[product['name']] = {
            "name": product['name'],
            "img_path": product['img_path'],
            "disc1": product['disc1'],
            "disc2": product['disc2'],
            "disc3": product['disc3']
        }

        with open("data.pkl", "wb") as f:
            pickle.dump(data, f)
            f.close()

        print("Produto editado com sucesso!")
        system("pause")

    def yesNoquestion(self, question):
        while True:
            system('cls')
            option = input(question+" (Y/n):")
            if option == 'Y' or option == 'y':
                system('cls')
                return 'y'
            elif option == 'n' or option == 'N':
                system('cls')
                return 'n'

    def handleImageEdit(self, product):
        # seleciona a nova imagem
        selectedFile, extension = self.selectFiles()

        if selectedFile == "":
            print("\nNenhuma imagem selecionada!")
            system("pause")
            return

        # pega o nome da imagem selecionada
        name = product['name']

        # caminho da nova imagem
        savepath = self.imgSavepath+'/'+name+extension

        try:
            remove(product['img_path'])
        except:
            pass

        copyfile(selectedFile, savepath)

        # update no objeto
        product['img_path'] = savepath

        print("Imagem editada com sucesso!\n")
        system("pause")

        return product

    def handleFileName(self, inputLabel):
        # Aplica o nome do arquivo com o padrão de nome do windowns
        while 1:
            name = input(inputLabel).strip()
            if len(name) >= 1 and re.match(r'^[ A-Za-z0-9_-]*$', name):
                break
            print('Nome do arquivo não pode conter: ',
                  re.findall(r'[^ A-Za-z0-9_-]', name))
            print('\nTente novamente: ')

        return name

    def handleNameEdit(self, product):
        name = self.handleFileName(
            'Digite o novo nome para o produto "{0}":\n'.format(product['name']))

        product['name'] = name

        print("Nome do arquivo editado com sucesso!")
        system("pause")

        return product

    def handleDescriptionsEdit(self, product):
        displatText = ['primeira', 'segunda', 'terceira']
        disc = ['disc1', 'disc2', 'disc3']

        # loop para inserir as linhas de descrição dos produtos
        system('cls')
        print("OS PRODUTOS DEVEM TER 3 LINHAS DE DESCRIÇÃO.\n")
        descriptions = []
        for index in range(3):
            description = input(
                "Digite a "+displatText[index]+" linha da descrição:")
            descriptions.append(description)

        for index in range(3):
            product[disc[index]] = descriptions[index]

        return product

    def getAndlistProducts(self, inputLabel):

        userInput = input(inputLabel)

        with open(self.itensFile, "rb") as f:
            try:
                data = pickle.load(f)
            except:
                print("Não existem produtos cadastrados!")
                system("pause")
                return

        matches = ["Cancelar"]
        for find in data:
            if userInput in find:
                matches.append(find)

        if len(matches) <= 1:
            print("\n   Produto não encontrado!")
            system("pause")
            return

        print('Selecione o Produto: "{0}"\n'.format(userInput))
        for index, name in enumerate(matches):
            print("{0}: {1}".format(index, name))
        print("\n0: Cancelar\n")

        while True:
            option = int(input("Digite a opção: "))

            if option >= 1 and option < len(matches):
                product = data[matches[option]]
                return product

            if option == 0:
                return

            print("Opção invalida")


if __name__ == "__main__":
    app = NiceDoDia()
    app.checkAndCreateFolders()
    app.mainMenu()
