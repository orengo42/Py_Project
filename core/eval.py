import ast
import keyword

from core.number_theory import ALLOWED_FUNCTIONS


ALLOWED_NODE_TYPES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Name,
    ast.Load,
    ast.Constant,
    ast.Call,

    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,

    ast.USub,
    ast.UAdd,
    ast.Not,

    ast.And,
    ast.Or,

    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
)


class SafeExpressionError(Exception):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def validate_variable_name(variable_name: str) -> None:
    if variable_name.strip() == "":
        raise SafeExpressionError("EMPTY_VARIABLE_NAME")

    if not variable_name.isidentifier():
        raise SafeExpressionError("INVALID_VARIABLE_NAME")

    if keyword.iskeyword(variable_name):
        raise SafeExpressionError("INVALID_VARIABLE_NAME")

    if variable_name in ALLOWED_FUNCTIONS:
        raise SafeExpressionError("VARIABLE_NAME_CONFLICT")


def validate_expression_for_variables(
    expression: str,
    variable_names: set[str],
) -> ast.Expression:
    if expression.strip() == "":
        raise SafeExpressionError("EMPTY_EXPRESSION")

    if len(variable_names) == 0:
        raise SafeExpressionError("NO_VARIABLES")

    for variable_name in variable_names:
        validate_variable_name(variable_name)

    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError:
        raise SafeExpressionError("SYNTAX_ERROR")

    function_names = set(ALLOWED_FUNCTIONS.keys())

    for node in ast.walk(tree):
        if not isinstance(node, ALLOWED_NODE_TYPES):
            raise SafeExpressionError("FORBIDDEN_EXPRESSION")

        if isinstance(node, ast.Name):
            is_variable = node.id in variable_names
            is_function = node.id in function_names

            if not is_variable and not is_function:
                raise SafeExpressionError("UNKNOWN_NAME")

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise SafeExpressionError("FORBIDDEN_FUNCTION_CALL")

            if node.func.id not in function_names:
                raise SafeExpressionError("UNKNOWN_FUNCTION")

            if len(node.keywords) > 0:
                raise SafeExpressionError("FORBIDDEN_FUNCTION_CALL")

        if isinstance(node, ast.Constant):
            if not isinstance(node.value, (int, float, bool)):
                raise SafeExpressionError("FORBIDDEN_CONSTANT")

    return tree


def compile_expression_for_variables(
    expression: str,
    variable_names: set[str],
):
    try:
        tree = validate_expression_for_variables(expression, variable_names)
        return compile(tree, filename="<user_expression>", mode="eval")
    except SafeExpressionError:
        raise
    except Exception:
        raise SafeExpressionError("COMPILE_ERROR")


def evaluate_compiled_expression_for_variables(
    code,
    variables: dict[str, int],
) -> object:
    try:
        local_names = ALLOWED_FUNCTIONS.copy()
        local_names.update(variables)

        return eval(code, {"__builtins__": {}}, local_names)
    except ZeroDivisionError:
        raise SafeExpressionError("DIVISION_BY_ZERO")
    except OverflowError:
        raise SafeExpressionError("OVERFLOW_ERROR")
    except TypeError:
        raise SafeExpressionError("TYPE_ERROR")
    except ValueError:
        raise SafeExpressionError("VALUE_ERROR")
    except Exception:
        raise SafeExpressionError("RUNTIME_ERROR")


def compile_expression(expression: str, variable_name: str = "x"):
    return compile_expression_for_variables(
        expression,
        {variable_name},
    )


def evaluate_compiled_expression(
    code,
    variable_name: str,
    variable_value: int,
) -> object:
    return evaluate_compiled_expression_for_variables(
        code,
        {
            variable_name: variable_value,
        },
    )


def evaluate_expression(
    expression: str,
    variable_name: str,
    variable_value: int,
) -> object:
    code = compile_expression(expression, variable_name)

    return evaluate_compiled_expression(
        code,
        variable_name,
        variable_value,
    )