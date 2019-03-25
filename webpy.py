import ast
from itertools import chain, islice, tee

class JSCompiler(ast.NodeVisitor):
    def generic_visit(self, node):
        raise ValueError(f"Unsupported node: {node.__class__.__name__}")

    def visit_Module(self, node):
        return ";\n".join(chain((self.visit(stmt) for stmt in node.body), ['']))

    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_Num(self, node):
        return str(node.n)

    def visit_Name(self, node):
        return node.id

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        op = self.visit(node.op)
        right = self.visit(node.right)
        return f"{left} {op} {right}"


    def visit_Compare(self, node):
        comparators = chain([node.left], node.comparators)
        comparators = map(self.visit, comparators)
        lefts, rights = tee(comparators)
        rights = islice(rights, 1, None)
        ops = map(self.visit, node.ops)
        return " && ".join(
            f"({left} {op} {right})" 
            for left, op, right in zip(lefts, ops, rights)
        )
    
    def visit_Add(self, node):
        return "+"

    def visit_Sub(self, node):
        return "-"

    def visit_Mult(self, node):
        return "*"

    def visit_Div(self, node):
        return "/"

    def visit_Lt(self, node):
        return "<"

    def visit_LtE(self, node):
        return "<="

    def visit_Gt(self, node):
        return ">"

    def visit_GtE(self, node):
        return ">="

    def visit_Eq(self, node):
        return "==="

    def visit_NotEq(self, node):
        return "!=="

    @classmethod
    def compile(cls, s):
        compiler = cls()
        return compiler.visit(ast.parse(s))