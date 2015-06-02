from PIL import Image
from downloadFile import download
import os

heightOne = 1024
weightOne = 1024
heightFull = heightOne*3+536
weightFull = weightOne*4+806
pageStart = 648 #854
pageEnd = 648#860
# pages = 100
pathToDirs = "./"
url = "http://192.114.7.88:2121/iipsrv?FIF=/operational_storage/derivative_copies/2014/06/26/file_3%d/V1-FL12997%d.ptif&JTL=6,%d"
tempFile = pathToDirs+'images/tempFile.jpg'

new_im = Image.new('RGB', (weightFull,heightFull))

index = 0
for page in range(pageStart,pageEnd):
    for i in range(0,4):
        for j in range(0,5):
            try:
                download(url % (((pageStart+index-30)/100-4),(pageStart+index),(i*5+j)),tempFile)
            except Exception as e:
                print "error in" + startUrl+str((pageStart+index-30)/100-4)+conUrl+str(pageStart+index)+endUrl+str(i*5+j)
                continue
            im=Image.open(tempFile)
            new_im.paste(im,(j*weightOne,i*heightOne))
    new_im.save(pathToDirs+'output/Epage'+str(index)+'.jpg')
    index+=1

os.remove(tempFile)
# new_im.show()
