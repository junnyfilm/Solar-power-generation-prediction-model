from datetime import timezone
from datetime import datetime
from datetime import timedelta
from functools import wraps
import time
import pandas as pd
import numpy as np

def check_func_progress(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        a = self.cur_gens.shape
        print(f'Start: {func.__name__:>25} {a}')
        start = time.time()
        func(self, *args, **kwargs)
        b = self.cur_gens.shape
        print(f'End  : {func.__name__:>25} {b} ({time.time()-start:.2f} [sec] elpased)')
    return wrapper

class preprocessing_postech():
    def __init__(self, envs, gens, sites, forecasts_1, forecasts_2, forecasts_3, weathers_1, weathers_2, weathers_3):
        self.envs = envs
        self.gens = gens
        self.sites = sites
        self.forecasts_1 = forecasts_1
        self.forecasts_2 = forecasts_2
        self.forecasts_3 = forecasts_3
        self.weathers_1 = weathers_1
        self.weathers_2 = weathers_2
        self.weathers_3 = weathers_3
        
        self.time_format_weather = '%Y-%m-%dT%H:%M:%S%z' 
        self.time_format_forecaset = '%Y-%m-%dT%H:%M:%S%z'
        self.time_format_generation = '%Y-%m-%d %H:%M:%S%z' 
        self.time_format_new = '%Y-%m-%d %H'
        
    def match_id(self, num_id):
        cur_wth_id_1 = self.sites[self.sites['id']==num_id]['wth1_id']
        cur_wth_id_2 = self.sites[self.sites['id']==num_id]['wth2_id']
        # cur_wth_id_3 = self.sites[self.sites['id']==num_id]['wth3_id']
        
        self.cur_wth_dist_1 = self.sites[self.sites['id']==num_id]['wth1_dist'].values[0]
        self.cur_wth_dist_2 = self.sites[self.sites['id']==num_id]['wth2_dist'].values[0]
        # self.cur_wth_dist_3 = self.sites[self.sites['id']==num_id]['wth3_dist'].values[0]
        
        self.cur_envs = self.envs[self.envs['id'] == num_id]
        self.cur_gens = self.gens[self.gens['id'] == num_id]
        # self.cur_forecasts = self.forecasts[self.forecasts['id'] == cur_wth_id.values[0]]
        self.cur_weathers_1 = self.weathers_1[self.weathers_1['id'] == cur_wth_id_1.values[0]]
        self.cur_weathers_2 = self.weathers_2[self.weathers_2['id'] == cur_wth_id_2.values[0]]
        # self.cur_weathers_3 = self.weathers_3[self.weathers_3['id'] == cur_wth_id_3.values[0]]        
        
        self.cur_capacity = self.sites[self.sites['id']==num_id]['capacity']
    
    
    def weather_time_change(self, time):
        time = datetime.strptime(time, self.time_format_weather)
        time = time.strftime('%Y-%m-%d %H:%M')
        time = datetime.strptime(time, '%Y-%m-%d %H:%M')
        if time.minute // 50 == 0 :
            time = time.strftime(self.time_format_new)
        else :
            # time = time.apply(lambda dt: datatime.datetime(dt.year, dt.month, dt.day, dt.hour+1))
            time = time + timedelta(hours=1)
            time = time.strftime(self.time_format_new)
        return time

    def generation_time_change(self, time):
        time = datetime.strptime(time, self.time_format_generation)
        return time.strftime(self.time_format_new)

    def forecast_time_change(self, time):
        time = datetime.strptime(time, self.time_format_forecaset)
        return time.strftime(self.time_format_new)   
    
    @check_func_progress
    def time_change(self):
        pd.set_option('mode.chained_assignment', None)
        for i in self.cur_weathers_1.index:
            new_time = self.weather_time_change(self.cur_weathers_1.loc[i, 'time'])
            self.cur_weathers_1.loc[i, 'time'] = new_time
        for i in self.cur_weathers_2.index:
            new_time = self.weather_time_change(self.cur_weathers_2.loc[i, 'time'])
            self.cur_weathers_2.loc[i, 'time'] = new_time    
        # for i in self.cur_weathers_3.index:
        #     new_time = self.weather_time_change(self.cur_weathers_3.loc[i, 'time'])
        #     self.cur_weathers_3.loc[i, 'time'] = new_time
            
        for i in self.cur_gens.index:
            new_time = self.generation_time_change(self.cur_gens.loc[i, 'time'])
            self.cur_gens.loc[i, 'time'] = new_time

    @check_func_progress
    def match_time(self):
        self.new_ = pd.DataFrame()
        for i in self.cur_gens.index:
            we_1 = self.cur_weathers_1['time'] == self.cur_gens.loc[i, 'time']
            we_2 = self.cur_weathers_2['time'] == self.cur_gens.loc[i, 'time']
            # we_3 = self.cur_weathers_3['time'] == self.cur_gens.loc[i, 'time']

            if not(sum(we_1) and sum(we_2)):
                continue

            # Time
            time = self.cur_weathers_1[we_1]['time'].values[0]
            hour = self.cur_weathers_1[we_1]['time'].values[0]
            hour = datetime.strptime(hour, '%Y-%m-%d %H')
            hour = int(hour.strftime('%H'))
            
            dew_point = self.cur_weathers_1[we_1]['dew_point'].values[0]
            uv_idx = self.cur_weathers_1[we_1]['uv_idx'].values[0]
            ceiling = self.cur_weathers_1[we_1]['ceiling'].values[0]
            pressure = self.cur_weathers_1[we_1]['pressure'].values[0]
            
            if min(self.cur_wth_dist_1, self.cur_wth_dist_2) < 800:
                dist_list = [self.cur_wth_dist_1, self.cur_wth_dist_2]
                weather_list = [self.cur_weathers_1, self.cur_weathers_2]
                min_region = np.argmin(dist_list)
                we = [we_1, we_2]
                
                temperature = weather_list[min_region][we[min_region]]['temperature'].values[0]
                humidity = weather_list[min_region][we[min_region]]['humidity'].values[0]
                wind_dir = weather_list[min_region][we[min_region]]['wind_dir'].values[0]
                wind_spd = weather_list[min_region][we[min_region]]['wind_spd'].values[0]
                precip_1h = weather_list[min_region][we[min_region]]['precip_1h'].values[0]
                cloudiness = weather_list[min_region][we[min_region]]['cloudiness'].values[0]

            
            else:
                temperature = (self.cur_weathers_1[we_1]['temperature'].values[0] / self.cur_wth_dist_1 + self.cur_weathers_2[we_2]['temperature'].values[0] / self.cur_wth_dist_2 ) / ( 1/self.cur_wth_dist_1 + 1/self.cur_wth_dist_2 )
                humidity = (self.cur_weathers_1[we_1]['humidity'].values[0] / self.cur_wth_dist_1 + self.cur_weathers_2[we_2]['humidity'].values[0] / self.cur_wth_dist_2 ) / ( 1/self.cur_wth_dist_1 + 1/self.cur_wth_dist_2 )
                wind_dir = (self.cur_weathers_1[we_1]['wind_dir'].values[0] / self.cur_wth_dist_1 + self.cur_weathers_2[we_2]['wind_dir'].values[0] / self.cur_wth_dist_2 ) / ( 1/self.cur_wth_dist_1 + 1/self.cur_wth_dist_2 )
                wind_spd = (self.cur_weathers_1[we_1]['wind_spd'].values[0] / self.cur_wth_dist_1 + self.cur_weathers_2[we_2]['wind_spd'].values[0] / self.cur_wth_dist_2 ) / ( 1/self.cur_wth_dist_1 + 1/self.cur_wth_dist_2 )
                precip_1h = (self.cur_weathers_1[we_1]['precip_1h'].values[0] / self.cur_wth_dist_1 + self.cur_weathers_2[we_2]['precip_1h'].values[0] / self.cur_wth_dist_2 ) / ( 1/self.cur_wth_dist_1 + 1/self.cur_wth_dist_2 )
                cloudiness = (self.cur_weathers_1[we_1]['cloudiness'].values[0] / self.cur_wth_dist_1 + self.cur_weathers_2[we_2]['cloudiness'].values[0] / self.cur_wth_dist_2 ) / ( 1/self.cur_wth_dist_1 + 1/self.cur_wth_dist_2 )
            
            new = pd.DataFrame({'id': self.cur_id, 'time': time, 'hour': hour, 'temperature': temperature, 'humidity': humidity, 'wind_dir': wind_dir, 'wind_spd': wind_spd, 'precip_1h': precip_1h, 'cloudiness': cloudiness, 'dew_point': dew_point, 'uv_idx': uv_idx, 'ceiling': ceiling, 'pressure': pressure, 'amount': self.cur_gens.loc[i, 'amount'] / self.cur_capacity})

            self.new_ = self.new_.append(new, ignore_index = True)
        self.new = self.new.append(self.new_, ignore_index = True)
        # to see shpae
        self.cur_gens = self.new_
        
    def main(self):
        self.new = pd.DataFrame()
        for i in range(21):
            print('------- id: {} -------'.format(i))
            self.cur_id = i
            self.match_id(i)
            self.time_change()
            self.match_time()
        return self.new
            