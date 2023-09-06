from utils.cnn import *
from utils.data_loader import *

import random
import time

class train_model():
    
    def __init__(self, opt, result_dir, x_data, y_data):
        self.opt = opt
        self.result_dir = result_dir
        self.x_data = x_data
        self.y_data = y_data
                 
    def load_data(self):
        self.train_dl, self.valid_dl = to_tensor(self.opt, self.x_data, self.y_data).main()
        
    def train(self):
        self.load_data()
        
        timestr = time.strftime("%Y%m%d-%H%M%S")
        os.mkdir(os.path.join(self.result_dir, timestr))
        time_dir = os.path.join(self.result_dir, timestr)
        
        
        for i in range(self.opt.iter):
            
            random_seed = i
            torch.manual_seed(random_seed)
            torch.cuda.manual_seed(random_seed)
            # torch.cuda.manual_seed_all(random_seed) # if use multi-GPU
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
            np.random.seed(random_seed)
            random.seed(random_seed)

            
            os.mkdir(os.path.join(time_dir, '{}'.format(random_seed+1)))
            self.final_dir = os.path.join(time_dir, '{}'.format(random_seed+1))
            
            CNN(self.opt, self.train_dl, self.valid_dl, self.final_dir, random_seed).train()
            
            