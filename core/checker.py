from core.models import CheckResult
from core.eval import (
    SafeExpressionError,
    compile_expression,
    evaluate_compiled_expression,
)


def check_hypothesis(
    expression: str,
    variable_name: str = "n",
    start: int = 1,
    end: int = 100000,
    max_counterexamples: int = 20,
) -> CheckResult:
    if start > end:
        return CheckResult(
            expression=expression,
            variable_name=variable_name,
            start=start,
            end=end,
            checked_count=0,
            is_true=False,
            counterexamples=[],
            error_code="INVALID_RANGE",
        )

    try:
        code = compile_expression(expression, variable_name)
    except SafeExpressionError as error:
        return CheckResult(
            expression=expression,
            variable_name=variable_name,
            start=start,
            end=end,
            checked_count=0,
            is_true=False,
            counterexamples=[],
            error_code=error.code,
        )

    counterexamples = []
    checked_count = 0

    for variable_value in range(start, end + 1):
        checked_count += 1

        try:
            result = evaluate_compiled_expression(
                code,
                variable_name,
                variable_value,
            )
        except SafeExpressionError as error:
            return CheckResult(
                expression=expression,
                variable_name=variable_name,
                start=start,
                end=end,
                checked_count=checked_count,
                is_true=False,
                counterexamples=counterexamples,
                error_code=error.code,
            )

        if not isinstance(result, bool):
            return CheckResult(
                expression=expression,
                variable_name=variable_name,
                start=start,
                end=end,
                checked_count=checked_count,
                is_true=False,
                counterexamples=counterexamples,
                error_code="NOT_BOOLEAN_RESULT",
            )

        if not result:
            counterexamples.append(variable_value)

            if len(counterexamples) >= max_counterexamples:
                break

    return CheckResult(
        expression=expression,
        variable_name=variable_name,
        start=start,
        end=end,
        checked_count=checked_count,
        is_true=len(counterexamples) == 0,
        counterexamples=counterexamples,
    )