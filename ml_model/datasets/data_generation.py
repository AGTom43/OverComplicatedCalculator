import numpy as np

# multiply # add # division #s ubtract

def create_multiply_set(n: int) -> np.ndarray:
    number1 = np.random.uniform(low=1, high=10, size=n)
    number2 = np.random.uniform(low=1, high=10, size=n)
    multiplication = number1 * number2
    return np.vstack([number1,number2,multiplication]).T

def create_addition_set(n: int) -> np.ndarray:
    number1 = np.random.uniform(low=1, high=10, size=n)
    number2 = np.random.uniform(low=1, high=10, size=n)
    multiplication = number1 + number2
    return np.vstack([number1,number2,multiplication]).T

def create_subtraction_set(n: int) -> np.ndarray:
    number1 = np.random.uniform(low=1, high=10, size=n)
    number2 = np.random.uniform(low=1, high=10, size=n)
    multiplication = number1 - number2
    return np.vstack([number1,number2,multiplication]).T

def create_divide_set(n: int) -> np.ndarray:
    number1 = np.random.uniform(low=1, high=10, size=n)
    number2 = np.random.uniform(low=1, high=10, size=n)
    multiplication = number1 / number2
    return np.vstack([number1,number2,multiplication]).T


# create dataset
number_of_rows = 1000
path = '/home/seetvn/random_projects/hack_sussex/project/ml_model/datasets/'
n = 1000
while n > 0:
    mult_set = create_multiply_set(number_of_rows)
    np.savetxt(path + "multiply.csv", mult_set, delimiter=",", fmt="%.2f", header="Col1,Col2,Col3", comments="")

    add_set = create_addition_set(number_of_rows)
    np.savetxt(path + "add.csv", add_set, delimiter=",", fmt="%.2f", header="Col1,Col2,Col3", comments="")

    subtract_set = create_subtraction_set(number_of_rows)
    np.savetxt(path + "subtract.csv", subtract_set, delimiter=",", fmt="%.2f", header="Col1,Col2,Col3", comments="")

    division_set = create_divide_set(number_of_rows)
    np.savetxt(path + "divide.csv", division_set, delimiter=",", fmt="%.2f", header="Col1,Col2,Col3", comments="")
    n -= 1
print(f'generated dataset of size {n} for each file')