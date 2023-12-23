import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from datetime import datetime

# Check if GPU is available and use it if possible
device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')
print(f"Using {device} device")

# Read and preprocess the dataset
file_path = '/Users/jorge/Downloads/players-data-sofascore.csv'

# Read CSV first row to populate column names
with open(file_path, 'r', encoding="utf-8-sig") as f:
    column_names = f.readline().strip().split(',')
    f.close()

# Read the dataset
raw_dataset = pd.read_csv(file_path, names=column_names, comment='\t', sep=',', skipinitialspace=True, low_memory=False)

# Convert non-numeric columns to numeric, handling errors
for col in raw_dataset.columns:
    raw_dataset[col] = pd.to_numeric(raw_dataset[col], errors='coerce')

# Fill missing (NaN) values with the mean of each column
dataset = raw_dataset.fillna(raw_dataset.mean())

unecessary_columns = ['player_id', 'player_name', 'player_slug', 'player_userCount', 'team_name', 'team_slug']

# Drop unnecessary columns
dataset = dataset.drop(columns=unecessary_columns)

# Split the dataset
train_dataset, test_dataset = train_test_split(dataset, test_size=0.2, random_state=0)
train_labels = train_dataset.pop('rating')
test_labels = test_dataset.pop('rating')

# Convert to PyTorch tensors
train_data = torch.tensor(train_dataset.values, dtype=torch.float32).to(device)
train_labels = torch.tensor(train_labels.values, dtype=torch.float32).view(-1, 1).to(device)
test_data = torch.tensor(test_dataset.values, dtype=torch.float32).to(device)
test_labels = torch.tensor(test_labels.values, dtype=torch.float32).view(-1, 1).to(device)

# Create data loaders
train_loader = DataLoader(TensorDataset(train_data, train_labels), batch_size=32, shuffle=True)
test_loader = DataLoader(TensorDataset(test_data, test_labels), batch_size=32, shuffle=False)

# Define the model
class NeuralNetwork(nn.Module):
    def __init__(self, input_size):
        super(NeuralNetwork, self).__init__()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        return self.linear_relu_stack(x)

model = NeuralNetwork(len(train_dataset.keys())).to(device)

# Define the loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.RMSprop(model.parameters(), lr=0.001)

# Train the model
def train(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    model.train()
    for batch, (X, y) in enumerate(dataloader):
        # Compute prediction and loss
        pred = model(X)
        loss = loss_fn(pred, y)

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

def test(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    test_loss, correct = 0, 0
    with torch.no_grad():
        for X, y in dataloader:
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
    test_loss /= num_batches
    print(f"Test Error: \n Avg loss: {test_loss:>8f} \n")

# Training loop
EPOCHS = 10
for t in range(EPOCHS):
    train(train_loader, model, criterion, optimizer)
    test(test_loader, model, criterion)


print(model)

# Save the model
current_date = datetime.now()
date_str = current_date.strftime("%m%d")
model_filename = f"SofaScoreTFDL{date_str}.pt"
torch.save(model.state_dict(), model_filename)
print(f"Model saved as {model_filename}")

# Prediction and evaluation
model.eval()
with torch.no_grad():
    predictions = model(test_data)
    mse = criterion(predictions, test_labels).item()
    rmse = np.sqrt(mse)

print(f"RMSE: {rmse}")

# Flatten the predictions and test_labels for comparison
predicted_ratings = predictions.view(-1).cpu().numpy()
real_ratings = test_labels.view(-1).cpu().numpy()

# Create a DataFrame for comparison
ratings_comparison = pd.DataFrame({
    'real_rating': real_ratings,
    'predicted_rating': predicted_ratings
})

# Save to CSV
output_file_path = 'ratings_comparison.csv'
ratings_comparison.to_csv(output_file_path, index=False)

print(f"File saved with real and predicted ratings to {output_file_path}")
