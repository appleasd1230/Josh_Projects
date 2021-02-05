from keras.applications.resnet50 import ResNet50
from keras.applications.imagenet_utils import preprocess_input
from keras.preprocessing import image
from keras.models import model_from_yaml
from keras import optimizers
# from keras.models import load_model
import yaml
import numpy as np
import configparser
import traceback
import os, sys, io
import logging
from pathlib import Path
import time as t

"""config"""
config = configparser.ConfigParser()
config.read('Config.ini', encoding = 'utf_8_sig')
dropout = float(config.get('Parameters', 'dropout')) # dropout
batch_size = int(config.get('Parameters', 'batch_size')) # batch_size
epochs = int(config.get('Parameters', 'epochs')) # epochs
lr = float(config.get('Parameters', 'lr')) # learning_rate
size = int(config.get('Parameters', 'size')) # size
test_path = config.get('Parameters', 'test_path') # label_path
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

"""讀取Model"""
def load_model():
	with open('weights_data/ResNet.yml', 'r') as f:
		yaml_string = yaml.load(f)
	model = model_from_yaml(yaml_string)
	model.load_weights('weights_data/ResNet.h5')
	model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
	return model    

"""預測結果"""
def predict():
    model = load_model() # 讀取參數

    for (folder, dirnames, filenames) in os.walk(test_path):
        for filename in filenames:
            img_path = folder + '\\' + filename  
            img = image.load_img(img_path, target_size=(size, size)) # 讀取照片
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            img = preprocess_input(img)
            preds = np.argmax(model.predict(img), axis=-1)
            print('結果 : ' + str(preds[0]) + ', 正確答案 : ' + filename.split('.')[0])

if __name__ == '__main__':
    predict()
