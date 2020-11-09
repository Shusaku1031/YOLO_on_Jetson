
total = sum([1 for _ in open('model_data/2020_train.txt')])

with open("model_data/2020_train.txt", "r") as f:
    text = f.readlines() 


with open("model_data/2020_train_part1.txt", "w") as f:
    for data in text[:int(total/2)]:
        f.write(data)

with open("model_data/2020_train_part2.txt", "w") as f:
    for data in text[int(total/2):]:
        f.write(data)