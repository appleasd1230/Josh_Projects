from keras.utils import np_utils
from keras.preprocessing import image
from keras.models import Sequential
from keras import optimizers
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
import tensorflow as tf
from sklearn.model_selection import train_test_split
import yaml
import matplotlib.pyplot as plt
import numpy as np
import configparser
import traceback
import os
import logging
from pathlib import Path
import time as t

"""呼叫GPU，如果沒有GPU這三行請註解掉"""
config = tf.compat.v1.ConfigProto( device_count = {'GPU': 0 } ) 
sess = tf.compat.v1.Session(config=config) 
tf.compat.v1.keras.backend.set_session(sess)

"""config"""
config = configparser.ConfigParser()
config.read('Config.ini', encoding = 'utf_8_sig')
dropout = float(config.get('Parameters', 'dropout')) # dropout
batch_size = int(config.get('Parameters', 'batch_size')) # batch_size
epochs = int(config.get('Parameters', 'epochs')) # epochs
lr = float(config.get('Parameters', 'lr')) # learning_rate
size = int(config.get('Parameters', 'size')) # size
image_path = config.get('Parameters', 'image_path') # image_path

"""log紀錄"""
path = str(Path(os.getcwd()))
Info_Log_path = os.path.join(path, "log", t.strftime('%Y%m%d', t.localtime()) + ".log")

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)-4s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers = [logging.FileHandler(Info_Log_path, 'a+', 'utf-8'),])

"""錯誤訊息追蹤"""
def exception_to_string(excp):
   stack = traceback.extract_stack()[:-3] + traceback.extract_tb(excp.__traceback__) 
   pretty = traceback.format_list(stack)
   return ''.join(pretty) + '\n  {} {}'.format(excp.__class__,excp)                    

"""以圖表呈現訓練結果"""
def show_train_history(train_history, title, train, validation):
    plt.plot(train_history.history[train])
    plt.plot(train_history.history[validation])
    plt.title(title)
    plt.ylabel(train)
    plt.xlabel('Epoch')
    plt.legend(['train', 'validation'], loc = 'upper left')
    plt.show()
    
"""讀取圖片以及標記的資料"""
def readData(path):
    imgs = [] # 圖片
    labs = [] # 標記
    for (folder, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            img_path = folder + '\\' + filename
            img = image.load_img(img_path, target_size=(size, size), ) # 讀取照片
            img = image.img_to_array(img) # 將照片轉為array
            # img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            img = np.expand_dims(img, axis=0) # 在0的位置新增資料

            lab = folder.split('\\')[-1] # 讀取標記資料
            
            imgs.append(img) # 寫入img array
            labs.append(lab) # 寫入label            


    return imgs, labs

"""取得訓練以及測試資料集"""
def preprocess():
    imgs, labs = readData(image_path) # 取得圖片與標記
    # 將圖片數據與標籤轉換成數組
    # random_list = list(zip(imgs, labs))
    # random.shuffle(random_list)
    # imgs, labs = zip(*random_list)
    imgs = np.array(imgs, dtype=float)
    # imgs = preprocess_input(imgs)
    labs = np.array([lab for lab in labs])
    labs = np_utils.to_categorical(labs, 10)

    #隨機劃分測試集與訓練集
    train_x,test_x,train_y,test_y = train_test_split(imgs, labs, test_size=0.2, random_state=0)#請改test_size (Change Me)
    # 參數 : 圖片數據的總數，圖片的高、寬、通道
    train_x = train_x.reshape(train_x.shape[0], size, size, 3)
    test_x = test_x.reshape(test_x.shape[0], size, size, 3)
    # 將數據轉換成小于1的數
    train_x = train_x.astype('float32')/255.0
    test_x = test_x.astype('float32')/255.0
    return train_x,test_x,train_y,test_y


def train():
    train_x,test_x,train_y,test_y = preprocess() # 取得訓練資料以及測試資料

    num_classes = 10 # 分成62種 0~9 a~z A~Z
    input_shape = (size, size, 3) # 輸入圖片的尺寸（長寬需不小於 32）
    model = Sequential([
        Conv2D(32, (3, 3), input_shape=input_shape, padding='same', activation='relu'),
        Conv2D(64, (3, 3), activation='relu', padding='same'),
        MaxPooling2D(pool_size=(2, 2), strides=(2, 2)),
        Conv2D(128, (3, 3), activation='relu', padding='same'),
        Conv2D(128, (3, 3), activation='relu', padding='same',),
        MaxPooling2D(pool_size=(2, 2), strides=(2, 2)),
        Conv2D(256, (3, 3), activation='relu', padding='same',),
        Conv2D(256, (3, 3), activation='relu', padding='same',),
        Conv2D(256, (3, 3), activation='relu', padding='same',),
        MaxPooling2D(pool_size=(2, 2), strides=(2, 2)),
        Flatten(),
        Dense(500, activation='relu'),
        Dense(num_classes, activation='softmax')
    ])

    model.summary()

    sgd = optimizers.Adam(lr=lr)
    model.compile(optimizer=sgd, loss='categorical_crossentropy',metrics=['accuracy'])

    train_history = model.fit(train_x, train_y, epochs=epochs, batch_size=batch_size, verbose=2, validation_data=(test_x, test_y))

    show_train_history(train_history, 'Accuracy', 'accuracy', 'val_accuracy')
    show_train_history(train_history, 'loss', 'loss', 'val_loss')

    score = model.evaluate(test_x, test_y,batch_size=batch_size)

    yaml_string = model.to_yaml()
    with open('weights_data/ResNet.yml', 'w') as outfile:
        outfile.write(yaml.dump(yaml_string, default_flow_style=True))
    model.save_weights('weights_data/ResNet.h5')

if __name__ == '__main__':
    train()
