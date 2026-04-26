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