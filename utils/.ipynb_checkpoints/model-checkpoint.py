from torch_snippets import *


class POSTECH_Model(nn.Module):
    def __init__(self):
        super(POSTECH_Model, self).__init__()
        self.layer_1 = nn.Sequential(nn.Conv1d(9, 9, kernel_size=3, stride=1, padding=1),
                                     nn.BatchNorm1d(9),
                                     nn.ReLU(),
                                     nn.Conv1d(9, 9, kernel_size=3, stride=1, padding=1),
                                     nn.BatchNorm1d(9),
                                     nn.ReLU())

        self.layer_2 = nn.Sequential(nn.Conv1d(9, 16, kernel_size=3, stride=1, padding=1),
                                     nn.BatchNorm1d(16),
                                     nn.ReLU(),
                                     nn.Conv1d(16, 16, kernel_size=3, stride=1, padding=1),
                                     nn.BatchNorm1d(16),
                                     nn.ReLU())
            
        self.layer_3 = nn.Sequential(nn.Conv1d(16, 32, kernel_size=3, stride=1, padding=1),
                                     nn.BatchNorm1d(32),
                                     nn.ReLU(),
                                     nn.Conv1d(32, 32, kernel_size=3, stride=1, padding=1),
                                     nn.BatchNorm1d(32),
                                     nn.ReLU(),
                                     nn.Flatten()
                                    )
        
        self.fc = nn.Sequential(nn.Linear(24*32, 256),
                                 nn.BatchNorm1d(256),
                                 nn.ReLU(),
                                 nn.Linear(256, 100),
                                 nn.BatchNorm1d(100),
                                 nn.ReLU(),
                                 nn.Linear(100, 100),
                                 nn.BatchNorm1d(100),
                                 nn.ReLU(),
                                 nn.Linear(100, 24),
                                 nn.ReLU()
                               )

    def forward(self, x):
        x = self.layer_1(x)
        x = self.layer_2(x)
        x = self.layer_3(x)
        x = self.fc(x)
        return x
