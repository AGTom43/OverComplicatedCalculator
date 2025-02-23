import ast
import operator
import pickle
import numpy as np

operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.UAdd: operator.pos,
        ast.USub: operator.neg
    }

def load_pickle(filename):
    with open(filename, 'rb') as handle:
        unserialized_data = pickle.load(handle)
        return unserialized_data
    
mult_model = load_pickle("C:/Users/akhil/Documents/Hack Day 2025/project/ml_model/models/add4.pkl")
add_model = load_pickle('C:/Users/akhil/Documents/Hack Day 2025/project/ml_model/models/add16.pkl')


def manual_predict(model, x):
    layer_values = [x.T]
    
    weights = model.coefs_
    biass = model.intercepts_
        
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))
    
    if model.activation == 'logistic':
        A = sigmoid
    else:
        A = lambda x: x * (x > 0)
    
    for W, b in zip(weights, biass):
        if len(b) == 1:
            x = x@W + b
        else:
            x = A(x@W + b)
        layer_values.append(x)
    
    return layer_values

def modify_layer(layer, goal = (8,8,8)):
    if layer == []:
        return layer
    
    new_layer = [layer[0].tolist()]
    for i in range(len(goal)):
        current_goal = goal[i]
        current_layer = layer[i+1]
        
        _layer = current_layer.reshape((-1, current_layer.shape[1] // current_goal))
        _layer = np.mean(_layer, axis = 1)
        
        new_layer.append(_layer.tolist())
    
    new_layer.append(layer[-1].tolist())
    
    return new_layer

def eval_nn(node):
    results = []
    layers = []
    def evaluate_nn(node):
        if isinstance(node, ast.Num):  # Numbers
            return node.n
        elif isinstance(node, ast.BinOp):  # Binary operations (e.g., +, -, *, /)
            left = evaluate_nn(node.left)
            right = evaluate_nn(node.right)
            
            if type(node.op) == ast.Add:
                print(left, right)
                if abs(left) < 16 and abs(right) < 16:
                    x = np.array([[left, right]])
                    layer = manual_predict(mult_model, x)
                    result = mult_model.predict(x)[0]
                else:
                    x = np.array([[left, right]])
                    layer = manual_predict(add_model, x)
                    result = add_model.predict(x)[0]
            elif type(node.op) == ast.Sub:
                if abs(left) < 16 and abs(right) < 16:
                    x = np.array([[left, -right]])
                    layer = manual_predict(mult_model, x)
                    result = mult_model.predict(x)[0]
                else:
                    x = np.array([[left, -right]])
                    layer = manual_predict(add_model, x)
                    result = add_model.predict(x)[0]
            elif type(node.op) == ast.Mult:
                sign = np.product(np.sign([left, right]))
                x = np.log(np.abs([[left, right]]))
                layer = manual_predict(mult_model, x)
                result = mult_model.predict(x)[0]
                result = sign * np.exp(result)
            elif type(node.op) == ast.Div:
                #Assume nonzero right
                sign = np.product(np.sign([left, right]))
                x = np.array([[np.log(abs(left)), -np.log(abs(right))]])
                layer = manual_predict(mult_model, x)
                result = mult_model.predict(x)[0]
                result = sign * np.exp(result)
            else:
                result = operators[type(node.op)](left, right)
                layer = []
            results.append(result)
            layers.append(layer)
            return result
        elif isinstance(node, ast.UnaryOp):  # Unary operations (e.g., -3, +4)
            operand = evaluate_nn(node.operand)
            return operators[type(node.op)](operand)
        else:
            raise ValueError("Unsupported expression")
    tree = evaluate_nn(node)
    return results, layers

# input tree.body
def eval_normal(node):
    results = []
    def evaluate_normal(node):
        if isinstance(node, ast.Num):  # Numbers
            return node.n
        elif isinstance(node, ast.BinOp):  # Binary operations (e.g., +, -, *, /)
            left = evaluate_normal(node.left)
            right = evaluate_normal(node.right)
            results.append(operators[type(node.op)](left, right))
            return operators[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):  # Unary operations (e.g., -3, +4)
            operand = evaluate_normal(node.operand)
            return operators[type(node.op)](operand)
        else:
            raise ValueError("Unsupported expression")
    result = evaluate_normal(node)
    return results

def parse_tree(expression):
    tree = ast.parse(expression, mode='eval')
    return tree

def dump_tree(tree):
    return ast.dump(tree, annotate_fields=False).replace(', None', '')

def clean_tree_dump(text):
    i = 0
    while i < len(text):
        pass
        

#TODO: Change here
expression = "10*3+5-2"
def get_results(expression):
    print("hello")
    tree = parse_tree(expression)
    print(tree)
    results, layers = eval_nn(tree.body)

    print(results, layers)
    
    return eval_normal(tree.body), results, dump_tree(tree), [modify_layer(l) for l in layers]
