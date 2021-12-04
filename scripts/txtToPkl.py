from os import system
import pickle
import pprint
from os import path

imgsPath = './imgs/'
extension = '.jpg'
dataFile = './data.pkl'
realFile = './descricoes.txt'
fakeFile = './fake.txt'

with open(realFile, 'r', encoding='latin-1') as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]

obj = {}

print(len(lines))

myi = 0
for index in range(540):

    obj[lines[myi]] = {
        "name": lines[myi],
        "img_path": imgsPath+lines[myi]+extension,
        "disc1": lines[myi+1],
        "disc2": lines[myi+2],
        "disc3": lines[myi+3],
    }
    if path.exists(imgsPath+lines[myi]+extension) == False:
        print(f'Não existe: {imgsPath+lines[myi]+extension}')
    myi += 4

    # pprint.pprint(obj)
    # with open("data.pkl", "wb") as f:
    #    pickle.dump(obj, f)
    # f.close()
