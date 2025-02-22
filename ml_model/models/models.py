import torch
import torch.nn as nn


# For adding and subtraction
class TwoInputNN(nn.Module):
    def __init__(self, input_dim1, input_dim2, output_dim):
        super(TwoInputNN, self).__init__()
        self.fc = nn.Linear(input_dim1 + input_dim2, output_dim,bias=False)  # Linear layer

    def forward(self, x1, x2):
        x = torch.cat((x1, x2), dim=-1)  # Concatenate along the last dimension
        return self.fc(x)



# === Example usage below ===
# input_dim1, input_dim2, output_dim = 3, 2, 1
# model = TwoInputNN(input_dim1, input_dim2, output_dim)

# x1 = torch.randn(5, input_dim1)  # Batch of 5 samples, each with input_dim1 features
# x2 = torch.randn(5, input_dim2)  # Batch of 5 samples, each with input_dim2 features
# output = model(x1, x2)
# print(output)
