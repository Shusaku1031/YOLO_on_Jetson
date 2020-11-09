from urllib import request
import xml.etree.ElementTree as ET
import os

wnid = "n02783161"
dirpath = os.path.join("raw_images",wnid)

if os.path.isdir(dirpath) == False:
    os.mkdir(dirpath)

IMG_LIST_URL="http://www.image-net.org/api/text/imagenet.synset.geturls.getmapping?wnid={}"

url = IMG_LIST_URL.format(wnid)
with request.urlopen(url) as response:
    html = response.read()
    data = html.decode()
    data = data.split()
    fnames = data[::2]
    urls = data[1::2]

files = os.listdir(os.path.join("bbox","Annotation",wnid))

annotated_index = [fnames.index(f.split('.')[0]) for f in files]
print(annotated_index)

#fnameをannotated_indexに
#for i in range(len(fnames)):
for i in annotated_index:
    try:
        print("Found:",urls[i],fnames[i])
        with request.urlopen(urls[i]) as response:
            img = response.read()

        with open(os.path.join(dirpath,fnames[i]),'wb') as f:
            f.write(img)
    except:
        print("Not Found:" + urls[i])