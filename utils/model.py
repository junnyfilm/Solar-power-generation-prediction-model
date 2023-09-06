from torch_snippets import *


class POSTECH_Model(nn.Module):
    def __init__(self):
        super(POSTECH_Model, self).__init__()
        
        
        # self.layer_1 = nn.Sequential(nn.Conv1d(9, 16, kernel_size=3, stride=1, padding=1),
        #                              nn.BatchNorm1d(16),
        #                              nn.ReLU(),
        #                              nn.Conv1d(16, 32, kernel_size=3, stride=1, padding=1),
        #                              nn.BatchNorm1d(32),
        #                              nn.ReLU(),
        #                              nn.Conv1d(32, 64, kernel_size=3, stride=1, padding=1),
        #                              nn.BatchNorm1d(64),
        #                              nn.ReLU()
        #                              )
        
        self.conv1 = nn.Sequential(nn.Conv1d(9, 32, kernel_size=1, stride = 1, padding=0),
                                     nn.BatchNorm1d(32),
                                 nn.ReLU())
        self.conv2 = nn.Sequential(nn.Conv1d(9, 32, kernel_size=3, stride = 1, padding=1),
                                     nn.BatchNorm1d(32),
                                 nn.ReLU())
        self.conv3 = nn.Sequential(nn.Conv1d(9, 32, kernel_size=5, stride = 1, padding=2),
                                     nn.BatchNorm1d(32),
                                 nn.ReLU())
        
        
        self.bn_concat = nn.BatchNorm1d(9+32+32+32)

        self.bottle_1 = nn.Sequential(nn.Conv1d(9+32+32+32,256,kernel_size=3, stride=1, bias=False),
                                      nn.BatchNorm1d(256),
                                 nn.ReLU())
        
        self.bottle_2 = nn.Sequential(nn.Conv1d(256,128,kernel_size=3, stride=1, bias=False),
                                      nn.BatchNorm1d(128),
                                 nn.ReLU())
        self.bottle_3 = nn.Sequential(nn.Conv1d(128,64,kernel_size=3, stride=1, bias=False),
                                      nn.BatchNorm1d(64),
                                 nn.ReLU())

        
        
        self.lstm = nn.LSTM(
            input_size=18,
            hidden_size=128,
            num_layers=2,
            batch_first=True
        )


        
        self.fc = nn.Sequential(
                                nn.Linear(128, 64),
                                 nn.BatchNorm1d(64),
                                 nn.ReLU(),
                                 nn.Linear(64, 24),
                                 nn.ReLU()
                               )

    def forward(self, x):
        x1 = self.conv1(x)
        x2 = self.conv2(x)
        x3 = self.conv3(x)
        
        feature=torch.cat((x1,x2,x3,x),dim=1)
        feature = self.bn_concat(feature)
        feature = self.bottle_1(feature)
        feature = self.bottle_2(feature)
        feature = self.bottle_3(feature)

        # x = x.transpose(0, 1) # (batch, seq, params) -> (seq, batch, params)
        # self.lstm.flatten_parameters
        hidden,_ = self.lstm(feature)
        x=hidden[:,-1,:]
        x = self.fc(x)
        # print(x.shape)
        return x
    
# https://coding-yoon.tistory.com/190


# class POSTECH_Model(nn.Module):
#     def __init__(self):
#         super(POSTECH_Model, self).__init__()
        
        
        
#         self.layer_1 = nn.Sequential(nn.Conv1d(9, 9, kernel_size=3, stride=1, padding=1),
#                                      nn.BatchNorm1d(9),
#                                      nn.ReLU(),
#                                      )


#         self.layer_2 = nn.Sequential(nn.Conv1d(9, 16, kernel_size=3, stride=1, padding=1),
#                                      nn.BatchNorm1d(16),
#                                      nn.ReLU(),
#                                      nn.Conv1d(16, 16, kernel_size=3, stride=1, padding=1),
#                                      nn.BatchNorm1d(16),
#                                      nn.ReLU())
            
#         self.layer_3 = nn.Sequential(nn.Conv1d(16, 32, kernel_size=3, stride=1, padding=1),
#                                      nn.BatchNorm1d(32),
#                                      nn.ReLU(),
#                                      nn.Conv1d(32, 32, kernel_size=3, stride=1, padding=1),
#                                      nn.BatchNorm1d(32),
#                                      nn.ReLU(),
#                                      nn.Flatten()
#                                     )
        
#         self.fc = nn.Sequential(nn.Linear(24*32, 256),
#                                  nn.BatchNorm1d(256),
#                                  nn.ReLU(),
#                                  nn.Linear(256, 100),
#                                  nn.BatchNorm1d(100),
#                                  nn.ReLU(),
#                                  nn.Linear(100, 100),
#                                  nn.BatchNorm1d(100),
#                                  nn.ReLU(),
#                                  nn.Linear(100, 24),
#                                  nn.ReLU()
#                                )

#     def forward(self, x):
#         print(x.shape)
#         x = self.layer_1(x)
#         x = self.layer_2(x)
#         x = self.layer_3(x)
#         x = self.fc(x)
#         print(x.shape)
#         return x
