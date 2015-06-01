from PIL import Image
from downloadFile import download

heightOne = 1024
weightOne = 1024
heightFull = heightOne*3+536
weightFull = weightOne*4+806
# piecesH = heightFull/heightOne + 1
# piecesW = weightFull/weightOne + 1

path = '/home/eli/Workspace/Concatenator/images/test.jpg'
# im = Image.open('/home/eli/Workspace/Concatenator/images/test.jpg')

new_im = Image.new('RGB', (weightFull,heightFull))


startUrl = "http://192.114.7.88:2121/iipsrv?FIF=/operational_storage/derivative_copies/2014/06/26/file_3"
conUrl = "/V1-FL12997"
endUrl = ".ptif&JTL=6,"
pageStart = 661
index = 35
for page in range(0,190):
    for i in range(0,4):
        for j in range(0,5):
            print
            try:
                download(startUrl+str((pageStart+index-30)/100-4)+conUrl+str(pageStart+index)+endUrl+str(i*5+j),path)
            except Exception as e:
                print "error in" + startUrl+str((pageStart+index-30)/100-4)+conUrl+str(pageStart+index)+endUrl+str(i*5+j)
                break
            im=Image.open(path) #Image.eval(im,lambda x: x)
            #paste the image at location i,j:
            new_im.paste(im,(j*1024,i*1024))
    new_im.save('/home/eli/Workspace/Concatenator/output/page'+str(index)+'.jpg')
    index+=1


# new_im.show()
