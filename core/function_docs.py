from dataclasses import dataclass


@dataclass(frozen=True)
class FunctionDoc:
    name: str
    signature: str
    category: str
    description: str
    aliases: list[str]


FUNCTION_DOCS = [
    FunctionDoc(
        name="gcd",
        signature="gcd(x, y)",
        category="Базовая арифметика",
        description="Возвращает наибольший общий делитель чисел x и y.",
        aliases=[],
    ),
    FunctionDoc(
        name="lcm",
        signature="lcm(x, y)",
        category="Базовая арифметика",
        description="Возвращает наименьшее общее кратное чисел x и y.",
        aliases=[],
    ),
    FunctionDoc(
        name="divides",
        signature="divides(x, y)",
        category="Базовая арифметика",
        description="Проверяет, делит ли x число y.",
        aliases=[],
    ),
    FunctionDoc(
        name="is_even",
        signature="is_even(x)",
        category="Базовая арифметика",
        description="Проверяет, является ли число x чётным.",
        aliases=[],
    ),
    FunctionDoc(
        name="is_odd",
        signature="is_odd(x)",
        category="Базовая арифметика",
        description="Проверяет, является ли число x нечётным.",
        aliases=[],
    ),
    FunctionDoc(
        name="is_coprime",
        signature="is_coprime(x, y)",
        category="Простые числа",
        description="Проверяет, являются ли x и y взаимно простыми.",
        aliases=[],
    ),
    FunctionDoc(
        name="is_prime",
        signature="is_prime(x)",
        category="Простые числа",
        description="Проверяет, является ли x простым числом.",
        aliases=[],
    ),
    FunctionDoc(
        name="next_prime",
        signature="next_prime(x)",
        category="Простые числа",
        description="Возвращает первое простое число, строго большее x.",
        aliases=[],
    ),
    FunctionDoc(
        name="prev_prime",
        signature="prev_prime(x)",
        category="Простые числа",
        description="Возвращает предыдущее простое число, строго меньшее x.",
        aliases=[],
    ),
    FunctionDoc(
        name="nth_prime",
        signature="nth_prime(x)",
        category="Простые числа",
        description="Возвращает x-е простое число.",
        aliases=[],
    ),
    FunctionDoc(
        name="prime_count",
        signature="prime_count(x)",
        category="Простые числа",
        description="Возвращает количество простых чисел, не превосходящих x.",
        aliases=[
            "primepi",
            "pi_n",
        ],
    ),
    FunctionDoc(
        name="spf",
        signature="spf(x)",
        category="Простые числа",
        description="Возвращает наименьший простой делитель числа x.",
        aliases=[],
    ),
    FunctionDoc(
        name="lpf",
        signature="lpf(x)",
        category="Простые числа",
        description="Возвращает наибольший простой делитель числа x.",
        aliases=[],
    ),
    FunctionDoc(
        name="tau",
        signature="tau(x)",
        category="Делители и мультипликативные функции",
        description="Возвращает количество положительных делителей числа x.",
        aliases=[
            "d0",
            "divisors_count",
        ],
    ),
    FunctionDoc(
        name="sigma",
        signature="sigma(x)",
        category="Делители и мультипликативные функции",
        description="Возвращает сумму положительных делителей числа x.",
        aliases=[
            "d1",
            "divisors_sum",
        ],
    ),
    FunctionDoc(
        name="phi",
        signature="phi(x)",
        category="Делители и мультипликативные функции",
        description="Возвращает значение функции Эйлера для x.",
        aliases=[
            "euler",
        ],
    ),
    FunctionDoc(
        name="mu",
        signature="mu(x)",
        category="Делители и мультипликативные функции",
        description="Возвращает значение функции Мёбиуса для x.",
        aliases=[
            "mobius",
        ],
    ),
    FunctionDoc(
        name="omega",
        signature="omega(x)",
        category="Делители и мультипликативные функции",
        description="Возвращает количество различных простых делителей x.",
        aliases=[],
    ),
    FunctionDoc(
        name="big_omega",
        signature="big_omega(x)",
        category="Делители и мультипликативные функции",
        description="Возвращает количество простых делителей x с учётом кратности.",
        aliases=[],
    ),
    FunctionDoc(
        name="rad",
        signature="rad(x)",
        category="Делители и мультипликативные функции",
        description="Возвращает радикал числа x.",
        aliases=[
            "radical",
        ],
    ),
    FunctionDoc(
        name="liouville",
        signature="liouville(x)",
        category="Делители и мультипликативные функции",
        description="Возвращает значение функции Лиувилля для x.",
        aliases=[
            "liouville_lambda",
            "lambda_n",
        ],
    ),
    FunctionDoc(
        name="is_square",
        signature="is_square(x)",
        category="Классификация чисел",
        description="Проверяет, является ли x полным квадратом.",
        aliases=[],
    ),
    FunctionDoc(
        name="is_square_free",
        signature="is_square_free(x)",
        category="Классификация чисел",
        description="Проверяет, свободно ли x от квадратов.",
        aliases=[],
    ),
    FunctionDoc(
        name="is_semiprime",
        signature="is_semiprime(x)",
        category="Классификация чисел",
        description="Проверяет, является ли x произведением двух простых чисел с учётом кратности.",
        aliases=[],
    ),
    FunctionDoc(
        name="is_perfect",
        signature="is_perfect(x)",
        category="Классификация чисел",
        description="Проверяет, является ли x совершенным числом.",
        aliases=[],
    ),
    FunctionDoc(
        name="is_abundant",
        signature="is_abundant(x)",
        category="Классификация чисел",
        description="Проверяет, является ли x избыточным числом.",
        aliases=[],
    ),
    FunctionDoc(
        name="is_deficient",
        signature="is_deficient(x)",
        category="Классификация чисел",
        description="Проверяет, является ли x недостаточным числом.",
        aliases=[],
    ),
    FunctionDoc(
        name="is_perfect_power",
        signature="is_perfect_power(x)",
        category="Классификация чисел",
        description="Проверяет, является ли x точной степенью вида y^k, где k > 1.",
        aliases=[],
    ),
    FunctionDoc(
        name="vp",
        signature="vp(x, y)",
        category="Модулярная арифметика",
        description="Возвращает y-адическую валюацию числа x.",
        aliases=[],
    ),
    FunctionDoc(
        name="ord_mod",
        signature="ord_mod(x, y)",
        category="Модулярная арифметика",
        description="Возвращает мультипликативный порядок x по модулю y.",
        aliases=[],
    ),
    FunctionDoc(
        name="primitive_root",
        signature="primitive_root(x)",
        category="Модулярная арифметика",
        description="Возвращает первообразный корень по модулю x, если он существует.",
        aliases=[],
    ),
    FunctionDoc(
        name="mod_pow",
        signature="mod_pow(x, y, mod)",
        category="Модулярная арифметика",
        description="Возвращает x^y по модулю mod.",
        aliases=[
            "pow_mod",
        ],
    ),
    FunctionDoc(
        name="mod_inv",
        signature="mod_inv(x, y)",
        category="Модулярная арифметика",
        description="Возвращает обратный элемент к x по модулю y.",
        aliases=[
            "inv_mod",
        ],
    ),
    FunctionDoc(
        name="sqrt_mod",
        signature="sqrt_mod(x, y)",
        category="Модулярная арифметика",
        description="Возвращает один квадратный корень из x по модулю y.",
        aliases=[],
    ),
    FunctionDoc(
        name="fib",
        signature="fib(x)",
        category="Комбинаторика",
        description="Возвращает x-е число Фибоначчи.",
        aliases=[],
    ),
    FunctionDoc(
        name="factorial",
        signature="factorial(x)",
        category="Комбинаторика",
        description="Возвращает факториал числа x.",
        aliases=[
            "fact",
        ],
    ),
    FunctionDoc(
        name="binomial",
        signature="binomial(x, y)",
        category="Комбинаторика",
        description="Возвращает биномиальный коэффициент C(x, y).",
        aliases=[
            "C",
        ],
    ),
    FunctionDoc(
        name="catalan",
        signature="catalan(x)",
        category="Комбинаторика",
        description="Возвращает x-е число Каталана.",
        aliases=[],
    ),
    FunctionDoc(
        name="partition",
        signature="partition(x)",
        category="Комбинаторика",
        description="Возвращает количество разбиений числа x.",
        aliases=[],
    ),
    FunctionDoc(
        name="sqrt",
        signature="sqrt(x)",
        category="Алгебраические функции",
        description="Возвращает квадратный корень из x.",
        aliases=[],
    ),
    FunctionDoc(
        name="cbrt",
        signature="cbrt(x)",
        category="Алгебраические функции",
        description="Возвращает кубический корень из x.",
        aliases=[],
    ),
    FunctionDoc(
        name="log",
        signature="log(x)",
        category="Алгебраические функции",
        description="Возвращает натуральный логарифм x.",
        aliases=[],
    ),
    FunctionDoc(
        name="log2",
        signature="log2(x)",
        category="Алгебраические функции",
        description="Возвращает логарифм x по основанию 2.",
        aliases=[],
    ),
    FunctionDoc(
        name="log10",
        signature="log10(x)",
        category="Алгебраические функции",
        description="Возвращает десятичный логарифм x.",
        aliases=[],
    ),
    FunctionDoc(
        name="exp",
        signature="exp(x)",
        category="Алгебраические функции",
        description="Возвращает e^x.",
        aliases=[],
    ),
    FunctionDoc(
        name="sin",
        signature="sin(x)",
        category="Тригонометрические функции",
        description="Возвращает синус x. Аргумент задаётся в радианах.",
        aliases=[],
    ),
    FunctionDoc(
        name="cos",
        signature="cos(x)",
        category="Тригонометрические функции",
        description="Возвращает косинус x. Аргумент задаётся в радианах.",
        aliases=[],
    ),
    FunctionDoc(
        name="tan",
        signature="tan(x)",
        category="Тригонометрические функции",
        description="Возвращает тангенс x. Аргумент задаётся в радианах.",
        aliases=[],
    ),
    FunctionDoc(
        name="floor",
        signature="floor(x)",
        category="Округления",
        description="Возвращает наибольшее целое число, не превосходящее x.",
        aliases=[],
    ),
    FunctionDoc(
        name="ceil",
        signature="ceil(x)",
        category="Округления",
        description="Возвращает наименьшее целое число, не меньшее x.",
        aliases=[],
    ),
    FunctionDoc(
        name="round",
        signature="round(x)",
        category="Округления",
        description="Округляет x до ближайшего целого.",
        aliases=[],
    ),
    FunctionDoc(
        name="abs",
        signature="abs(x)",
        category="Алгебраические функции",
        description="Возвращает модуль числа x.",
        aliases=[],
    ),
]


def get_function_docs() -> list[FunctionDoc]:
    return FUNCTION_DOCS


def get_function_doc(name: str) -> FunctionDoc | None:
    for function_doc in FUNCTION_DOCS:
        if function_doc.name == name or name in function_doc.aliases:
            return function_doc

    return None