import xml.etree.ElementTree as ET
import os
import cv2
import numpy as np 


wnid = "n02231487"
files = os.listdir(os.path.join("bbox","Annotation",wnid))
wd = os.getcwd()

availables = []
count = 0
for f in files:

    with open(os.path.join("bbox","Annotation",wnid,f)) as x:
        xml_raw = x.read()

    #print(xml_raw)

    #print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    root = ET.fromstring(xml_raw)

    save_dir = os.path.join("use_images",root[0].text)

    if os.path.isdir(save_dir) == False:
        os.mkdir(save_dir)
    
    try:
        img = cv2.imread(os.path.join("raw_images",root[0].text,root[1].text))
        save_path = os.path.join("use_images",root[0].text,root[1].text)+".jpg"

        train_size = 416
        max_side = max(img.shape)
        count += 1
        square = np.zeros((max_side,max_side,img.shape[2]), dtype="uint8")

        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                square[i][j] = img[i][j]

        for z in root.iter('width'):
            print(z.text)
        """ xmin = int(root[5][4][0].text)
        ymin = int(root[5][4][1].text)
        xmax = int(root[5][4][2].text)
        ymax = int(root[5][4][3].text) 
        bndbox = [xmin,ymin,xmax,ymax]"""

        square = cv2.resize(square,(train_size,train_size))
        print("after resize")
        reshape_rate = train_size / max_side
        print(reshape_rate)

        xmin = []
        ymin = []
        xmax = []
        ymax = []

        for z in root.iter('xmin'):
            xmin.append(round(int(z.text)*reshape_rate))

        for z in root.iter('ymin'):
            ymin.append(round(int(z.text)*reshape_rate))

        for z in root.iter('xmax'):
            xmax.append(round(int(z.text)*reshape_rate))

        for z in root.iter('ymax'):
            ymax.append(round(int(z.text)*reshape_rate))

        annotation_text = "{}/{}".format(wd,save_path)

        for i in range(len(xmin)):
            print((xmin[i],ymin[i],xmax[i],ymax[i]))
            annotation_text += " {},{},{},{},{}".format(xmin[i],ymin[i],xmax[i],ymax[i],0) 
            #cv2.rectangle(square,(xmin[i],ymin[i]),(xmax[i],ymax[i]),(56,0,231),2)

        availables.append(annotation_text)
        #print(square)
        #print(img)
        #print(square.shape)
        cv2.imwrite(save_path,square)

        #cv2.imshow("",square)
        #cv2.waitKey(0)

    except Exception as e:
        print(os.path.join("images",root[0].text,root[1].text))
        print(e)

print(availables)

annotation_path = os.path.join("model_data")

train_rate = 0.9
test_rate = 0.1
#val_rate = 0.05

train_annotations = availables[:round(len(availables)*train_rate)]
#val_annotations = availables[round(len(availables)*train_rate):round(len(availables)*(train_rate+val_rate))]
#test_annotations = availables[round(len(availables)*(train_rate+val_rate)):]
test_annotations = availables[round(len(availables)*train_rate):]

with open(os.path.join("model_data","2020_train.txt"),"w") as f:
    for n in train_annotations:
        f.write(n+"\n")

""" with open(os.path.join("model_data","2020_val.txt"),"w") as f:
    for n in val_annotations:
        f.write(n+"\n") """

with open(os.path.join("model_data","2020_test.txt"),"w") as f:
    for n in test_annotations:
        f.write(n+"\n")