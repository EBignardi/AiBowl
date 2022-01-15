import matplotlib
import tensorflow as tf
from tensorflow.keras.layers import Dense, Flatten, Dropout, Conv2D, MaxPooling2D, BatchNormalization
from tensorflow.keras.models import Sequential

import torch
import torch.nn as nn
from torch.autograd.grad_mode import F
from torch.nn import init
from torchvision import models
import torchvision.transforms as T
from torchvision.utils import make_grid
from torchvision.utils import save_image
from IPython.display import Image
import matplotlib.pyplot as plt
import numpy as np
import random

from torch.utils.data import DataLoader, Dataset

import numpy as np
import os
import random
import cv2
from sklearn.model_selection import train_test_split
from numba import cuda

print(cuda.gpus)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
img_size = 100
animals = ["dog", "horse", "chicken", "cat", "cow", "sheep", "squirrel"]

def create_data():
    categories = {'cane': 'dog', "cavallo": "horse", "gallina": "chicken", "gatto": "cat", "mucca": "cow",
                  "pecora": "sheep", "scoiattolo": "squirrel"}
    data = []
    
    img_size = 100
    num_img = 0

    for category, translate in categories.items():
        path = "/home/erosb/Desktop/raw-img/" + category
        print(path)
        target = animals.index(translate)

        for img in os.listdir(path):
            # tqdm(range(os.listdir(path)))
            try:
                img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
                new_img_array = cv2.resize(img_array, (img_size, img_size))
                data.append([new_img_array, target])
                num_img += 1
                print(num_img)
            except Exception as e:
                pass

    random.shuffle(data)
    x = []
    y = []

    for features, labels in data:
        x.append(features)
        y.append(labels)
        
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    x_train = np.array(x_train).reshape(-1, img_size, img_size, 1)
    # x_train = tf.keras.utils.normalize(x_train, axis=1)
    y_train = np.array(y_train)

    print("load data finished")

    return x_train, y_train, x_test, y_test, img_size


def train_CNN_Network(x_train, y_train, x_test, y_test, img_size):
    model = Sequential()
    model.add(Conv2D(32, kernel_size=3, activation='relu', input_shape=x_train.shape[1:]))
    print(x_train.shape[1:])
    model.add(BatchNormalization())
    model.add(Conv2D(32, kernel_size=3, activation='relu'))
    model.add(BatchNormalization())
    model.add(Conv2D(32, kernel_size=5, strides=2, padding='same', activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.4))
    model.add(Conv2D(64, kernel_size=5, strides=2, padding='same', activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.4))
    model.add(Conv2D(256, kernel_size=4, activation='relu'))
    model.add(BatchNormalization())
    model.add(Flatten())
    model.add(Dropout(0.4))
    model.add(Dense(64, activation='softmax'))
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

    # training...
    for i in range(10):
        model.fit(x_train, y_train, epochs=5, batch_size=500)
        print('Saving checkpoints for step: ' + str(i))
        model.save_weights('checkpoint_step_save')

    # model.load_weights('checkpoint_step_save')

    # prediction...
    
    prediction = model.predict(np.array(x_test).reshape(-1, img_size, img_size, 1))
    # predict_x = model.predict(x_test) 
    classes_x = np.argmax(prediction, axis=1)
    # class_predicted = model.predict_classes(prediction)
    print('Label predetta: ' + str(classes_x[0:10]) + 'Label corretta: ' + str(y_test[0:10]))
    # print('Accuracy: ' + str(score))
    return model


def CNN_Network():
    model = Sequential()
    model.add(Conv2D(32, kernel_size=3, activation='relu', input_shape=(100, 100, 1)))
    model.add(BatchNormalization())
    model.add(Conv2D(32, kernel_size=3, activation='relu'))
    model.add(BatchNormalization())
    model.add(Conv2D(32, kernel_size=5, strides=2, padding='same', activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.4))
    model.add(Conv2D(64, kernel_size=5, strides=2, padding='same', activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.4))
    model.add(Conv2D(256, kernel_size=4, activation='relu'))
    model.add(BatchNormalization())
    model.add(Flatten())
    model.add(Dropout(0.4))
    model.add(Dense(64, activation='softmax'))
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

    model.load_weights('checkpoint_step_save')

    return model



def read_show_image(path):
    # read image
    image = cv2.imread(path)
    # show the image, provide window name first
    cv2.imshow('image window', image)
    # add wait key. window waits until user presses a key
    cv2.waitKey(0)
    # and finally destroy/close all open windows
    cv2.destroyAllWindows()


def search_animal(model, frame):
    print(frame.shape)
    prediction = model.predict(np.array(frame).reshape(-1, img_size, img_size, 1))
    classes_x = np.argmax(prediction, axis=1)
    label=str(animals[classes_x[0]])
    return label