# def add(*args):
#    for n in args:
#        print(n)

def add(*args):
    print(args[0])

    sum = 0
    for n in args:
        sum += n
    return sum

print(add(3, 5, 8 ,23, 54))   
