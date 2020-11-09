import os
import cv2

with open(os.path.join("model_data","2020_train.txt"),"r") as f:
    annotations = f.readlines()

sample = annotations[87].split(" ")
img = cv2.imread(sample[0])
coordinate = [int(i) for i in sample[1].replace("\n","").split(',')[:4]]
print(coordinate)
cv2.rectangle(img,(coordinate[0],coordinate[1]),(coordinate[2],coordinate[3]),(239,0,22),2)

cv2.imshow("",img)
cv2.waitKey(0)