from utils.test_prep import *
from utils.data_loader import *

import pandas as pd
import numpy as np
import requests
import json

class eval_test():
    def __init__(self, opt, final_model_dir, api_key, now_date, now_hour, pred_date):
        self.opt = opt
        self.final_model_dir = final_model_dir
        self.api_key = api_key
        self.now_date = now_date
        self.now_hour = now_hour
        self.pred_date = pred_date
        
    def load_test_file(self):
        prep_file = test_api_load(self.api_key, self.now_date, self.now_hour, self.pred_date).main()
        self.x_test = np.expand_dims(prep_file.iloc[:, 3:12].to_numpy(), 0)
        self.y_test = np.expand_dims(prep_file.iloc[:, 12].to_numpy(), 0)
        
    def change_tensor(self):
        x_data = np.load('x_data.npy')
        y_data = np.load('y_data.npy')
        self.test_dl = to_tensor_test(self.opt, x_data, y_data, self.x_test, self.y_test).main()
        
    def model_eval(self):
        self.final_pred = []
        for i in range(self.opt.iter):
            model = torch.load(self.final_model_dir + '/{}/model.pt'.format(i+1))
            model.eval()
            for ix, batch in enumerate(self.test_dl):
                x, y = batch
                pred = model(x)
                
                self.final_pred.append(pred.cpu().detach().numpy())
                
        self.final_pred = np.array(self.final_pred) * 472.39
        
        self.final_pred = np.squeeze(self.final_pred)
        
    def main(self):
        self.load_test_file()
        self.change_tensor()
        self.model_eval()

    def load_real_gen(self):
        self.real_gen = test_api_load(self.api_key, self.now_date, self.now_hour, self.pred_date)._get_pv_gens()
        self.real_gen = pd.DataFrame(self.real_gen)
        self.real_gen = self.real_gen[self.real_gen['pv_id'] == 0]['amount'].values
        return self.real_gen
    
    def compare_plot(self):
        self.main()
        self.load_real_gen()
        pred_mean = np.mean( self.final_pred, axis = 0)
        pred_std = np.std( self.final_pred, axis = 0)
        arr = []
        for i in range(len( self.final_pred[0])):
            arr_ = [i, pred_mean[i].item(), pred_std[i].item()]
            arr.append(arr_)
        pred_arr = np.array(arr).T
        
        plt.plot(pred_mean, 'black')
        plt.fill_between(pred_arr[0][:], pred_arr[1][:]-pred_arr[2][:], pred_arr[1][:]+pred_arr[2][:], fc="blue", alpha=0.5, zorder=2.4)
        plt.plot(self.real_gen, 'r--')
        
        plt.title('{}'.format(self.pred_date))
        
        plt.savefig(self.final_model_dir+'/{}.png'.format(self.pred_date), dpi=300)
        
        plt.show()
        
    def calculate_bid(self):
        self.main()
        pred_mean = np.mean( self.final_pred, axis = 0)
        pred_std = np.std( self.final_pred, axis = 0)
        
        self.bid = [{'upper': pred_mean[0] + pred_std[0], 'lower': pred_mean[0] - pred_std[0]},
                    {'upper': pred_mean[1] + pred_std[1], 'lower': pred_mean[1] - pred_std[1]},
                    {'upper': pred_mean[2] + pred_std[2], 'lower': pred_mean[2] - pred_std[2]},
                    {'upper': pred_mean[3] + pred_std[3], 'lower': pred_mean[3] - pred_std[3]},
                    {'upper': pred_mean[4] + pred_std[4], 'lower': pred_mean[4] - pred_std[4]},
                    {'upper': pred_mean[5] + pred_std[5], 'lower': pred_mean[5] - pred_std[5]},
                    {'upper': pred_mean[6] + pred_std[6], 'lower': pred_mean[6] - pred_std[6]},
                    {'upper': pred_mean[7] + pred_std[7], 'lower': pred_mean[7] - pred_std[7]},
                    {'upper': pred_mean[8] + pred_std[8], 'lower': pred_mean[8] - pred_std[8]},
                    {'upper': pred_mean[9] + pred_std[9], 'lower': pred_mean[9] - pred_std[9]},
                    {'upper': pred_mean[10] + pred_std[10], 'lower': pred_mean[10] - pred_std[10]},
                    {'upper': pred_mean[11] + pred_std[11], 'lower': pred_mean[11] - pred_std[11]},
                    {'upper': pred_mean[12] + pred_std[12], 'lower': pred_mean[12] - pred_std[12]},
                    {'upper': pred_mean[13] + pred_std[13], 'lower': pred_mean[13] - pred_std[13]},
                    {'upper': pred_mean[14] + pred_std[14], 'lower': pred_mean[14] - pred_std[14]},
                    {'upper': pred_mean[15] + pred_std[15], 'lower': pred_mean[15] - pred_std[15]},
                    {'upper': pred_mean[16] + pred_std[16], 'lower': pred_mean[16] - pred_std[16]},
                    {'upper': pred_mean[17] + pred_std[17], 'lower': pred_mean[17] - pred_std[17]},
                    {'upper': pred_mean[18] + pred_std[18], 'lower': pred_mean[18] - pred_std[18]},
                    {'upper': pred_mean[19] + pred_std[19], 'lower': pred_mean[19] - pred_std[19]},
                    {'upper': pred_mean[20] + pred_std[20], 'lower': pred_mean[20] - pred_std[20]},
                    {'upper': pred_mean[21] + pred_std[21], 'lower': pred_mean[21] - pred_std[21]},
                    {'upper': pred_mean[22] + pred_std[22], 'lower': pred_mean[22] - pred_std[22]},
                    {'upper': pred_mean[23] + pred_std[23], 'lower': pred_mean[23] - pred_std[23]},]
        
        for i in range(len(self.bid)):
            for j in ['upper', 'lower']:
                if self.bid[i][j] < 0:
                    self.bid[i][j] = 0
        
        # numpy float -> float
        for i in range(len(self.bid)):
            self.bid[i] = {k:float(v) for k,v in self.bid[i].items()}
        
        return self.bid
    
    def eval_score(self):
        self.main()
        self.load_real_gen()
        self.calculate_bid()
        
        TOTAL_CAPACITY = 472.39
        
        gens = self.real_gen
        sum_value: float = 0
        for idx, gen in enumerate(gens):
            util_errs = []

            bids = self.bid
            bid = bids[idx]
            real_gen = gens[idx]

            value = (
                abs((bid['upper'] + bid['lower']) / 2 - real_gen) / TOTAL_CAPACITY
                + (bid['upper'] - bid['lower']) / (2 * TOTAL_CAPACITY)
                + real_gen * (1 if bid['lower'] > real_gen or bid['upper'] < real_gen else 0) / TOTAL_CAPACITY
            )
            print(f'Idx({idx}) | '
                  f'Evaluation value: {value} (%) / '
                  f'Bid: {bid} (kWh) / '
                  f'Gen: {gen} (kWh)')
            sum_value += value

        print(f'Total Evaluation value: {sum_value} (KRW)')
    

    
    def prize_1st_bid(self):
        self.calculate_bid()

        amounts = self.bid
        
        _API_KEY = self.api_key
        
        success = requests.post(f'https://research-api.dershare.xyz/open-proc/cmpt-2022/bids', data=json.dumps(amounts), headers={
                                    'Authorization': f'Bearer {_API_KEY}'
                                }).json()
        print(success)