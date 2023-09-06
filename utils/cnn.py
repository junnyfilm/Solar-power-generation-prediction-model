from utils.model import *
import torch
import torch.nn as nn
from torch_snippets import *
from tqdm.notebook import tqdm

class CNN():  
    def __init__(self, opt, train_dl, valid_dl, save_dir, random_seed):
        self.opt = opt
        self.train_dl = train_dl
        self.valid_dl = valid_dl
        self.save_dir = save_dir
        self.random_seed = random_seed
    
    def train(self):
        
        best_loss = 10000
        
        dict_result = {
                       'y_loss': []
                      }
        
        print('---------------------------------------------------')
        print('Model: {}'.format(self.random_seed + 1))
        
        opt = self.opt

        
        self.model = POSTECH_Model().to(device)
        self.model.train()
        
        self.loss_mse = nn.MSELoss()

        self.optimizer = optim.Adam(list(self.model.parameters()), lr=opt.lr)
        self.scheduler = optim.lr_scheduler.LambdaLR(optimizer=self.optimizer, lr_lambda=lambda epoch: opt.lamda ** epoch)
        
        pbar = tqdm(range(opt.epochs), unit = 'epoch')
        
        for epoch in pbar:
            
            # Training
            
            for ix, batch in enumerate(iter(self.train_dl)):
                
                train_x, train_y = batch
                
                pred_y = self.model(train_x)

                # DANN
                loss_y = self.loss_mse(pred_y, train_y)

                self.optimizer.zero_grad()
                loss_y.backward()
                self.optimizer.step()
                 
                ##################### result_save ############################           
                dict_result['y_loss'].append(loss_y.item())
                ###############################################################
                
                pbar.set_postfix({'y_loss' : loss_y.item(), 'valid_loss' : best_loss})
                
            self.scheduler.step()
            valid_loss = self.valid_loss()
            
            if best_loss > valid_loss:
                best_loss = valid_loss
                
                torch.save(self.model, self.save_dir + '/model.pt')
                torch.save(self.model.state_dict(), self.save_dir + '/model_state_dict.pt')
       
        # Test set
    def valid_loss(self):
        self.model.eval()
        loss = []
        with torch.no_grad():
            for ix, batch in enumerate(iter(self.valid_dl)):
                x, y = batch
                pred = self.model(x)
                
                loss_y = self.loss_mse(pred, y)
                loss.append(loss_y.item())

        return np.mean(loss)
