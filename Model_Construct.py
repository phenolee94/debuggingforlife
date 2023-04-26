from torch import nn

class Binary_Fungi_Classifier(nn.Module):
    def __init__(self):
        super(Binary_Fungi_Classifier, self).__init__()
        # First layer
        # Input shape = (64, 4, 650)
        self.conv1 = nn.Conv1d(in_channels=4, out_channels=8, kernel_size=3, stride=1, padding=1)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool1d(kernel_size=2, stride=2)
        # Input shape = (64, 8, 325)
        self.dropout = nn.Dropout(p=0.25)
        self.fc = nn.Linear(8 * 325, 2)

    def forward(self, x):
        out = self.conv1(x)
        out = self.relu(out)
        out = self.pool(out)
        out = self.dropout(out)
        out = out.view(out.size(0), -1)  # flatten
        out = self.fc(out)
        return out

model = Binary_Fungi_Classifier()