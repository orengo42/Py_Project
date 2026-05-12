from dataclasses import dataclass


@dataclass
class CheckResult:
    expression: str
    variable_name: str
    start: int
    end: int
    checked_count: int
    is_true: bool
    counterexamples: list[int]
    error_code: str | None = None


@dataclass
class ValuePoint:
    variable_value: int
    value: object | None
    error_code: str | None = None


@dataclass
class ValuesResult:
    expression: str
    variable_name: str
    start: int
    end: int
    points: list[ValuePoint]
    error_code: str | None = None


@dataclass
class Hypothesis2DPoint:
    x_value: int
    y_value: int
    value: bool | None
    error_code: str | None = None


@dataclass
class Hypothesis2DResult:
    expression: str
    x_variable_name: str
    y_variable_name: str
    x_start: int
    x_end: int
    y_start: int
    y_end: int
    checked_count: int
    is_true: bool
    points: list[Hypothesis2DPoint]
    error_code: str | None = None