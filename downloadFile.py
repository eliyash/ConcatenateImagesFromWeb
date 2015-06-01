import urllib2



def download(url,path):
    request = urllib2.Request(url)
    request.add_header('User-agent', "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5." )
    
    opener = urllib2.build_opener()

    f = open(path, "wb")
    f.write(opener.open(request).read())
    f.close()


# url = "http://192.114.7.88:2121/iipsrv?FIF=/operational_storage/derivative_copies/2014/06/26/file_33/V1-FL12997820.ptif&JTL=6,1"
# path = '/home/eli/Workspace/Concatenator/images/test.jpg'
# download(url,path)
