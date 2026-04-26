from core.models import ValuesResult, ValuePoint
from core.eval import (
    SafeExpressionError,
    compile_expression,
    evaluate_compiled_expression,
)


def build_values(
    expression: str,
    variable_name: str = "n",
    start: int = 1,
    end: int = 100,
) -> ValuesResult:
    if start > end:
        return ValuesResult(
            expression=expression,
            variable_name=variable_name,
            start=start,
            end=end,
            points=[],
            error_code="INVALID_RANGE",
        )

    try:
        code = compile_expression(expression, variable_name)
    except SafeExpressionError as error:
        return ValuesResult(
            expression=expression,
            variable_name=variable_name,
            start=start,
            end=end,
            points=[],
            error_code=error.code,
        )

    points = []

    for variable_value in range(start, end + 1):
        try:
            value = evaluate_compiled_expression(
                code,
                variable_name,
                variable_value,
            )

            points.append(
                ValuePoint(
                    variable_value=variable_value,
                    value=value,
                )
            )

        except SafeExpressionError as error:
            points.append(
                ValuePoint(
                    variable_value=variable_value,
                    value=None,
                    error_code=error.code,
                )
            )

    return ValuesResult(
        expression=expression,
        variable_name=variable_name,
        start=start,
        end=end,
        points=points,
    )


def convert_to_graph_value(value: object) -> float | None: #решил что если результат булевский (например is_prime) то буду
    if isinstance(value, bool):  #                                          делать 0/1. Лучше идей пока нет.
        return 1.0 if value else 0.0

    if isinstance(value, int) or isinstance(value, float):
        return float(value)

    return None


def get_graph_points(result: ValuesResult) -> list[tuple[int, float]]:
    graph_points = []

    for point in result.points:
        if point.error_code is not None:
            continue

        graph_value = convert_to_graph_value(point.value)

        if graph_value is not None:
            graph_points.append(
                (
                    point.variable_value,
                    graph_value,
                )
            )

    return graph_points