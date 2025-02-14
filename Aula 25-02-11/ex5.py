base = int(input("Infome o tamanho da base: "))
alt = int(input("Infome o tamanho da altura: "))

for i in range(base):
    print("*", end="") if (i + 1 != base) else print("*")

for k in range(alt - 2):
    if (k == 0):
        print("*", end="")
    print(" ", end="") if (k == base) else print("*", end="")
    if (k == alt - 3):
        print("*")

for l in range(base):
    print("*",end="")