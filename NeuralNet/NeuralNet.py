import tensorflow.keras as k
from tensorflow.keras import metrics
import numpy as np
import datetime
import random
import os
import pandas as pd

from NeuralNet.default_params import params
from system.system import System
from gcloud.gcloud import GCloud
from sklearn.model_selection import train_test_split

class NeuralNet:
    def __init__(self, csv, out_dir):
        self.out_dir = out_dir
        self.csv = csv

    def train(self):
        df = pd.read_csv(self.csv, skiprows=1)
        train, test = train_test_split(df, test_size=0.2)
        train_x = train.iloc[:, 0:-1]
        train_y = train.iloc[:, -1:]
        test_x = test.iloc[:, 0:-1]
        test_y = test.iloc[:, -1:]
        self.train_model(np.array(train_x), np.array(train_y), np.array(test_x), np.array(test_y))

    def train_model(self, train_x, train_y, test_x, test_y):
        # Create neural network architecture
        model = k.Sequential()

        input_layer = k.layers.Dense(len(train_x), input_dim=len(train_x[0]),
                                                            activation=params['INPUT_LAYER']['ACTIVATION'])
        model.add(input_layer)

        for hidden_layer_data in params['HIDDEN_LAYERS']:
            hidden_layer = k.layers.Dense(hidden_layer_data['NUM_NODES'],
                                                            activation=hidden_layer_data['ACTIVATION'])
            model.add(hidden_layer)

        output_layer = k.layers.Dense(params['OUTPUT_LAYER']['NUM_NODES'],
                                                                activation=params['OUTPUT_LAYER']['ACTIVATION'])
        model.add(output_layer)

        # optimizer - sgd, rmsprop
        model.compile(loss=params['LOSS_FUNCTION'], optimizer=params['OPTIMIZER'], metrics=[metrics.binary_accuracy])
        model.fit(np.array(train_x), np.array(train_y), validation_split=params['VALIDATION_SPLIT'],
                epochs=params['EPOCHS'], batch_size=params['BATCH_SIZE'])

        test_loss_test, test_acc_test = model.evaluate(test_x, test_y)

        print('Results: loss {},   accuracy {},  :'.format(test_loss_test, test_acc_test))
        self.test_acc = test_acc_test
        self.model = model
        self.save()
    
    def save(self):
        out_dir = self.out_dir
        date_str = str(datetime.datetime.now().strftime("%d-%B-%Y-%I-%M%p")) + "-" + str(self.test_acc)
        package_dir = os.path.join(out_dir, date_str)
        os.makedirs(package_dir)
        
        self.model.save(os.path.join(package_dir, 'model.h5'))
        System.copy_file_to(self.csv, os.path.join(package_dir, 'data.csv'))
        System.write_json_to_file({
            'test_accuracy': str(self.test_acc),
        }, os.path.join(package_dir, 'accuracy.json'))
        GCloud.upload_directory_to_bucket(package_dir, 'test_bucket_12349876')
        # write_to_json(os.path.join(out_dir, date_str, 'data.csv'), Match.get_features_list())
        # write_to_json(os.path.join(keras_models_directory, date_str, 'params.json'), params)
        # write_to_json(os.path.join(keras_models_directory, date_str, 'accuracy.json'), { 'loss': str(test_loss_test), 'accuracy': str(test_acc_test) })