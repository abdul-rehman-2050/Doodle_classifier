
from __future__ import print_function
#simplified interface for building models 
import keras
#our handwritten character labeled dataset
from keras.datasets import mnist
#because our models are simple
from keras.models import Sequential
#dense means fully connected layers, dropout is a technique to improve convergence, flatten to reshape our matrices for feeding
#into respective layers
from keras.layers import Dense, Dropout, Flatten
#for convolution (images) and pooling is a technique to help choose the most relevant features in an image
from keras.layers import Conv2D, MaxPooling2D, MaxPooling2D, Conv1D
from keras import backend as K
import numpy as np
import os



#mini batch gradient descent ftw
batch_size = 128
#10 difference characters
num_classes = 3
#very short training time
epochs = 10

# input image dimensions
#28x28 pixel images. 
img_rows, img_cols = 28, 28


# In[3]:


# the data downloaded, shuffled and split between train and test sets
#if only all datasets were this easy to import and format
import pandas as pd
from sklearn.model_selection import train_test_split
X = np.load('dataset.npy')
X = X.reshape(3000,28,28)
y = np.load('labels.npy')
y = np.array(y, dtype='uint8')
y = keras.utils.np_utils.to_categorical(y)
x_train, x_test, y_train, y_test = train_test_split(X, y)


# In[4]:


# this assumes our data format
# For 3D data, "channels_last" assumes (conv_dim1, conv_dim2, conv_dim3, channels) while 
# "channels_first" assumes (channels, conv_dim1, conv_dim2, conv_dim3).
if K.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
    x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
else:
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)

    print(x_train.shape[0])

    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
input_shape = (img_rows, img_cols, 1)
#more reshaping
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')



# In[5]:


#build our model
model = Sequential()
#convolutional layer with rectified linear unit activation
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=input_shape))
#again
model.add(Conv2D(64, (3, 3), activation='relu'))
#choose the best features via pooling
model.add(MaxPooling2D(pool_size=(2, 2)))
#randomly turn neurons on and off to improve convergence
model.add(Dropout(0.25))
#flatten since too many dimensions, we only want a classification output
model.add(Flatten())
#fully connected to get all relevant data
model.add(Dense(128, activation='relu'))
#one more dropout for convergence' sake :) 
model.add(Dropout(0.5))
#output a softmax to squash the matrix into output probabilities
model.add(Dense(num_classes, activation='softmax'))
#Adaptive learning rate (adaDelta) is a popular form of gradient descent rivaled only by adam and adagrad
#categorical ce since we have multiple classes (10) 
model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

#train that ish!
model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(x_test, y_test))
 #how well did it do? 
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])


# In[6]:


#Save the model
# serialize model to JSON
model_json = model.to_json()
os.chdir("../Main")
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")
print('Now run app.py')

