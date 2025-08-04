import os
import numpy as np
from PIL import Image
from keras.layers import Input
from keras.models import Model
from keras.applications.resnet50 import decode_predictions
from keras.applications.resnet_v2 import ResNet50V2

# Размеры изображения
height = width = nh = nw = 224
ncol = 3

# Создание модели ResNet
visible2 = Input(shape=(nh, nw, ncol), name='imginp')
resnet = ResNet50V2(include_top=True,
                    weights='imagenet',
                    input_tensor=visible2,
                    input_shape=None,
                    pooling=None,
                    classes=1000)


def read_image_files(files_max_count,dir_name):
    files = [item.name for item in os.scandir(dir_name) if item.is_file()]
    files_count = files_max_count
    if(files_max_count>len(files)): # определяем количество файлов не больше max
        files_count = len(files)
        image_box = [[]] * files_count
        for file_i in range(files_count):  # читаем изображения в список
            image_box[file_i] = Image.open(dir_name + '/' + files[file_i])  # / ??
    return files_count, image_box

def getresult(image_box):
    """Обработка изображений через нейросеть"""
    files_count = len(image_box)
    images_resized = []

    for i in range(files_count):
        img = image_box[i].resize((height, width))
        images_resized.append(np.array(img) / 255.0)

    images_resized = np.array(images_resized)
    out_net = resnet.predict(images_resized)
    decode = decode_predictions(out_net, top=1)
    return decode


# Пример использования
if __name__ == "__main__":
    fcount, fimage = read_image_files(1, './static')
    if fcount > 0:
        decode = getresult(fimage)
        print("Результат распознавания:", decode)