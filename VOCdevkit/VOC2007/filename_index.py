import os


annotate_files = os.listdir("Annotations")
file_name = []
for n in annotate_files:
  file_name.append(n.split(".")[0])
print(file_name)

train_rate = 0.95
test_rate = 0.5
train_amount = round(len(file_name) * train_rate)
test_amount = round((len(file_name)-train_amount)*test_rate)

print("total:",len(file_name))
print("train:",train_amount)
print("test:",test_amount)
print("validate:",len(file_name)-train_amount-test_amount)

with open("ImageSet/Main/train.txt",mode="w") as f:
  for fn in file_name[:train_amount]:
    contents = fn + "\n"
    f.write(contents)
  
with open("ImageSet/Main/test.txt",mode="w") as f:
  for fn in file_name[train_amount:train_amount+test_amount]:
    contents = fn + "\n"
    f.write(contents)
  
with open("ImageSet/Main/val.txt",mode="w") as f:
  for fn in file_name[train_amount+test_amount:]:
    contents = fn + "\n"
    f.write(contents)
  