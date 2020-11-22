import os
import json
import pprint
import argparse
from yolo import YOLO
from PIL import Image, ImageDraw
import tensorflow as tf
import keras.backend as K

print("Configuration...")
config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.66
sess = tf.Session(config=config)
K.set_session(sess)


parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)

parser.add_argument(
    '--model_path', type=str,
    help='path to model weight file, default ' + YOLO.get_defaults("model_path")
)

parser.add_argument(
    '--save_path', type=str, default='detection_result.json0',
    help='path to model weight file, default '
)

FLAGS = parser.parse_args()

if os.path.isdir(FLAGS.save_path) == False:
    os.mkdir(FLAGS.save_path)

if os.path.isdir(os.path.join(FLAGS.save_path,"groundtruths")) == False:
    os.mkdir(os.path.join(FLAGS.save_path,"groundtruths"))
    
if os.path.isdir(os.path.join(FLAGS.save_path,"detections")) == False:
    os.mkdir(os.path.join(FLAGS.save_path,"detections"))

with open(os.path.join("model_data","2020_test.txt"), "r") as f:
    test_data = f.readlines()

with open(os.path.join("model_data","voc_classes.txt"), "r") as f:
    class_names = f.readlines()
class_names = [c.strip() for c in class_names]

save_dict = {}
print(vars(FLAGS))
yolo_instance = YOLO(**vars(FLAGS))

for test in test_data:
    test_text = test[:-1].split(" ")
    img_path = test_text[0]
    
    img = Image.open(img_path)
    detected = yolo_instance.detect_image(img)
    draw = ImageDraw.Draw(detected["image"])

    """ with open(os.path.join("Object-Detection-Metrics","groundtruths",img_path.split("/")[-1].split(".")[0]+".txt"), "w") as f:
        for bbox in test_text[1:]:
            bbox_split = bbox.split(',')
            target_name = class_names[int(bbox_split[4])]
            top = bbox_split[0]
            left = bbox_split[1]
            bottom = bbox_split[2]
            right = bbox_split[3]
            f.write(target_name + " " + top + " " + left + " " + bottom + " " + right + "\n")
 """
    with open(os.path.join(FLAGS.save_path,"groundtruths",img_path.split("/")[-1].split(".")[0]+".txt"), "w") as f:
        for bbox in test_text[1:]:
            bbox_split = bbox.split(',')
            target_name = class_names[int(bbox_split[4])]
            top = bbox_split[0]
            left = bbox_split[1]
            bottom = bbox_split[2]
            right = bbox_split[3]
            f.write(target_name + " " + left + " " + top + " " + right+ " " + bottom + "\n")

    """ with open(os.path.join("Object-Detection-Metrics","detections",img_path.split("/")[-1].split(".")[0]+".txt"), "w") as f:
        for predict_vals in detected["info"]:
            top = str(predict_vals["bbox"]["top"])
            left = str(predict_vals["bbox"]["left"])
            bottom = str(predict_vals["bbox"]["bottom"])
            right = str(predict_vals["bbox"]["right"])
            f.write(predict_vals["class"] + " " + str(predict_vals["score"]) + " " + top + " " + left + " " + bottom + " " + right + "\n")
 """
 
    with open(os.path.join(FLAGS.save_path,"detections",img_path.split("/")[-1].split(".")[0]+".txt"), "w") as f:
        for predict_vals in detected["info"]:
            top = str(predict_vals["bbox"]["top"])
            left = str(predict_vals["bbox"]["left"])
            bottom = str(predict_vals["bbox"]["bottom"])
            right = str(predict_vals["bbox"]["right"])
            f.write(predict_vals["class"] + " " + str(predict_vals["score"]) + " " + left + " " + top + " " + right + " " + bottom + "\n")



    #img = Image.open(img_path)
    #detected = yolo_instance.detect_image(img)

    #draw = ImageDraw.Draw(detected["image"])

#JSONに書き込んでいた頃のコード
""" for test in test_data:
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

with open(FLAGS.save_path, "w") as f:
    json.dump(save_dict, f, indent=4)
#detected["image"].show() """

