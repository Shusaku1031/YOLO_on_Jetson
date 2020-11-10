import os
import json
import pprint
import argparse
from yolo import YOLO
from PIL import Image, ImageDraw

parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)

parser.add_argument(
    '--model_path', type=str,
    help='path to model weight file, default ' + YOLO.get_defaults("model_path")
)

FLAGS = parser.parse_args()


with open(os.path.join("model_data","2020_test.txt"), "r") as f:
    test_data = f.readlines()

with open(os.path.join("model_data","voc_classes.txt"), "r") as f:
    class_names = f.readlines()
class_names = [c.strip() for c in class_names]

test_text = test_data[48].split(" ")
img_path = test_text[0]
img = Image.open(img_path)

yolo_instance = YOLO(**vars(FLAGS))
detected = yolo_instance.detect_image(img)

draw = ImageDraw.Draw(detected["image"])


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

print(img_path)
detected["image"].show()