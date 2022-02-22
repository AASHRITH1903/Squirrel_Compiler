from enum import Enum


class Operator(Enum):
    A_AND = "&&"
    A_OR = "||"
    A_EQUAL = "=="
    A_NOT_EQUAL = "!="
    A_LESS_THAN = "<"
    A_GREATER_THAN = ">"
    A_LESS_THAN_EQUAL = "<="
    A_GREATER_THAN_EQUAL = ">="
    A_PLUS = "+"
    A_MINUS = "-"
    A_MULTIPLY = "*"
    A_DIVIDE = "/"
    A_MODULO = "%"
    A_NOT = "!"
    A_NEGATE = "-"
    A_ASSIGN = "="
    A_IF = "if"
    A_ELSE = "else"
    A_WHILE = "while"
    A_FOR = "for"
    A_RETURN = "return"
    A_BREAK = "break"
    A_VAR = "var"
    A_BOOLCONST = "const"
    A_FUNC = "func"
    A_NODE = "node"
    A_ROOT = "root"
    A_DECL = "decl"
    A_IFELSE = "if else"
    A_CONTINUE = "continue"
    A_IFELIF = "if elif"
    A_ELIFSINGLE = "elif single"
    A_ELIFMULTIPLE = "elif multiple"
    A_IFELIFELSE = "if elif else"


class AstNode:
    '''
    If a node contains 2 children, they must be assigned to the left and right attributes
    If a node contains 1 child, it must be assigned to the left child
    '''

    def __init__(self, operator=None, left=None, mid=None, right=None, value=None, next_label=None):
        self.operator = operator
        self.left = left
        self.mid = mid
        self.right = right
        self.value = value

        self.true = None
        self.false = None

        self.code = None
        self.next = next_label

    @staticmethod
    def generateCode(head, get_new_label):
        if head is None:
            return

        # --------------------------------------------------

        if head.operator == Operator.A_ROOT:
            AstNode.generateCode(head.left, get_new_label)
            head.code = head.left.code

            with open("output.tac", "w") as f:
                f.write(head.code)

            # print(head.code)

        # --------------------------------------------------

        elif head.operator == Operator.A_NODE:
            left, right = head.left, head.right

            if left and right:
                head.next = get_new_label()
                right.next = head.next
                left.next = get_new_label()
                AstNode.generateCode(left, get_new_label)
                head.code = left.code + "\n"
                AstNode.generateCode(right, get_new_label)
                head.code += left.next + ":\n" + right.code + "\n" + head.next + ":"
            elif left:
                head.next = get_new_label()
                left.next = get_new_label()
                AstNode.generateCode(left, get_new_label)
                head.code = left.code

        # ------------------------------------------------------------

        elif head.operator == Operator.A_FUNC:
            params, statements = head.left, head.right

            AstNode.generateCode(statements, get_new_label)

            head.code = statements.code + "\n" + head.next + ":\n" + "return\n"

        # ------------------------------------------------------------

        elif head.operator == Operator.A_AND:

            left, right = head.left, head.right
            true, false = head.true, head.false

            left.true = get_new_label()
            left.false = false
            right.true = true
            right.false = false

            AstNode.generateCode(left, get_new_label)
            AstNode.generateCode(right, get_new_label)

            head.code = left.code + "\n" + left.true + ":" + "\n" + right.code + "\n"

        # ------------------------------------------------------------

        elif head.operator == Operator.A_OR:

            left, right = head.left, head.right
            true, false = head.true, head.false

            left.true = true
            left.false = get_new_label()
            right.true = true
            right.false = false

            AstNode.generateCode(left, get_new_label)
            AstNode.generateCode(right, get_new_label)

            head.code = left.code + "\n" + left.false + ":" + "\n" + right.code + "\n"

        # ------------------------------------------------------------

        elif head.operator == Operator.A_IF or head.operator == Operator.A_ELIFSINGLE:
            expr, statements = head.left, head.right

            expr.true = get_new_label()
            expr.false = head.next
            statements.next = head.next

            AstNode.generateCode(expr, get_new_label)
            AstNode.generateCode(statements, get_new_label)

            head.code = expr.code + "\n" + expr.true + ":\n" + statements.code + "\n"

        # ------------------------------------------------------------

        elif head.operator == Operator.A_IFELSE or head.operator == Operator.A_ELIFMULTIPLE or head.operator == Operator.A_IFELIFELSE:
            expr, statements1, statements2 = head.left, head.mid, head.right

            expr.true = get_new_label()
            expr.false = get_new_label()
            statements1.next = head.next
            statements2.next = head.next

            AstNode.generateCode(expr, get_new_label)
            AstNode.generateCode(statements1, get_new_label)
            AstNode.generateCode(statements2, get_new_label)

            head.code = expr.code + "\n" + expr.true + ":\n" + statements1.code + "\n" + \
                "goto " + head.next + "\n" + expr.false + ":\n" + statements2.code + "\n"

        # ------------------------------------------------------------

        elif head.operator == Operator.A_WHILE:
            expr, statements = head.left, head.right

            begin = get_new_label()
            expr.true = get_new_label()
            expr.false = head.next
            statements.next = begin

            AstNode.generateCode(expr, get_new_label)
            AstNode.generateCode(statements, get_new_label)

            head.code = begin + ":\n" + expr.code + "\n" + expr.true + ":\n" + statements.code + "\n" + \
                "goto " + begin

        # ------------------------------------------------------------

        elif head.operator == Operator.A_BOOLCONST:
            if head.value == "true":
                head.code = "goto " + head.true
            elif head.value == "false":
                head.code = "goto " + head.false

        # --------------------------------------------------------------------
