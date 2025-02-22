from models.models import TwoInputNN
import torch as t
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from typing import Union, List

operation_types = {"+": "add.csv", "*": "multiply.csv", "-": "subtract.csv"}
operation_types_weights = {"*": "multiply", "+": "add", "-": "subtract"}


def get_data(file_path: str) -> Union[t.tensor, t.tensor, t.tensor]:
    df = pd.read_csv(file_path)
    # Extract individual columns
    col1 = t.tensor(df.iloc[:, 0].values, dtype=t.float32)  # First column
    col2 = t.tensor(df.iloc[:, 1].values, dtype=t.float32)  # Second column
    col3 = t.tensor(df.iloc[:, 2].values, dtype=t.float32)  # Third column
    return [col1, col2, col3]


def training_process(model: nn,
                     loss_function=nn.MSELoss(),
                     learning_rate=0.01,
                     file_path: str = None,
                     epochs: int = 30,
                     operation: str = None,
                     batch_size: int = 10) -> None:

    x1, x2, y = get_data(
        "/home/seetvn/random_projects/hack_sussex/project/ml_model/datasets/" + operation_types[operation])
    x1_train, x1_val, x1_test = x1[:600], x1[601:801], x1[:1000]
    x2_train, x2_val, x2_test = x2[:600], x2[601:801], x2[:1000]
    y_train, y_val, y_test = y[:600], y[601:801], y[:1000]

    x1_train = x1_train.view(-1, 1)  # Reshape to (600, 1)
    x2_train = x2_train.view(-1, 1)  # Reshape to (600, 1)
    y_train = y_train.view(-1, 1)   # Reshape to (600, 1)

    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    # Create DataLoader
    dataset = t.utils.data.TensorDataset(x1_train, x2_train, y_train)
    train_loader = t.utils.data.DataLoader(dataset, batch_size=batch_size)

    for i in range(epochs):
        total_loss = 0
        for x1_var, x2_var, y_var in train_loader:
            optimizer.zero_grad()
            output = model(x1_var, x2_var)
            # for v1,v2,o in zip(x1_var,x2_var,output):
            #     print(v1,v2,o)
            loss = loss_function(y_var, output)
            # Backward pass
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        # Print progress
        print(f"Epoch [{i + 1}, Loss: {total_loss / len(train_loader):.4f}")
        print(f"weights: {[weight for weight in model.parameters()]}")

    t.save(
        model.state_dict(), f"{
            operation_types_weights[operation]}_model_weights.pth")
    print("Model weights saved!")


# change sign for corresponding model
my_model = TwoInputNN(input_dim1=1, input_dim2=1, output_dim=1)
training_process(my_model, operation="-", epochs=100)
