import cProfile
import functools
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILES_DIR = os.path.join(BASE_DIR, "profiles")

def profile_helper(filename="hypothesis_profile.prof"):
    """Декоратор для профилирования функций ядра"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            os.makedirs(PROFILES_DIR, exist_ok=True)
            
            full_profile_path = os.path.join(PROFILES_DIR, filename)
            
            prof = cProfile.Profile()
            result = prof.runcall(func, *args, **kwargs)
            prof.dump_stats(full_profile_path)
            return result
        return wrapper
    return decorator