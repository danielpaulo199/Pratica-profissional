import pickle
import pprint
import reportlab as pd


def searchPkl():

    with open("data.pkl", "rb") as f:
        dict = pickle.load(f)

    inputa = input("digita: ")

    matches = []
    for find in dict:
        if inputa in find:
            matches.append(find)

    print('Selecione o Produto: "{0}"'.format(inputa))
    for index, name in enumerate(matches):
        print("{0}: {1}".format(index, name))


def editpkl():
    with open("data.pkl", "rb") as f:
        dict = pickle.load(f)
        f.close()

    dict['abacaxi tropical unidade']['img_path'] = "./imgs/abacaxi tropical und.jpg"
    with open("data.pkl", "wb") as f:
        pickle.dump(dict, f)


def lerpkl():
    a_file = open("data.pkl", "rb")
    output = pickle.load(a_file)
    pprint.pprint(output)


def addToPkl():
    with open("data.pkl", "rb") as f:
        data = pickle.load(f)

    data["nescau 2.0 radical 200g"] = {
        "name": "nescau 2.0 radical 200g",
        "img_path": "caminho do nescau",
        "disc1": "nescau 2.0",
        "disc2": "gostozo d+",
        "disc3": "200g"
    }

    with open("data.pkl", "wb") as f:
        pickle.dump(data, f)


def addBG():
    with open("data.pkl", "rb") as f:
        obj = pickle.load(f)

    obj["#Red Background"] = {
        "name": "Red Background",
        "img_path": "./fundos/Red Background.jpg"
    }

    with open("data.pkl", "wb") as f:
        pickle.dump(obj, f)


def dellPkl():
    with open("data.pkl", "rb") as f:
        obj = pickle.load(f)
        f.close()
    del obj['#Green Background']
    with open("data.pkl", "wb") as f:
        pickle.dump(obj, f)


def testeMatch():
    a = input("Digit: ").isdigit()
    print(a)


lerpkl()


def dictadd():
    offerOBJ = {}

    offerOBJ['products'] = [{"prod1": "omo 1kg"}, {"prod2": "omo 2kg"}]
    print(type(offerOBJ))
    newobj = {"prod3": "omo 3kg"}
    offerOBJ['products'].append(newobj)
    offerOBJ['prices'] = [30, 10, 20]
    print(offerOBJ)


def versiona():
    print(pd.__version__)
