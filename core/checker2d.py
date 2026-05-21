from core.models import Hypothesis2DPoint, Hypothesis2DResult
from core.eval import (
    SafeExpressionError,
    compile_expression_for_variables,
    evaluate_compiled_expression_for_variables,
)

from core.Profiler import profile_helper

@profile_helper("check_hypothesis_2d.prof")
def check_hypothesis_2d(
    expression: str,
    x_start: int = 1,
    x_end: int = 10,
    y_start: int = 1,
    y_end: int = 10,
    x_variable_name: str = "x",
    y_variable_name: str = "y",
    max_points: int = 10000,
) -> Hypothesis2DResult:
    if x_variable_name == y_variable_name:
        return Hypothesis2DResult(
            expression=expression,
            x_variable_name=x_variable_name,
            y_variable_name=y_variable_name,
            x_start=x_start,
            x_end=x_end,
            y_start=y_start,
            y_end=y_end,
            checked_count=0,
            is_true=False,
            points=[],
            error_code="SAME_VARIABLE_NAMES",
        )

    if x_start > x_end or y_start > y_end:
        return Hypothesis2DResult(
            expression=expression,
            x_variable_name=x_variable_name,
            y_variable_name=y_variable_name,
            x_start=x_start,
            x_end=x_end,
            y_start=y_start,
            y_end=y_end,
            checked_count=0,
            is_true=False,
            points=[],
            error_code="INVALID_RANGE",
        )

    x_count = x_end - x_start + 1
    y_count = y_end - y_start + 1
    total_points = x_count * y_count

    if total_points > max_points:
        return Hypothesis2DResult(
            expression=expression,
            x_variable_name=x_variable_name,
            y_variable_name=y_variable_name,
            x_start=x_start,
            x_end=x_end,
            y_start=y_start,
            y_end=y_end,
            checked_count=0,
            is_true=False,
            points=[],
            error_code="TOO_MANY_POINTS",
        )

    variable_names = {
        x_variable_name,
        y_variable_name,
    }

    try:
        code = compile_expression_for_variables(expression, variable_names)
    except SafeExpressionError as error:
        return Hypothesis2DResult(
            expression=expression,
            x_variable_name=x_variable_name,
            y_variable_name=y_variable_name,
            x_start=x_start,
            x_end=x_end,
            y_start=y_start,
            y_end=y_end,
            checked_count=0,
            is_true=False,
            points=[],
            error_code=error.code,
        )

    checked_count = 0
    points = []
    is_true = True

    for x_value in range(x_start, x_end + 1):
        for y_value in range(y_start, y_end + 1):
            checked_count += 1

            variables = {
                x_variable_name: x_value,
                y_variable_name: y_value,
            }

            try:
                value = evaluate_compiled_expression_for_variables(
                    code,
                    variables,
                )
            except SafeExpressionError as error:
                is_true = False

                points.append(
                    Hypothesis2DPoint(
                        x_value=x_value,
                        y_value=y_value,
                        value=None,
                        error_code=error.code,
                    )
                )

                continue

            if not isinstance(value, bool):
                return Hypothesis2DResult(
                    expression=expression,
                    x_variable_name=x_variable_name,
                    y_variable_name=y_variable_name,
                    x_start=x_start,
                    x_end=x_end,
                    y_start=y_start,
                    y_end=y_end,
                    checked_count=checked_count,
                    is_true=False,
                    points=points,
                    error_code="NOT_BOOLEAN_RESULT",
                )

            if not value:
                is_true = False

            points.append(
                Hypothesis2DPoint(
                    x_value=x_value,
                    y_value=y_value,
                    value=value,
                )
            )

    return Hypothesis2DResult(
        expression=expression,
        x_variable_name=x_variable_name,
        y_variable_name=y_variable_name,
        x_start=x_start,
        x_end=x_end,
        y_start=y_start,
        y_end=y_end,
        checked_count=checked_count,
        is_true=is_true,
        points=points,
    )

@profile_helper("get_counterexample_points.prof")
def get_counterexample_points(
    result: Hypothesis2DResult,
) -> list[tuple[int, int]]:
    counterexamples = []

    for point in result.points:
        if point.value is False and point.error_code is None:
            counterexamples.append(
                (
                    point.x_value,
                    point.y_value,
                )
            )

    return counterexamples

@profile_helper("get_error_points.prof")
def get_error_points(
    result: Hypothesis2DResult,
) -> list[tuple[int, int, str]]:
    errors = []

    for point in result.points:
        if point.error_code is not None:
            errors.append(
                (
                    point.x_value,
                    point.y_value,
                    point.error_code,
                )
            )

    return errors

@profile_helper("get_plot_cells.prof")
def get_plot_cells(
    result: Hypothesis2DResult,
) -> list[tuple[int, int, str, str | None]]:
    cells = []

    for point in result.points:
        if point.error_code is not None:
            status = "error"
        elif point.value is False:
            status = "counterexample"
        else:
            status = "true"

        cells.append(
            (
                point.x_value,
                point.y_value,
                status,
                point.error_code,
            )
        )

    return cells

@profile_helper("count_counterexample.prof")
def count_counterexamples(result: Hypothesis2DResult) -> int:
    return len(get_counterexample_points(result))

@profile_helper("count_error_points.prof")
def count_error_points(result: Hypothesis2DResult) -> int:
    return len(get_error_points(result))