import random
import threading
from config import FRACTION_MIN, FRACTION_MAX

lock = threading.Lock()
reserved_fractions = set()

def pick_fraction():
    with lock:
        available = [i for i in range(FRACTION_MIN, FRACTION_MAX+1) if i not in reserved_fractions]
        if not available:
            return None
        f = random.choice(available)
        reserved_fractions.add(f)
        return f

def release_fraction(frac):
    with lock:
        reserved_fractions.discard(frac)
