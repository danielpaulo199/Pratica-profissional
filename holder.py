import subprocess
from shutil import copyfile
import os
import shutil
import stat

#subprocess.call(['chmod', '-R', '+w', './folder'])
copyfile("C:\\Users\\Jenifer\\Desktop\\pratica pro (Daniel)\\Nice-do-Dia-master\\top.txt", './folder/top.txt')
#os.chmod('./folder', stat.S_IWRITE)


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
