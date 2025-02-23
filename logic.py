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
    
mult_model = load_pickle('ml_model/models/add4.pkl')
add_model = load_pickle('ml_model/models/add16.pkl')

def eval_nn(node):
    results = []
    def evaluate_nn(node):
        if isinstance(node, ast.Num):  # Numbers
            return node.n
        elif isinstance(node, ast.BinOp):  # Binary operations (e.g., +, -, *, /)
            left = evaluate_nn(node.left)
            right = evaluate_nn(node.right)
            
            if type(node.op) == ast.Add:
                if abs(left) < 16 and abs(right) < 16:
                    result = mult_model.predict([[left, right]])[0]
                else:
                    result = add_model.predict([[left, right]])[0]
            elif type(node.op) == ast.Sub:
                if abs(left) < 16 and abs(right) < 16:
                    result = mult_model.predict([[left, -right]])[0]
                else:
                    result = add_model.predict([[left, -right]])[0]
            elif type(node.op) == ast.Mult:
                sign = np.product(np.sign([left, right]))
                result = mult_model.predict(np.log(np.abs([[left, right]])))[0]
                result = sign * np.exp(result)
            elif type(node.op) == ast.Div:
                #Assume nonzero right
                sign = np.product(np.sign([left, right]))
                X = [[np.log(abs(left)), -np.log(abs(right))]]
                result = sign * np.exp(mult_model.predict(X))[0]
            else:
                result = operators[type(node.op)](left, right)
            results.append(result)
            return result
        elif isinstance(node, ast.UnaryOp):  # Unary operations (e.g., -3, +4)
            operand = evaluate_nn(node.operand)
            return operators[type(node.op)](operand)
        else:
            raise ValueError("Unsupported expression")
    tree = evaluate_nn(node)
    return results

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
        
expression = "10*3+5-2"
def get_results(expression):
    tree = parse_tree(expression)
    
    return eval_normal(tree.body), eval_nn(tree.body), dump_tree(tree)
