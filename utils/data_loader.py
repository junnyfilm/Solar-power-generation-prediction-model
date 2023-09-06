from sklearn.model_selection import train_test_split
from torch_snippets import *
from sklearn.preprocessing import StandardScaler

class POSTECH_Dataset(Dataset):
    def __init__(self, x, y):
        self.x, self.y = x, y
        
    def __len__(self):
        return len(self.x)
    
    def __getitem__(self, ix):
        x, y = self.x[ix], self.y[ix]
        return x.to(device).float(), y.to(device).float()

class to_tensor():
    def __init__(self, opt, x_data, y_data):
        self.opt = opt
        self.x = x_data
        self.y = y_data
    
    def data_split(self):
        self.x_train, self.x_valid, self.y_train, self.y_valid = train_test_split(self.x, self.y, train_size = self.opt.train_size)
        
    def scaler(self):
        scalers = {}
        for i in range(self.x_train.shape[1]):
            scalers[i] = StandardScaler()
            self.x_train[:, i, :] = scalers[i].fit_transform(self.x_train[:, i, :]) 
        for i in range(self.x_valid.shape[1]):
            self.x_valid[:, i, :] = scalers[i].transform(self.x_valid[:, i, :]) 
        
        # self.x_train = scaler.fit_transform(self.x_train)
        # self.x_valid = scaler.fit_transform(self.x_valid)
        
        
    def to_tensor(self):
        self.x_train = torch.tensor(self.x_train)
        self.y_train = torch.tensor(self.y_train)
        self.x_valid = torch.tensor(self.x_valid)
        self.y_valid = torch.tensor(self.y_valid)
        
        # self.x_train = torch.unsqueeze(self.x_train, 1)
        self.x_train = self.x_train.permute(0, 2, 1)
        self.y_train = torch.squeeze(self.y_train)
        # self.x_valid = torch.unsqueeze(self.x_valid, 1)
        self.x_valid = self.x_valid.permute(0, 2, 1)
        self.y_valid = torch.squeeze(self.y_train)
        
    def to_dataloader(self):
        self.train = POSTECH_Dataset(self.x_train, self.y_train)
        self.valid = POSTECH_Dataset(self.x_train, self.y_valid)
        self.train_dl = DataLoader(self.train, batch_size=self.opt.batch_size, shuffle=True)
        self.valid_dl = DataLoader(self.valid, batch_size=self.opt.batch_size, shuffle=False)
        
    def main(self):
        self.data_split()
        self.scaler()
        self.to_tensor()
        self.to_dataloader()
        
        return self.train_dl, self.valid_dl
    
class to_tensor_test():
    def __init__(self, opt, x_data, y_data, x_test, y_test):
        self.opt = opt
        self.x = x_data
        self.y = y_data
        self.x_test = x_test
        self.y_test = y_test
    
    def scaler(self):
        scalers = {}
        for i in range(self.x.shape[1]):
            scalers[i] = StandardScaler()
            self.x[:, i, :] = scalers[i].fit_transform(self.x[:, i, :]) 
        for i in range(self.x_test.shape[1]):
            self.x_test[:, i, :] = scalers[i].transform(self.x_test[:, i, :]) 
    
    def to_tensor(self):
        self.x_test = torch.tensor(self.x_test)
        self.y_test = torch.tensor(self.y_test)
        
        # self.x_test = torch.unsqueeze(self.x_test, 1)
        self.x_test = self.x_test.permute(0, 2, 1)
        self.y_test = torch.squeeze(self.y_test)
        
    def to_dataloader(self):
        self.test = POSTECH_Dataset(self.x_test, self.y_test)
        self.test_dl = DataLoader(self.test, batch_size=self.opt.batch_size, shuffle=False)
        
    def main(self):
        self.scaler()
        self.to_tensor()
        self.to_dataloader()
        
        return self.test_dl