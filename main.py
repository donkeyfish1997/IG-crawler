from api.ig import *
from api.get import *
import os,sys
# 把登入狀態下的cookies資訊寫入 main.py 的變數cookies 中
cookies={
         
     }



if __name__ == '__main__':
    keyword = sys.argv[1]
    page = int(sys.argv[2])
    path = '/'
    if not os.path.isdir(keyword):
     os.mkdir(keyword)
     
    
   
    
    imgs = getIgImgsByNameAndPages(keyword,page)
    downloadImgsByImgs(imgs,keyword)

