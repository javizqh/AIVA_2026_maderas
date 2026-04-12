import os
import re
import argparse
import numpy as np
import pandas as pd
import cv2
import collections
from iterstrat.ml_stratifiers import MultilabelStratifiedShuffleSplit
from ultralytics import YOLO


def tryint(s):
    try:
        return int(s)
    except Exception:
        return s


def alphanum_key(s):
    """Turn a string into a list of string and number chunks.
    "z23a" -> ["z", 23, "a"]
    """
    return [tryint(c) for c in re.split("([0-9]+)", s)]


def get_images(dir_path):
    files = [
        os.path.join(dir_path, x)
        for x in os.listdir(dir_path)
        if os.path.isfile(os.path.join(dir_path, x))
    ]

    files.sort(key=alphanum_key)

    imgs = []
    labels = []

    index = 0
    for file in files:
        if index % 2 == 0:
            imgs.append(file)
        else:
            labels.append(file)
        index += 1

    return (imgs, labels)


def read_label(path):
    try:
        s = cv2.FileStorage()
        s.open(path, cv2.FileStorage_READ)
        matrix = s.getNode("rectangles").mat()
        matrix = matrix.T
        s.release()
    except Exception:
        matrix = []

    return matrix


def load_image(path: str) -> np.array:
    """Loads an image using opencv and return it.

    Keyword arguments:
    path -- the image path
    """
    if not os.path.isfile(path):
        raise Exception("Image does not exist")

    img = cv2.imread(path, cv2.IMREAD_COLOR_BGR)
    # img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


def create_yolo_labels():
    images, labels = get_images("../dataset")

    zipped = zip(images, labels)

    for img, label in zipped:
        instances = read_label(label)
        print(img, instances)
        img = load_image(img)

        new_labels = ""

        for instance in instances:
            overlay = img.copy()
            [x, y, w, h] = instance
            p1 = [int(x), int(y)]
            p2 = [int(x + w), int(y + h)]
            cv2.rectangle(overlay, p1, p2, (0, 0, 255), 3)

            cv2.imshow("Image", overlay)
            cv2.waitKey(1)

            new_class = ""

            new_class = input("Class: ")
            print("\033[1A" + "\x1b[2K", end="")

            if new_class == "q":  # q
                cv2.destroyAllWindows()
                exit()
            height, width, _ = img.shape

            nx = (x + w / 2) / width
            ny = (y + h / 2) / height

            new_labels += f"{new_class} {nx} {ny} {w / width} {h / height}\n"

        new_label_path = label[:-4] + ".txt"
        with open(new_label_path, "w") as f:
            f.write(new_labels)


def generate_splits_dataset(train=0.7, val=0.15, test=0.15):

    labels_column = []
    total_labels = []
    image_names_column = []

    labels_path = "../dataset_yolo/labels"

    # Get the labels from the txt files and make a label column list of all image labels (without duplicates)
    for file in os.listdir(labels_path):
        if os.path.isfile(os.path.join(labels_path, file)):
            filename, extension = os.path.splitext(file)
            image_names_column.append(filename + ".png")
            with open(os.path.join(labels_path, file)) as txt:
                orig_labels = []
                for line in txt:
                    words = line.split()
                    orig_labels.append(int(words[0]))
                    total_labels.append(int(words[0]))
                labels_column.append(orig_labels)

    # Create csv data
    csv_rows = zip(image_names_column, labels_column)

    # Load dataframe and convert to column per label
    df = pd.DataFrame(csv_rows, columns=["images", "labels"])
    labels = df["labels"]
    cs = collections.Counter(total_labels)

    text_to_category = {label: [] for label in cs.keys()}
    for _, item in df.iterrows():
        for label in text_to_category:
            text_to_category[label].append(item["labels"].count(label))

    for label in text_to_category:
        df[label] = text_to_category[label]

    del df["labels"]

    class_list = list(filter(lambda x: x != "images", df.columns))

    X = labels.to_numpy()
    Y = df[class_list].to_numpy(dtype=np.float32)
    msss = MultilabelStratifiedShuffleSplit(
        n_splits=1, test_size=1 - train, random_state=0
    )

    for train_index, tmp_index in msss.split(X, Y):
        train_list = train_index.tolist()
        tmp_list = tmp_index.tolist()
        for i in range(len(train_list)):
            train_list[i] = image_names_column[train_list[i]]

        for i in range(len(tmp_list)):
            tmp_list[i] = image_names_column[tmp_list[i]]

    train_df = df[df["images"].isin(train_list)]
    tmp_df = df[df["images"].isin(tmp_list)]
    tmp_index = df.index[df["images"].isin(tmp_list)].to_list()

    X = labels[tmp_index].to_numpy()
    Y = tmp_df[class_list].to_numpy(dtype=np.float32)
    msss = MultilabelStratifiedShuffleSplit(
        n_splits=1, test_size=val / (test + val), random_state=0
    )

    for test_index, val_index in msss.split(X, Y):
        val_list = val_index.tolist()
        test_list = test_index.tolist()
        for i in range(len(val_list)):
            val_list[i] = tmp_list[val_list[i]]

        for i in range(len(test_list)):
            test_list[i] = tmp_list[test_list[i]]

    val_df = df[df["images"].isin(val_list)]
    test_df = df[df["images"].isin(test_list)]

    return train_df, val_df, test_df


def mv_to_split(split, df):
    images_path = os.path.join("../dataset_yolo/images", split)
    labels_path = os.path.join("../dataset_yolo/labels", split)

    if df.empty:
        return

    for file in df["images"]:
        label = file.replace(".png", ".txt")

        og_path = os.path.join("../dataset_yolo/images", file)
        target_path = os.path.join(images_path, file)
        os.replace(og_path, target_path)

        og_txt_path = os.path.join("../dataset_yolo/labels", label)
        target_txt_path = os.path.join(labels_path, label)
        os.replace(og_txt_path, target_txt_path)


def split_dataset():
    train_df, val_df, test_df = generate_splits_dataset()

    mv_to_split("train", train_df)
    mv_to_split("val", val_df)
    mv_to_split("test", test_df)


def train_model():
    model = YOLO("yolo26s.pt")
    model.train(
        data="dataset_yolo/data.yaml",
        epochs=2000,
        patience=1000,
        lr0=0.001,
        lrf=0.001,
        mosaic=0,
        erasing=0,
        imgsz=488,
        batch=24,
        project="trainings",
        device=-1,
        name="Maderas",
    )
    model.export(format="onnx")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Visual tracking using particles filter"
    )

    parser.add_argument("--create", help="Create Yolo labels", action="store_true")
    parser.add_argument("--split", help="Split Yolo dataset", action="store_true")
    parser.add_argument("--train", help="Train Yolo model", action="store_true")

    args = parser.parse_args()

    if args.create:
        create_yolo_labels()
    elif args.split:
        split_dataset()
    elif args.train:
        train_model()
    else:
        parser.print_help()
