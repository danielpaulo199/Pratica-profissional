import subprocess
from shutil import copyfile
import os
import shutil
import stat

# subprocess.call(['chmod', '-R', '+w', './folder'])
copyfile("C:\\Users\\Jenifer\\Desktop\\pratica pro (Daniel)\\Nice-do-Dia-master\\top.txt", './folder/top.txt')
# os.chmod('./folder', stat.S_IWRITE)


# abre o arquivo para salvar o novo nome
   with open("data.pkl", "rb") as f:
        data = pickle.load(f)
        f.close()

    data[name] = {
        "name": name,
        "img_path": product['img_path'],
        "disc1": product['disc1'],
        "disc2": product['disc2'],
        "disc3": product['disc3']
    }
    del data[product['name']]

    with open("data.pkl", "wb") as f:
        pickle.dump(data, f)


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
            try:
                option = int(input("Digite a opção: "))
            except:
                print("Digite apenas números.")

            if option >= 1 and option < len(matches):
                return data[matches[option]]

            if option == 0:
                return

            print("Opção invalida")