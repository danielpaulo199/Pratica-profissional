from os import system, path, listdir
import re
import pickle
from createPDF import createPDF

#importar as cores depois
#adicionar fundos
#R$ ser desenhado por uma conta que adiciona mais por length do preço
# Bug = na hora de selecionar produtos no autocomplete se colocar letra crasha
#selecionar BG caso não encontre?
class NiceDoDia:
    def __init__(self):
        self.itensFile = "data.pkl"
        self.productAmmount = 0
        self.PDFsavepath = path.join('./PDFs/')
        self.BGsavepath = './fundos'
        #Dict que vai conter as variaveis para gerar o pdf
        self.newOfferDict = {
            "products" : [],
            "prices" : [],
            "PDFsavepath" : self.PDFsavepath
            #background
            
        }

    def mainMenu(self):
        ans=True
        while ans:
            system("cls")
            print ("""
            ------ NICE DO DIA ------

            1.Gerar Oferta
            2.Alterar imagem de fundo
            3.Adicionar novas imagens de fundo
            4.Adicionar produtos
            5.Editar produto
            6.Sair
            """)
            ans= input("Escolha uma opção: ") 
            if ans=="1": 
                system('cls')
                self.createOffer()
            elif ans=="2":
                system('cls')
                self.testefile()
            elif ans=="3":
                exit()
            elif ans !="":
                wait = input('\n Opção Invalida, tente novamente')
                system('cls')

    def getProductAmmountInput(self):
        while 1:
            self.productAmmount = input("Digite a quantidade de itens (Máximo 4): ").strip()
            if re.match(r'^[1-4]+$', self.productAmmount):
                if int(self.productAmmount) <= 4 and int(self.productAmmount) > 0:
                    break
            print('Quantidade não pode conter: ', re.findall(r'[^1-4]', self.productAmmount))
            print('Tente novamente: ')

    def getProductsInput(self):
        inputOrder = ['primeiro', 'segundo', 'terceiro', 'quarto']

        while len(self.newOfferDict['products']) < int(self.productAmmount):
            system("cls")
            product = str(input("Digite o {order} produto: ".format(order=inputOrder[len(self.newOfferDict['products'])])))

            validated_product = self.handleProductsInput(product)
            
            if validated_product != None:
                self.newOfferDict['products'].append(validated_product)
                self.getAndHandlePrices()               

    def getAndHandlePrices(self):
        array_possition = int(len(self.newOfferDict['products']) - 1)
        while 1:
            print("Digite o preço para: ", self.newOfferDict['products'][array_possition]["name"])
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
        with open(self.itensFile,"rb") as f:
            data = pickle.load(f)
            f.close()

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

        while 1:
            option = int(input("Digite a opção: "))

            if option >= 1 and option < len(matches):
                return data[matches[option]]

            if option == 0: 
                return

            print("Opção invalida")

    def setBGimage(self):
        default = str(self.BGsavepath+'/Default.jpg')
        #Seta o background para padrão 
        if path.exists(default): self.newOfferDict['background'] = default
        else:#caso não encontre o default 
            backgrounds = listdir(self.BGsavepath)
            self.newOfferDict['background'] = str(self.BGsavepath+'/'+backgrounds[0]) #usa o primeiro que encontar no diretorio
        

    def createOffer(self):
        self.getProductAmmountInput()
        self.getProductsInput()
        self.setBGimage()
        self.createPDFfile()

    def testefile(self):

        self.newOfferDict = {'products': [{'name': 'abacaxi tropical unidade', 'img_path': './imgs/abacaxi tropical und.jpg', 'disc1': 'abacaxi tropicalasbas', 'disc2': 'gostozo d+', 'disc3': 'und'},{'name': 'abacaxi tropical unidade', 'img_path': './imgs/abacaxi tropical und.jpg', 'disc1': 'abacaxi tropical', 'disc2': 'gostozo d+', 'disc3': 'und'}, {'name': 'abacaxi tropical unidade', 'img_path': './imgs/abacaxi tropical und.jpg', 'disc1': 'abacaxi tropical', 'disc2': 'gostozo d+', 'disc3': 'und'}], 'prices': ['1,00', '1,00'], 'PDFsavepath': './PDFs/', 'background': './fundos/Default.jpg'}

        PDFfile = createPDF(self.newOfferDict)
        PDFfile.initPDFfile()

    def createPDFfile(self):

        PDFfile = createPDF(self.newOfferDict)
        PDFfile.initPDFfile()
        system("pause")

if __name__ == "__main__":
    app = NiceDoDia()
    app.mainMenu()

