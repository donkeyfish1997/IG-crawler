from api.ig import *
from api.get import *
import os,sys





if __name__ == '__main__':
    print(sys.argv)
    keyword = sys.argv[1]
    page = int(sys.argv[2])
    path = 'C:\\a'
    if not os.path.isdir(keyword):
     os.mkdir(keyword)
    
    imgs = getIgImgsByNameAndPages(keyword,page)
    downloadImgsByImgs(imgs,keyword)
