import torch
from torch import nn
import torch.optim as optim
from Data_Loading import trainloader
from Data_Loading import valloader
from Model_Construct import model

# Model Training
loss_fn = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Store the training loss and the accuracy
training_losses = []
training_accuracy = []

# Store the validation loss and the accuracy
validation_losses = []
validation_accuracy = []

epochs = 100
for epoch in range(epochs):
    model.train()
    training_loss = 0.0
    correct = 0  # 예측값이 맞은 횟수
    total = 0

    # x_train is input data for the batch, y_train is the labels
    for i, (x_train, y_train) in enumerate(trainloader):
        input = x_train.transpose(1, 2)
        output = model(input)  # Output shape: torch.Size([64, 2])
        loss = loss_fn(output, y_train)

        # Add L2 regularization
        l2_reg = torch.tensor(0.)
        for param in model.parameters():
            l2_reg += torch.norm(param)
        loss += 0.001 * l2_reg

        # Back propagation - gradients are calculated and the optimizer updates
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Calculate training loss and accuracy
        training_loss += loss.item() * input.size(0)  # multiply the loss with the batch size
        _, predicted = torch.max(output.data,
                                 1)  # 0은 행 (세로), 1은 열 (가로) 마다 최댓값의 위치를 예측값으로 사용하겠다는 의미! * 원래 torch.max 는 최댓값, 최댓값의 위치를 산출해주는데, 최댓값은 필요없으므로 _ 로 저장 x
        total += y_train.size(0)  # Total number of predictions
        correct += (predicted == y_train).sum().item()  # 예측값과 라벨이 맞을때의 개수 * item()이 없으면 tensor(64) 라고 나옴.

    # Print training statistics
    epoch_loss = training_loss / len(
        trainloader.dataset)  # Training loss is calculated by dividing the cumulative loss by the total number of data points in the training dataset
    epoch_acc = 100. * correct / total

    # Store the training loss and the accuracy
    training_losses.append(epoch_loss)
    training_accuracy.append(epoch_acc)

    # validation
    model.eval()
    validation_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for i, (x_val, y_val) in enumerate(valloader):
            input = x_val.transpose(1, 2)
            output = model(input)
            loss = loss_fn(output, y_val)

            # Calculate validation loss and accuracy
            validation_loss += loss.item() * input.size(0)
            _, predicted = torch.max(output.data, 1)
            total += y_val.size(0)
            correct += (predicted == y_val).sum().item()

    # Calculate validation loss and accuracy
    epoch_val_loss = validation_loss / len(valloader.dataset)
    epoch_val_acc = 100. * correct / total

    # Store the validation loss and the accuracy
    validation_losses.append(epoch_val_loss)
    validation_accuracy.append(epoch_val_acc)

    print(
        f'Epoch [{epoch + 1}/{epochs}], Training Loss: {epoch_loss:.4f}, Validation Loss: {epoch_val_loss:.4f}, Training Accuracy: {epoch_acc:.2f}%, Validation Accuracy: {epoch_val_acc:.2f}%')

