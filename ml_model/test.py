from models.models import TwoInputNN
import torch as t


# Initialize the model with the correct input/output dimensions
my_model = TwoInputNN(input_dim1=1, input_dim2=1, output_dim=1)

# Load the saved model weights
my_model.load_state_dict(t.load("model_weights.pth"))

# Set model to evaluation mode (important for inference)
my_model.eval()

print("Model weights loaded successfully!")

random_1 = t.floor(t.rand((10,1)) * 10)
random_2 = t.floor(t.rand((10,1)) * 10)

solution = random_1 + random_2

for num1,num2,sol in zip(random_1,random_2,solution):
    output = my_model(num1,num2)
    print(f" {num1.item()} + {num2.item()} = {output.item()}  ({sol.item()})")
