import requests

from datetime import timezone
from datetime import datetime
from datetime import timedelta
from functools import wraps
import time
import pandas as pd
import numpy as np


class test_api_load():
    def __init__(self, api_key, now_date, now_hour, pred_date):
        
        self._API_URL = 'https://research-api.dershare.xyz'
        self._API_KEY = api_key
        self._AUTH_PARAM = {'headers': {'Authorization': f'Bearer {self._API_KEY}'}}

        self.cur_id = 0
        
        self.now_date = now_date
        self.now_hour = now_hour
        self.pred_date = pred_date
    
    def _get(self, url):
        response = requests.get(url, **self._AUTH_PARAM)
        return response.json()
    
    def _get_pv_sites(self):
        self.pv_sites = self._get(f'{self._API_URL}/open-proc/cmpt-2022/pv-sites')
        
    def _get_pv_gens(self):
        self.pv_gens = self._get(f'{self._API_URL}/open-proc/cmpt-2022/pv-gens/{self.pred_date}')
        return self.pv_gens
    
    def get_site(self):
        self._get_pv_sites()
        self.sites = pd.DataFrame(self.pv_sites)
    
    def get_forecasts(self):
        
        wth1_id = 1
        wth2_id = 1
        wth3_id = 1

        hour = self.now_hour
        
        self.forecasts_1 = self._get(f'{self._API_URL}/open-proc/cmpt-2022/weathers/1/{wth1_id}/forecasts/{self.now_date}/{hour}')
        self.forecasts_2 = self._get(f'{self._API_URL}/open-proc/cmpt-2022/weathers/2/{wth2_id}/forecasts/{self.now_date}/{hour}')
        self.forecasts_3 = self._get(f'{self._API_URL}/open-proc/cmpt-2022/weathers/3/{wth3_id}/forecasts/{self.now_date}/{hour}')
        
        self.forecasts_1 = pd.DataFrame(self.forecasts_1)
        self.forecasts_2 = pd.DataFrame(self.forecasts_2)
        self.forecasts_3 = pd.DataFrame(self.forecasts_3)
        
    def forecast_time_change(self, time):
        time_format_forecaset = '%Y-%m-%dT%H:%M:%S%z'
        time_format_new = '%Y-%m-%d %H'
        time = datetime.strptime(time, time_format_forecaset) + timedelta(hours = 9)
        return time.strftime(time_format_new)  
    
    def change_time(self):
        pd.set_option('mode.chained_assignment', None)
        for i in range(len(self.forecasts_1)):
            new_time = self.forecast_time_change(self.forecasts_1.loc[i, 'time'])
            self.forecasts_1.loc[i, 'time'] = new_time
        for i in range(len(self.forecasts_2)):
            new_time = self.forecast_time_change(self.forecasts_2.loc[i, 'time'])
            self.forecasts_2.loc[i, 'time'] = new_time
        # for i in range(12):
            # new_time = forecast_time_change(self.forecasts_3.loc[i, 'time'])
            # self.forecasts_3.loc[i, 'time'] = new_time
    
    def refer_site(self):
        num_id = 0
        self.cur_wth_dist_1 = self.sites[self.sites['id']==num_id]['wth1_dist'].values[0]
        self.cur_wth_dist_2 = self.sites[self.sites['id']==num_id]['wth2_dist'].values[0]
        # self.cur_wth_dist_3 = self.sites[self.sites['id']==num_id]['wth3_dist'].values[0]
        self.cur_capacity = self.sites[self.sites['id']==num_id]['capacity']
    
    def interpolate(self):
        self.new = pd.DataFrame()
        for i in range(len(self.forecasts_1)):
            if self.forecasts_1['time'][i] == '{} 01'.format(self.pred_date):
                self.start = i
                break
                
        for i in range(self.start, self.start + 24):
            time = self.forecasts_1['time'][i]
            hour = self.forecasts_1['time'][i]
            hour = datetime.strptime(hour, '%Y-%m-%d %H')
            hour = int(hour.strftime('%H'))
            
            dew_point = self.forecasts_1['dew_point'][i]
            uv_idx = self.forecasts_1['uv_idx'][i]
            ceiling = self.forecasts_1['ceiling'][i]
            # pressure = self.forecasts_1['pressure'][i]
            
            
            # temperature = (self.forecasts_1[i]['temperature'].values[0] / self.cur_wth_dist_1 + self.forecasts_2[i]['temperature'].values[0] / self.cur_wth_dist_2 + self.forecasts_3[i]['temperature'].values[0] / self.cur_wth_dist_3 ) / ( 1/self.cur_wth_dist_1 + 1/self.cur_wth_dist_2 + 1/self.cur_wth_dist_3)
            # humidity = (self.forecasts_1[i]['humidity'].values[0] / self.cur_wth_dist_1 + self.forecasts_2[i]['humidity'].values[0] / self.cur_wth_dist_2 + self.forecasts_3[i]['humidity'].values[0] / self.cur_wth_dist_3 ) / ( 1/self.cur_wth_dist_1 + 1/self.cur_wth_dist_2 + 1/self.cur_wth_dist_3)
            # wind_dir = (self.forecasts_1[i]['wind_dir'].values[0] / self.cur_wth_dist_1 + self.forecasts_2[i]['wind_dir'].values[0] / self.cur_wth_dist_2 + self.forecasts_3[i]['wind_dir'].values[0] / self.cur_wth_dist_3 ) / ( 1/self.cur_wth_dist_1 + 1/self.cur_wth_dist_2 + 1/self.cur_wth_dist_3)
            # wind_spd = (self.forecasts_1[i]['wind_spd'].values[0] / self.cur_wth_dist_1 + self.forecasts_2[i]['wind_spd'].values[0] / self.cur_wth_dist_2 + self.forecasts_3[i]['wind_spd'].values[0] / self.cur_wth_dist_3 ) / ( 1/self.cur_wth_dist_1 + 1/self.cur_wth_dist_2 + 1/self.cur_wth_dist_3)
            # precip_1h = (self.forecasts_1[i]['precip_1h'].values[0] / self.cur_wth_dist_1 + self.forecasts_2[i]['precip_1h'].values[0] / self.cur_wth_dist_2 + self.forecasts_3[i]['precip_1h'].values[0] / self.cur_wth_dist_3 ) / ( 1/self.cur_wth_dist_1 + 1/self.cur_wth_dist_2 + 1/self.cur_wth_dist_3)
            temperature = (self.forecasts_1['temperature'][i] / self.cur_wth_dist_1 + self.forecasts_2['temperature'][i] / self.cur_wth_dist_2 ) / ( 1/self.cur_wth_dist_1 + 1/self.cur_wth_dist_2 )
            humidity = (self.forecasts_1['humidity'][i] / self.cur_wth_dist_1 + self.forecasts_2['humidity'][i] / self.cur_wth_dist_2 ) / ( 1/self.cur_wth_dist_1 + 1/self.cur_wth_dist_2 )
            wind_dir = (self.forecasts_1['wind_dir'][i] / self.cur_wth_dist_1 + self.forecasts_2['wind_dir'][i] / self.cur_wth_dist_2 ) / ( 1/self.cur_wth_dist_1 + 1/self.cur_wth_dist_2 )
            wind_spd = (self.forecasts_1['wind_spd'][i] / self.cur_wth_dist_1 + self.forecasts_2['wind_spd'][i] / self.cur_wth_dist_2 ) / ( 1/self.cur_wth_dist_1 + 1/self.cur_wth_dist_2 )
            precip_1h = (self.forecasts_1['precip_1h'][i] / self.cur_wth_dist_1 + self.forecasts_2['precip_1h'][i] / self.cur_wth_dist_2 ) / ( 1/self.cur_wth_dist_1 + 1/self.cur_wth_dist_2 )
            
            cloudiness = (self.forecasts_1['cloudiness'][i] / self.cur_wth_dist_1 + self.forecasts_2['cloudiness'][i] / self.cur_wth_dist_2 ) / ( 1/self.cur_wth_dist_1 + 1/self.cur_wth_dist_2 )
            
            new = pd.DataFrame({'id': self.cur_id, 'time': time, 'hour': hour, 'temperature': temperature, 'humidity': humidity, 'wind_dir': wind_dir, 'wind_spd': wind_spd, 'precip_1h': precip_1h, 'cloudiness': cloudiness, 'dew_point': dew_point, 'uv_idx': uv_idx, 'ceiling': ceiling, 'amount': [0]})
            
            self.new = self.new.append(new, ignore_index = True)
    
    def main(self):
        self.get_site()
        self.get_forecasts()
        self.change_time()
        self.refer_site()
        self.interpolate()
        
        return self.new