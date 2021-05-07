# -*- coding: utf-8 -*-
"""FRFD-DL.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xBKWHTgkQIN5dODmtCTR0Dk_sZnw2PXh

#***Fake or Real Face detection using CNN***
"""

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import pandas as  pd
import matplotlib.pyplot as plt
import zipfile

zip=zipfile.ZipFile('data.zip')
zip.extractall()

model=Sequential()
model.add(Conv2D(32,(3,3),input_shape = (64,64,3),activation = 'relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Flatten())
model.add(Dense(units=2500,activation='relu'))
model.add(Dense(units=1,activation='sigmoid'))

model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])# optimising model

train_datagen=ImageDataGenerator(rescale=1./255,shear_range=0.2,zoom_range=0.2,horizontal_flip=True)
val_datagen=ImageDataGenerator(rescale=1./255)

training_set=train_datagen.flow_from_directory('data/train',target_size=(64,64),batch_size=100,class_mode='binary')
val_set=val_datagen.flow_from_directory('data/valid',target_size=(64,64),batch_size=100,class_mode='binary')

history=model.fit(training_set,steps_per_epoch=15,epochs=100,validation_data=val_set,validation_steps=2)
# saving the model
model.save('FRFD.h5')

print("Accuracy of the model is --> " , model.evaluate(val_set, batch_size=100)[1]*100 , "%")
print("Loss of the model is --> " , model.evaluate(val_set, batch_size=100)[0])

plt.figure(0)
plt.plot(history.history['accuracy'], label='training accuracy')
plt.plot(history.history['val_accuracy'], label='val accuracy')
plt.title('Accuracy')
plt.xlabel('epochs')
plt.ylabel('accuracy')
plt.legend()
plt.savefig('Accuracy.png')

plt.figure(1)
plt.plot(history.history['loss'], label='training loss')
plt.plot(history.history['val_loss'], label='val loss')
plt.title('Loss')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.legend()
plt.savefig('Loss.png')
print("Saved Model & Graph to disk")

"""#***Testing the model***"""

from tensorflow.keras.models import model_from_json # used to import model
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image# used for preproccesing
import os

zip=zipfile.ZipFile('test.zip')
zip.extractall()

model=load_model('FRFD.h5')
print("loaded model from disk")

def classify(img_file):
    img_name=img_file
    test_image=image.load_img(img_name,target_size=(64,64))
    test_image=image.img_to_array(test_image)
    test_image=np.expand_dims(test_image,axis=0)
    result=model.predict(test_image)

    if result[0][0]==1:
        prediction='Fake Face'
        print("\n In this{0}the face is{1}!".format(img_name,prediction))   
    else:
        prediction='Real Face'
        print("\n In this{0}the face is{1}!".format(img_name,prediction))

cur_path = os.getcwd()
path = os.path.join(cur_path,'test/')

files=[]
# r=root,d=directories,f=files
for r,d,f in os.walk(path):
    for file in f:
        if '.jpeg' or '.jpg' or '.png' or '.JPEG' in file:
            files.append(os.path.join(r,file))
for f in files: 
    classify(f)