from math import floor

def fuel_count_upper(mass: int) -> int:
    return floor(mass / 3) - 2

# Tests
# print(fuel_count_upper(12)) # 2
# print(fuel_count_upper(14)) # 2
# print(fuel_count_upper(1969)) # 654
# print(fuel_count_upper(100756)) # 33583

total = 0
with open("input.txt") as file:
    for line in file.readlines():
        fuel = fuel_count_upper(int(line))
        total += fuel
        while True:
            fuel = fuel_count_upper(fuel)
            if fuel <= 0:
                break
            else:
                total += fuel

print(total)