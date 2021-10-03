import requests
import os
def downloadImgsByImgs(imgs, path='img'):
    os.makedirs(f'./{path}/', exist_ok=True)
    for i in range(len(imgs)):
        url = imgs[i]
        r = requests.get(url)
        with open(f'./{path}/{i}.jpg', 'wb') as f:
            f.write(r.content)
    pass