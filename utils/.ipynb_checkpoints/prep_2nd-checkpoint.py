import os
import pickle
import numpy as np
import pandas as pd

class prep_2nd():
    def __init__(self, data_dir):
        self.data_dir = data_dir
    
    def main(self):
        
        data_dir = self.data_dir
        
        file = data_dir + '/x_data.npy'
        
        if not os.path.isfile(file):
        
            print('------- Remove Outlier -------')
            
            with open('prep_data.pickle', 'rb') as f:
                prep_train = pickle.load(f)

            prep_train = prep_train.drop(index = range(150822,151569))
            prep_train = prep_train.reset_index(drop=True)
            for i in range(len(prep_train)):
                if abs(prep_train.loc[i, 'temperature']) > 50 or abs(prep_train.loc[i, 'wind_spd']) > 50 or abs(prep_train.loc[i, 'cloudiness']) > 100 or abs(prep_train.loc[i, 'humidity']) > 100 or abs(prep_train.loc[i, 'precip_1h']) > 50 or abs(prep_train.loc[i, 'uv_idx']) > 20:
                    prep_train = prep_train.drop(index = i )
            prep_train = prep_train.reset_index(drop=True)

            # num_id = 20

            # plt.plot(prep_train[prep_train['id'] == num_id]['wind_spd'])
            # plt.plot(prep_train[prep_train['id'] == num_id]['humidity'])
            # plt.plot(prep_train[prep_train['id'] == num_id]['temperature'])
            # plt.plot(prep_train[prep_train['id'] == num_id]['precip_1h'])
            # plt.plot(prep_train[prep_train['id'] == num_id]['cloudiness'])

            x_data = np.empty((0,24,9))
            y_data = np.empty((0,24))
            for i in range(len(prep_train)-24):
                if prep_train.loc[i, 'hour'] == 1:
                    if prep_train.loc[i+23, 'hour'] == 0:
                        if prep_train.loc[i, 'id'] ==0:
                            for j in range(10):
                                x_data = np.concatenate([x_data, np.expand_dims(prep_train.iloc[i:i+24, 3:12].to_numpy(), 0)], 0)
                                y_data = np.concatenate([y_data, np.expand_dims(prep_train.iloc[i:i+24, 13].to_numpy(), 0)], 0)
                        else:
                            x_data = np.concatenate([x_data, np.expand_dims(prep_train.iloc[i:i+24, 3:12].to_numpy(), 0)], 0)
                            y_data = np.concatenate([y_data, np.expand_dims(prep_train.iloc[i:i+24, 13].to_numpy(), 0)], 0)

            np.save('x_data.npy', x_data)
            np.save('y_data.npy', y_data)