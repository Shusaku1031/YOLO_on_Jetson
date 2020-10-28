import os
import cv2
import shutil
import xml.etree.ElementTree as ET
import numpy as np  
""" from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
 """
images_path = os.path.join("VOCdevkit","VOC2007","JPEGImage")
annotations_path = os.path.join("VOCdevkit","VOC2007","Annotations")

image_files = os.listdir(images_path)
annotation_files = os.listdir(annotations_path)

print(len(image_files),len(annotation_files))

""" 
print(annotation_files[0])
print(image_files[0]) """
gamma = 0.5
table = np.array([((i / 255.0) ** (1 / gamma)) * 255 for i in np.arange(0, 256)]).astype("uint8")

print("processing images")
for i in range(len(image_files)):
    
    target_file = annotation_files[i].split(".")[0]
    augmentation_name = target_file + "_augment"
    
    print(augmentation_name)
    #image augmentation
    img = cv2.imread(os.path.join(images_path,target_file + ".jpg"))
    for j in range(len(["R","G","B"])):
        img[:,:,j] = cv2.equalizeHist(img[:,:,j])
    img = cv2.LUT(img,table)
    cv2.imwrite(os.path.join(images_path,augmentation_name + ".jpg"),img)

    #annotations copy
    original_file = os.path.join(annotations_path,target_file + ".xml")
    copy_file = os.path.join(annotations_path,augmentation_name + ".xml")
    shutil.copyfile(original_file,copy_file)

"""print(target_file)
print(copy_file)
print(annotation_files[i])
cv2.imwrite("test.jpg",img)

print(annotation_files[0])

shutil.copyfile(os.path.join(annotations_path,annotation_files[0]),annotation_files[0].split(".")[0]+"_gamma.xtml") """