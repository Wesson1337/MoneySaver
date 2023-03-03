from decimal import Decimal

print(Decimal(100000000000000.01).quantize(Decimal(".01")) + Decimal(100000.01))
