var_a = 10

def escrever_var():
    global var_a
    var_a = 99
    print(var_a)
    # print(var_b)

escrever_var()

print(var_a)