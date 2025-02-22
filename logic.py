import ast
import operator


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

# input tree.body
def evaluate(node):
    if isinstance(node, ast.Num):  # Numbers
        return node.n
    elif isinstance(node, ast.BinOp):  # Binary operations (e.g., +, -, *, /)
        left = evaluate(node.left)
        right = evaluate(node.right)
        return operators[type(node.op)](left, right)
    elif isinstance(node, ast.UnaryOp):  # Unary operations (e.g., -3, +4)
        operand = evaluate(node.operand)
        return operators[type(node.op)](operand)
    else:
        raise ValueError("Unsupported expression")

def parse_tree(expression):
    tree = ast.parse(expression, mode='eval')
    return tree

def dump_tree(tree):
    ast.dump(tree, annotate_fields=False)
    return

#TODO: Change here
expression = "-2 + +3 * -4"
