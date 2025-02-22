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


def transform_unary(node):
    """Convert UnaryOp nodes into a single Constant node with positive/negative values."""
    if isinstance(node, ast.UnaryOp) and isinstance(node.operand, ast.Constant):
        value = node.operand.value
        if isinstance(node.op, ast.UAdd):  # Unary plus (+)
            return ast.Constant(value=+value)
        elif isinstance(node.op, ast.USub):  # Unary minus (-)
            return ast.Constant(value=-value)
    return node  # Return unchanged if not a unary operation

class UnaryTransformer(ast.NodeTransformer):
    """AST Transformer that replaces UnaryOp with direct Constant values."""
    
    def visit_UnaryOp(self, node):
        return transform_unary(self.visit(node.operand))

    def visit_BinOp(self, node):
        """Ensure left and right operands are visited and transformed."""
        node.left = self.visit(node.left)
        node.right = self.visit(node.right)
        return node

def parse_and_transform(expression):
    """Parse the expression and transform unary operators into constants."""
    tree = ast.parse(expression, mode="eval")
    transformer = UnaryTransformer()
    transformed_tree = transformer.visit(tree)
    return transformed_tree

def prettify(ast_tree_str, indent=4):
    ret = []
    stack = []
    in_string = False
    curr_indent = 0

    for i in range(len(ast_tree_str)):
        char = ast_tree_str[i]
        if in_string and char != '\'' and char != '"':
            ret.append(char)
        elif char == '(' or char == '[':
            ret.append(char)

            if i < len(ast_tree_str) - 1:
                next_char = ast_tree_str[i+1]
                if next_char == ')' or next_char == ']':
                    curr_indent += indent
                    stack.append(char)
                    continue

            print(''.join(ret))
            ret.clear()

            curr_indent += indent
            ret.append(' ' * curr_indent)
            stack.append(char)
        elif char == ',':
            ret.append(char)

            print(''.join(ret))
            ret.clear()
            ret.append(' ' * curr_indent)
        elif char == ')' or char == ']':
            ret.append(char)
            curr_indent -= indent
            stack.pop()
        elif char == '\'' or char == '"':

            if (len(ret) > 0 and ret[-1] == '\\') or (in_string and stack[-1] != char):
                ret.append(char)
                continue

            if len(stack) > 0 and stack[-1] == char:
                ret.append(char)
                in_string = False
                stack.pop()
                continue

            in_string = True
            ret.append(char)
            stack.append(char)
        elif char == ' ':
            pass
        else:
            ret.append(char)

    print(''.join(ret).strip(',\nNone'))
# Example usage

#TODO: Change here
expression = "-2 + +3 * -4"
transformed_ast = parse_and_transform(expression)

# Print transformed AST
print(prettify(ast.dump(transformed_ast, annotate_fields=False)))
  
