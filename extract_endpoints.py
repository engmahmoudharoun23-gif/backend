import ast

class FunctionVisitor(ast.NodeVisitor):
    def __init__(self, target_endpoints):
        self.target_endpoints = target_endpoints
        self.code_snippets = []
        self.source_code = ""
        self.line_offsets = []

    def visit_AsyncFunctionDef(self, node):
        self.check_function(node)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.check_function(node)
        self.generic_visit(node)

    def check_function(self, node):
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute):
                if decorator.func.attr in ['get', 'post', 'put', 'delete']:
                    if decorator.args and isinstance(decorator.args[0], ast.Constant):
                        endpoint = decorator.args[0].value
                        if endpoint in self.target_endpoints:
                            start_line = node.lineno - 1
                            end_line = node.end_lineno
                            # Try to include decorators
                            if node.decorator_list:
                                start_line = node.decorator_list[0].lineno - 1
                            snippet = "\n".join(self.source_code.split("\n")[start_line:end_line])
                            self.code_snippets.append(f"Endpoint: {endpoint}\n{snippet}\n")

with open("server.py", "r", encoding="utf-8") as f:
    source_code = f.read()

targets = ["/safety-reports", "/notifications/pending-count", "/reports/pending-review-count"]
tree = ast.parse(source_code)
visitor = FunctionVisitor(targets)
visitor.source_code = source_code
visitor.visit(tree)

with open("endpoint_code.txt", "w", encoding="utf-8") as f:
    f.write("\n==========================\n".join(visitor.code_snippets))
