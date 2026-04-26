from math import cbrt as math_cbrt
from math import ceil as math_ceil
from math import cos as math_cos
from math import exp as math_exp
from math import floor as math_floor
from math import gcd as math_gcd
from math import isfinite, isqrt
from math import log as math_log
from math import log2 as math_log2
from math import log10 as math_log10
from math import sin as math_sin
from math import sqrt as math_sqrt
from math import tan as math_tan

from sympy.functions.combinatorial.factorials import binomial as sympy_binomial
from sympy.functions.combinatorial.factorials import factorial as sympy_factorial
from sympy.functions.combinatorial.numbers import catalan as sympy_catalan
from sympy.functions.combinatorial.numbers import fibonacci as sympy_fibonacci
from sympy.functions.combinatorial.numbers import mobius as sympy_mobius
from sympy.functions.combinatorial.numbers import partition as sympy_partition
from sympy.functions.combinatorial.numbers import primepi as sympy_primepi
from sympy.functions.combinatorial.numbers import totient as sympy_totient
from sympy.ntheory.factor_ import factorint as sympy_factorint
from sympy.ntheory.factor_ import perfect_power as sympy_perfect_power
from sympy.ntheory.generate import nextprime as sympy_nextprime
from sympy.ntheory.generate import prevprime as sympy_prevprime
from sympy.ntheory.generate import prime as sympy_prime
from sympy.ntheory.primetest import isprime as sympy_isprime
from sympy.ntheory.residue_ntheory import n_order as sympy_n_order
from sympy.ntheory.residue_ntheory import primitive_root as sympy_primitive_root
from sympy.ntheory.residue_ntheory import sqrt_mod as sympy_sqrt_mod


MAX_ABS_INT = 10 ** 9
MAX_FACTORIAL_N = 1000
MAX_FIBONACCI_N = 10000


def _require_int(value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError


def _require_float(value: int | float) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError


def _require_positive(value: int) -> None:
    _require_int(value)

    if value <= 0:
        raise ValueError


def _require_non_negative(value: int) -> None:
    _require_int(value)

    if value < 0:
        raise ValueError


def _require_small_int(value: int) -> None:
    _require_int(value)

    if abs(value) > MAX_ABS_INT:
        raise ValueError


def _to_int(value: object) -> int:
    if isinstance(value, bool):
        raise ValueError

    if isinstance(value, int):
        return value

    if getattr(value, "is_integer", False) is True:
        return int(value)

    raise ValueError


def _to_float(value: object) -> float:
    result = float(value)

    if not isfinite(result):
        raise ValueError

    return result


def _factorize_positive(n: int) -> dict[int, int]:
    _require_positive(n)

    factors = sympy_factorint(n)

    return {
        int(prime): int(power)
        for prime, power in factors.items()
    }


def gcd(a: int, b: int) -> int:
    _require_int(a)
    _require_int(b)

    return math_gcd(a, b)


def lcm(a: int, b: int) -> int:
    _require_int(a)
    _require_int(b)

    if a == 0 or b == 0:
        return 0

    return abs(a * b) // gcd(a, b)


def divides(a: int, b: int) -> bool:
    _require_int(a)
    _require_int(b)

    if a == 0:
        raise ValueError

    return b % a == 0


def is_even(n: int) -> bool:
    _require_int(n)

    return n % 2 == 0


def is_odd(n: int) -> bool:
    _require_int(n)

    return n % 2 != 0


def is_coprime(a: int, b: int) -> bool:
    _require_int(a)
    _require_int(b)

    return gcd(a, b) == 1


def is_prime(n: int) -> bool:
    _require_int(n)

    return bool(sympy_isprime(n))


def next_prime(n: int) -> int:
    _require_int(n)

    return _to_int(sympy_nextprime(n))


def previous_prime(n: int) -> int:
    _require_int(n)

    if n <= 2:
        raise ValueError

    return _to_int(sympy_prevprime(n))


def nth_prime(n: int) -> int:
    _require_positive(n)

    return _to_int(sympy_prime(n))


def prime_count(n: int) -> int:
    _require_int(n)

    if n < 0:
        raise ValueError

    return _to_int(sympy_primepi(n))


def smallest_prime_factor(n: int) -> int:
    _require_int(n)

    if n < 2:
        raise ValueError

    factors = _factorize_positive(n)

    return min(factors.keys())


def largest_prime_factor(n: int) -> int:
    _require_int(n)

    if n < 2:
        raise ValueError

    factors = _factorize_positive(n)

    return max(factors.keys())


def divisors_count(n: int) -> int:
    factors = _factorize_positive(n)

    result = 1

    for power in factors.values():
        result *= power + 1

    return result


def divisors_sum(n: int) -> int:
    factors = _factorize_positive(n)

    result = 1

    for prime, power in factors.items():
        result *= (prime ** (power + 1) - 1) // (prime - 1)

    return result


def proper_divisors_sum(n: int) -> int:
    _require_positive(n)

    return divisors_sum(n) - n


def euler_phi(n: int) -> int:
    _require_positive(n)

    return _to_int(sympy_totient(n))


def mobius(n: int) -> int:
    _require_positive(n)

    return _to_int(sympy_mobius(n))


def omega(n: int) -> int:
    factors = _factorize_positive(n)

    return len(factors)


def big_omega(n: int) -> int:
    factors = _factorize_positive(n)

    result = 0

    for power in factors.values():
        result += power

    return result


def radical(n: int) -> int:
    factors = _factorize_positive(n)

    result = 1

    for prime in factors:
        result *= prime

    return result


def liouville(n: int) -> int:
    total = big_omega(n)

    if total % 2 == 0:
        return 1

    return -1


def is_square(n: int) -> bool:
    _require_int(n)

    if n < 0:
        return False

    root = isqrt(n)

    return root * root == n


def is_square_free(n: int) -> bool:
    factors = _factorize_positive(n)

    for power in factors.values():
        if power > 1:
            return False

    return True


def is_semiprime(n: int) -> bool:
    _require_int(n)

    if n < 2:
        return False

    return big_omega(n) == 2


def is_perfect(n: int) -> bool:
    _require_positive(n)

    return divisors_sum(n) == 2 * n


def is_abundant(n: int) -> bool:
    _require_positive(n)

    return divisors_sum(n) > 2 * n


def is_deficient(n: int) -> bool:
    _require_positive(n)

    return divisors_sum(n) < 2 * n


def valuation(n: int, p: int) -> int:
    _require_int(n)
    _require_int(p)

    if n == 0 or p < 2 or not is_prime(p):
        raise ValueError

    n = abs(n)
    result = 0

    while n % p == 0:
        result += 1
        n //= p

    return result


def multiplicative_order(a: int, n: int) -> int:
    _require_int(a)
    _require_positive(n)

    if gcd(a, n) != 1:
        raise ValueError

    return _to_int(sympy_n_order(a, n))


def primitive_root(n: int) -> int:
    _require_positive(n)

    result = sympy_primitive_root(n)

    if result is None:
        raise ValueError

    return _to_int(result)


def is_perfect_power(n: int) -> bool:
    _require_int(n)

    if n < 2:
        return False

    return sympy_perfect_power(n) is not False


def mod_pow(a: int, power: int, mod: int) -> int:
    _require_int(a)
    _require_int(power)
    _require_int(mod)

    if power < 0 or mod <= 0:
        raise ValueError

    return pow(a, power, mod)


def mod_inv(a: int, mod: int) -> int:
    _require_int(a)
    _require_int(mod)

    if mod <= 1 or gcd(a, mod) != 1:
        raise ValueError

    return pow(a, -1, mod)


def sqrt_mod_first(a: int, mod: int) -> int:
    _require_int(a)
    _require_positive(mod)

    roots = sympy_sqrt_mod(a, mod, all_roots=True)

    if len(roots) == 0:
        raise ValueError

    return _to_int(roots[0])


def fibonacci(n: int) -> int:
    _require_non_negative(n)

    if n > MAX_FIBONACCI_N:
        raise ValueError

    return _to_int(sympy_fibonacci(n))


def factorial(n: int) -> int:
    _require_non_negative(n)

    if n > MAX_FACTORIAL_N:
        raise ValueError

    return _to_int(sympy_factorial(n))


def binomial(n: int, k: int) -> int:
    _require_non_negative(n)
    _require_non_negative(k)

    if k > n:
        return 0

    if n > MAX_FACTORIAL_N:
        raise ValueError

    return _to_int(sympy_binomial(n, k))


def catalan(n: int) -> int:
    _require_non_negative(n)

    if n > MAX_FACTORIAL_N:
        raise ValueError

    return _to_int(sympy_catalan(n))


def partition(n: int) -> int:
    _require_non_negative(n)

    if n > MAX_FACTORIAL_N:
        raise ValueError

    return _to_int(sympy_partition(n))


def sqrt(x: int | float) -> float:
    _require_float(x)

    if x < 0:
        raise ValueError

    return _to_float(math_sqrt(x))


def cbrt(x: int | float) -> float:
    _require_float(x)

    return _to_float(math_cbrt(x))


def log(x: int | float) -> float:
    _require_float(x)

    if x <= 0:
        raise ValueError

    return _to_float(math_log(x))


def log2(x: int | float) -> float:
    _require_float(x)

    if x <= 0:
        raise ValueError

    return _to_float(math_log2(x))


def log10(x: int | float) -> float:
    _require_float(x)

    if x <= 0:
        raise ValueError

    return _to_float(math_log10(x))


def exp(x: int | float) -> float:
    _require_float(x)

    return _to_float(math_exp(x))


def sin(x: int | float) -> float:
    _require_float(x)

    return _to_float(math_sin(x))


def cos(x: int | float) -> float:
    _require_float(x)

    return _to_float(math_cos(x))


def tan(x: int | float) -> float:
    _require_float(x)

    return _to_float(math_tan(x))


def floor(x: int | float) -> int:
    _require_float(x)

    return int(math_floor(x))


def ceil(x: int | float) -> int:
    _require_float(x)

    return int(math_ceil(x))


def round_value(x: int | float) -> int:
    _require_float(x)

    return int(round(x))


def abs_value(x: int | float) -> int | float:
    _require_float(x)

    return abs(x)


ALLOWED_FUNCTIONS = {
    "gcd": gcd,
    "lcm": lcm,
    "divides": divides,

    "is_even": is_even,
    "is_odd": is_odd,
    "is_coprime": is_coprime,
    "is_prime": is_prime,

    "next_prime": next_prime,
    "prev_prime": previous_prime,
    "nth_prime": nth_prime,

    "prime_count": prime_count,
    "primepi": prime_count,
    "pi_n": prime_count,

    "spf": smallest_prime_factor,
    "lpf": largest_prime_factor,

    "tau": divisors_count,
    "d0": divisors_count,
    "divisors_count": divisors_count,

    "sigma": divisors_sum,
    "d1": divisors_sum,
    "divisors_sum": divisors_sum,

    "phi": euler_phi,
    "euler": euler_phi,

    "mobius": mobius,
    "mu": mobius,

    "omega": omega,
    "big_omega": big_omega,

    "rad": radical,
    "radical": radical,

    "liouville": liouville,
    "liouville_lambda": liouville,
    "lambda_n": liouville,

    "is_square": is_square,
    "is_square_free": is_square_free,
    "is_semiprime": is_semiprime,
    "is_perfect": is_perfect,
    "is_abundant": is_abundant,
    "is_deficient": is_deficient,
    "is_perfect_power": is_perfect_power,

    "vp": valuation,
    "ord_mod": multiplicative_order,
    "primitive_root": primitive_root,

    "mod_pow": mod_pow,
    "pow_mod": mod_pow,
    "mod_inv": mod_inv,
    "inv_mod": mod_inv,
    "sqrt_mod": sqrt_mod_first,

    "fib": fibonacci,
    "factorial": factorial,
    "fact": factorial,
    "binomial": binomial,
    "C": binomial,
    "catalan": catalan,
    "partition": partition,

    "sqrt": sqrt,
    "cbrt": cbrt,
    "log": log,
    "log2": log2,
    "log10": log10,
    "exp": exp,
    "sin": sin,
    "cos": cos,
    "tan": tan,
    "floor": floor,
    "ceil": ceil,
    "round": round_value,
    "abs": abs_value,
}
