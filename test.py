import math
x = 12.23
frac,whole = math.modf(x)
frac *= 100

print(int(frac))
print(int(whole))