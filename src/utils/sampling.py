import random
from typing import List, Any

def weighted_choice(items: List[Any], weights: List[float]) -> Any:
    return random.choices(items, weights=weights, k=1)[0]

def probability_event(p: float) -> bool:
    return random.random() < p
