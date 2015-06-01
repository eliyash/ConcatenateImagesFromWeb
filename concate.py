from PIL import Image
from downloadFile import download

heightOne = 1024
weightOne = 1024
heightFull = heightOne*3+536
weightFull = weightOne*4+806
pageStart = 661
pages = 100
url = "http://192.114.7.88:2121/iipsrv?FIF=/operational_storage/derivative_copies/2014/06/26/file_3%d/V1-FL12997%d.ptif&JTL=6,%d"
tempFile = '/home/eli/Workspace/Concatenator/images/tempFile.jpg'


# im = Image.open('/home/eli/Workspace/Concatenator/images/test.jpg')

new_im = Image.new('RGB', (weightFull,heightFull))


index = 114
for page in range(0,pages):
    for i in range(0,4):
        for j in range(0,5):
            try:
                download(url % (((pageStart+index-30)/100-4),(pageStart+index),(i*5+j)),tempFile)
            except Exception as e:
                print "error in" + startUrl+str((pageStart+index-30)/100-4)+conUrl+str(pageStart+index)+endUrl+str(i*5+j)
                continue
            im=Image.open(tempFile) #Image.eval(im,lambda x: x)
            #paste the image at location i,j:
            new_im.paste(im,(j*weightOne,i*heightOne))
    new_im.save('/home/eli/Workspace/Concatenator/output/page'+str(index)+'.jpg')
    index+=1


# new_im.show()
