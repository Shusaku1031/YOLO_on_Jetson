import os
import json
import pprint
from yolo import YOLO
from PIL import Image, ImageDraw

with open(os.path.join("model_data","2020_test.txt"), "r") as f:
    test_data = f.readlines()

with open(os.path.join("model_data","voc_classes.txt"), "r") as f:
    class_names = f.readlines()
class_names = [c.strip() for c in class_names]

save_dict = {}

yolo_instance = YOLO()

for test in test_data:
    test_text = test[:-1].split(" ")
    img_path = test_text[0]
    img = Image.open(img_path)
    detected = yolo_instance.detect_image(img)

    draw = ImageDraw.Draw(detected["image"])

    save_dict[img_path] = {}
    save_dict[img_path]["ground truth"] = {}

    gt_bbox = []
    for bbox in test_text[1:]:
        gt = {}
        bbox_split = bbox.split(",")
        
        gt["class"] = class_names[int(bbox_split[4])]
        gt["bbox"] = {
            "top": int(bbox_split[0]),
            "left": int(bbox_split[1]),
            "bottom": int(bbox_split[2]),
            "right": int(bbox_split[3])
        }
        gt_bbox.append(gt)
        for i in range(3):
            draw.rectangle(
                [int(bbox_split[1]) + i, int(bbox_split[0]) + i, int(bbox_split[2]) - i, int(bbox_split[3]) - i],
            outline=(0,0,255))

    save_dict[img_path]["ground truth"] = gt_bbox
    save_dict[img_path]["prediction"] = detected["info"]


del draw

#pprint.pprint(save_dict, width=50)

with open("test_result.json", "w") as f:
    json.dump(save_dict, f, indent=4)
#detected["image"].show()

