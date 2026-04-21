from decimal import Decimal
import random


def _price_bounds(category):
    if category == "Grocery":
        return Decimal("20"), Decimal("850")
    if category == "Gadgets":
        return Decimal("799"), Decimal("159999")
    return Decimal("199"), Decimal("8999")


def update_price_value(current_price, category):
    base = Decimal(str(current_price))
    change_pct = Decimal(str(random.uniform(-0.12, 0.12)))
    new_value = (base * (Decimal("1") + change_pct)).quantize(Decimal("0.01"))
    lower, upper = _price_bounds(category)
    return min(max(new_value, lower), upper)