import os
import numpy as np
import pandas as pd
import pickle
from utils.prep_postech import *

class prep_1st():
    def __init__(self, common_dir):
        self.common_dir = common_dir
    
    def main(self):
        common_dir = self.common_dir
        
        file = common_dir + '/prep_data.pickle'
        
        data_dir = os.path.join(common_dir, 'data')
        
        if not os.path.isfile(file):
        
            envs = pd.read_csv(data_dir + '/envs.csv')
            gens = pd.read_csv(data_dir + '/gens.csv')

            forecasts1 = pd.read_csv(data_dir + '/forecasts1.csv')
            forecasts2 = pd.read_csv(data_dir + '/forecasts2.csv')
            forecasts3 = pd.read_csv(data_dir + '/forecasts3.csv')

            weathers1 = pd.read_csv(data_dir + '/weathers1.csv')
            weathers2 = pd.read_csv(data_dir + '/weathers2.csv')
            weathers3 = pd.read_csv(data_dir + '/weathers3.csv')

            with open('sites.pickle', 'rb') as f:
                sites = pickle.load(f)
            prep_data = preprocessing_postech(envs, gens, sites, forecasts1, forecasts2, forecasts3, weathers1, weathers2, weathers3).main()

            with open('prep_data.pickle', 'wb') as f:
                pickle.dump(prep_data, f)