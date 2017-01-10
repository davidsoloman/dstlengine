from generate import batches

import keras

from keras.models import Sequential
from keras.layers import *
from keras.utils.np_utils import to_categorical        
from keras.optimizers import RMSprop, SGD, Nadam

from keras.metrics import mean_absolute_error
import keras.backend as K

width = 64

def tp(y_true, y_pred):
    return K.mean(y_true * y_pred)

def fp(y_true, y_pred):
    return K.mean(y_pred) - tp(y_true, y_pred)

def fn(y_true, y_pred):
    return K.mean(y_true) - tp(y_true, y_pred)
    
def jaccard(y_true, y_pred):
    tpv = tp(y_true, y_pred)
    fpv = fp(y_true, y_pred)
    fnv = fp(y_true, y_pred)
    intersection = tpv+fpv+fnv+ K.epsilon()
    #if intersection == 0 : return 0
    return tpv/intersection

def the_loss(y_true, y_pred):
    y_true = K.clip(y_true, K.epsilon(), 1.-K.epsilon())
    y_pred = K.clip(y_pred, K.epsilon(), 1.-K.epsilon())
    loss =  K.mean(y_true * K.log(y_true / y_pred), axis=-1)
    loss +=  K.mean((1.-y_true) * K.log((1.- y_true) / (1.-y_pred) ), axis=-1)
    #loss +=  2.* K.mean( K.log(y_pred), axis=-1) 
    return loss


def think() :
    
    input_shape=(20, 243, 243)
    
    model= Sequential()
 
    model.add( Convolution2D(64, 3,3, activation='relu', border_mode='same', input_shape=input_shape) )
    model.add( Convolution2D(64, 3,3, activation='relu', border_mode='same') )
    model.add( Convolution2D(10, 1,1, activation='sigmoid', border_mode='same') )    
  
    
    
    default_nadam_lr = 0.002
    opt = Nadam(default_nadam_lr)       
    model.compile(optimizer='rmsprop',
              loss=the_loss,
              metrics=[jaccard, tp,fp,fn])
    model.summary()              


    
    train_gen, train_samples, val_gen, val_samples = batches()
    
    print(train_samples, val_samples)
    
    model.fit_generator( train_gen, train_samples, 400, validation_data=val_gen, nb_val_samples=val_samples)
    
think()