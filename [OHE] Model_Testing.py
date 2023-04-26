import torch
from Data_Loading import testloader
from Model_Construct import model
from Model_Training import loss_fn, training_losses, training_accuracy, validation_losses, validation_accuracy

# Set the model to evaluation mode
model.eval()

# Store the test loss and the accuracy
testing_losses = []
testing_accuracy = []

# Deactivate autograd for evaluation
with torch.no_grad():
    for x_test, y_test in testloader:
        # Transpose the input data
        input = x_test.transpose(1, 2)

        # Feed the input data to the model to get the output
        output = model(input)

        # Calculate the test loss and accuracy
        loss = loss_fn(output, y_test)
        testing_losses.append(loss.item())
        _, predicted = torch.max(output.data, 1)
        testing_accuracy.append((predicted == y_test).sum().item() / y_test.size(0) * 100)

    # Calculate the average test loss and accuracy
    avg_test_loss = sum(testing_losses) / len(testing_losses)
    avg_test_accuracy = sum(testing_accuracy) / len(testing_accuracy)

    # Print test statistics
    print(f'Average Test Loss: {avg_test_loss:.4f}, Average Test Accuracy: {avg_test_accuracy:.2f}%')

# Making Plot
import matplotlib.pyplot as plt

# Loss plot
plt.plot(training_losses, label='Training Loss')
plt.plot(validation_losses, label='validation Loss')
# plt.plot(testing_losses, label='Testing Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()

# Accuracy plotting
plt.plot(training_accuracy, label='Training Accuracy')
plt.plot(validation_accuracy, label='validation Accuracy')
# plt.plot(testing_accuracy, label='Testing Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

plt.plot(testing_losses, label='Testing Loss')
plt.show()
plt.plot(testing_accuracy, label='Testing accuracy')
plt.show()
